#!/usr/bin/env python

# Copyright 2020 The Tekton Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ntpath
import os
import shutil
import tempfile
import unittest
from unittest import mock
from urllib.parse import urlparse

import git
import sync

from sync import (
    doc_config, docs_from_tree, get_links, is_absolute_url,
    is_fragment, get_tags, load_config, save_config,
    get_files_in_path, transform_link, transform_links_doc,
    transform_doc, transform_docs, read_front_matter)


BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

class TestSync(unittest.TestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        # Create a test repo in a tmp dir
        self.gitrepo = git.Repo.init(self._tempdir.name)
        # Copy test content in it
        docs_folder = os.path.join(self._tempdir.name, 'test-content')
        shutil.copytree(os.path.join(BASE_FOLDER, 'test-content'), docs_folder)
        # Commit the new content
        self.gitrepo.index.add(docs_folder)
        self.gitrepo.index.commit("Added test content")
        # Create a tag
        self.tagname = "test_version"
        self.gitrepo.create_tag(self.tagname)
        self.doc = self.gitrepo.tree().join('test-content/content.md')

    def tearDown(self):
        self._tempdir.cleanup()

    # Utils
    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def read_and_delete_file(self, name):
        file = open(name, "r")
        text = file.read()
        file.close()
        os.remove(name)
        return text

    # Tests
    def test_doc_config(self):
        folder_config = dict(index='foo.md')

        expected = ('content.md', '', None)
        actual = doc_config(self.doc, folder_config)
        self.assertEqual(actual, expected)

    def test_doc_config_header(self):
        folder_config = dict(
            index='foo.md',
            header={'title': 'test'})

        header = folder_config['header']
        header['weight'] = 10
        expected = ('content.md', '', header)
        actual = doc_config(self.doc, folder_config, 10)
        self.assertEqual(actual, expected)

    def test_doc_config_index_target(self):
        folder_config = dict(
            index='content.md',
            header={'title': 'test'},
            target='foobar')

        header = folder_config['header']
        header['weight'] = 10
        expected = ('_index.md', 'foobar', header)
        actual = doc_config(self.doc, folder_config, 10)
        self.assertEqual(actual, expected)

    def test_docs_from_tree(self):
        tree = self.gitrepo.tree().join('test-content')
        expected = ['content.md', 'test.txt', 'unwanted.txt']
        actual = [x.name for x in docs_from_tree(tree)]
        self.assertEqual(actual, expected)

    def test_docs_from_tree_include(self):
        tree = self.gitrepo.tree().join('test-content')
        expected = ['content.md']
        actual = [x.name for x in
            docs_from_tree(tree, include=['*.md'])]
        self.assertEqual(actual, expected)

    def test_docs_from_tree_include_specific(self):
        tree = self.gitrepo.tree().join('test-content')
        expected = ['content.md', 'test.txt']
        actual = [x.name for x in
            docs_from_tree(tree, include=['content.md', 'test.txt'])]
        self.assertEqual(actual, expected)

    def test_docs_from_tree_include_subfolder(self):
        tree = self.gitrepo.tree().join('test-content/nested')
        expected = ['content.md']
        actual = [x.name for x in
            docs_from_tree(tree, include=['content.md'])]
        self.assertEqual(actual, expected)

    def test_docs_from_tree_exclude(self):
        tree = self.gitrepo.tree().join('test-content')
        expected = ['content.md']
        actual = [x.name for x in
            docs_from_tree(tree, exclude=['*.txt'])]
        self.assertEqual(actual, expected)

    def test_is_fragment(self):
        """ Verify if a string is a reference. A reference is
        defined as  a string where its first character is a hashtag """
        self.assertFalse(is_fragment(urlparse("")))
        self.assertTrue(is_fragment(urlparse("#footer")))
        self.assertFalse(is_fragment(urlparse("www.google.com")))

    def test_get_tags(self):
        """ map a list of dictionaries to only
        have name, displayName feilds """
        expected = [{'name': 'test_tag', 'displayName': 'test_display'}]
        tags = {'tags': [
            {
                'name': 'test_tag',
                'displayName': 'test_display',
                'files': []
            },
        ]}

        self.assertEqual(get_tags(tags), expected)

    def test_load_save_config(self):
        """ convert a list of files into a list of dictionaries """
        # create a tmp file with yaml txt
        text = "{displayOrder: 1}"

        with tempfile.NamedTemporaryFile(dir='/tmp', delete=False) as tmp:
            tmp_name = tmp.name
            tmp.write(text.strip().encode())

        expected = [{'content': {'displayOrder': 1},
                     'filename': tmp_name}]
        actual = load_config([tmp_name])
        self.assertEqual(actual, expected)

        mod_config = actual
        mod_config[0]['content']['displayOrder'] = 2
        expected = [{'content': {'displayOrder': 2},
                     'filename': tmp_name}]
        save_config(mod_config)
        actual = load_config([tmp_name])
        self.assertEqual(actual, expected)
        self.read_and_delete_file(tmp_name)

    def test_get_files_in_path(self):
        """ create a list of files within a
        directory that contain a valid extension"""

        with tempfile.NamedTemporaryFile(dir='/tmp', delete=True) as tmp:
            expected = [tmp.name]
            actual = get_files_in_path("/tmp", self.path_leaf(tmp.name))

        self.assertEqual(actual, expected)

        with tempfile.NamedTemporaryFile(dir='/tmp', delete=True) as tmp:
            expected = [tmp.name]
            actual = get_files_in_path("/tmp", self.path_leaf(tmp.name))

        self.assertEqual(actual, expected)

    def test_get_links(self):
        """ return a list of links formatted in markdown in a given string"""
        actual = "www.link.com"

        expected = get_links("")
        self.assertEqual([], expected)

        expected = get_links("[link](www.link.com) this is a link")
        self.assertEqual(actual, expected[0].get("href"))

    def test_multiple_get_links(self):
        """ This will ensure that get links will
        return a list of multiple md links """
        expected = ["www.link.com", "./link"]
        result = get_links("this is a [link](www.link.com) and [link](./link)")

        for index, link in enumerate(result):
            self.assertEqual(link.get("href"), expected[index])

    def test_is_absolute_url(self):
        """This will return a test to see if the link is a valid url format"""
        self.assertTrue(is_absolute_url(urlparse("http://www.fake.g00gl3.com")))
        self.assertTrue(is_absolute_url(urlparse("http://www.google.com")))
        self.assertFalse(is_absolute_url(urlparse("www.google.com")))
        self.assertFalse(is_absolute_url(urlparse(".sync.py")))
        self.assertFalse(is_absolute_url(urlparse("#fragment")))

    def test_transform_link(self):
        base_path = './test-content'
        rewrite_path = '/docs/foo'
        rewrite_url = 'https://foo.bar'
        local_files = {
            'test-content/content.md': ('_index.md', ''),
            'test-content/test.txt': ('test.txt', ''),
            'another-content/test.md': ('test.md', 'another'),
            'test-content/nested/content.md': ('content.md', 'nested'),
            'test-content/nested/example.yaml': ('example.yaml', 'nested')
        }

        cases = [
            "",
            "http://test.com",
            "test.txt",
            "content.md",
            "notthere.txt",
            "../another-content/test.md",
            "./nested/content.md",
            "./nested/example.yaml"
        ]

        expected_results = [
            "",
            "http://test.com",
            "/docs/foo/test.txt",
            "/docs/foo/",
            "https://foo.bar/test-content/notthere.txt",
            "/docs/foo/another/test/",
            "/docs/foo/nested/content/",
            "/docs/foo/nested/example.yaml"
        ]

        for case, expected in zip(cases, expected_results):
            self.assertEqual(
                transform_link(case, base_path, local_files, rewrite_path, rewrite_url),
                expected)

    def test_transform_links_doc(self):
        self.maxDiff = None

        # Links are in a page stored undrer base_path
        base_path = 'test-content'

        # The following pages are synced
        local_files = {
            f'{base_path}/content.md': '_index.md',
            f'{base_path}/else.md': 'else.md',
            f'{base_path}/test.txt': 'test.txt',
            'some_other_folder/with_contend.md': 'with_contend.md'
        }

        cases = [
            "[exists-relative-link](./test.txt)",
            "[exists-relative-link-index](./content.md)",
            "[exists-relative-link-index](./else.md)",
            "[exists-relative-link-other-path](../some_other_folder/with_content.md)",
            "[exists-relative-link-fragment](test.txt#Fragment)",
            "[notfound-relative-link](./this/is/not/found.txt#FraGment)",
            "[notfound-relative-link-fragment](./this/is/not/found.md#fraGmenT)",
            "[notfound-relative-link-dotdot](../examples/notfound.txt)",
            "[invalid-absolute-link](www.github.com)",
            ("[valid-absolute-link](https://website-random321.net#FRagment) "
             "[valid-ref-link](#fooTEr)"),
            ("Valid link broken on two lines [exists-link-in-list]("
            "./test.txt)")
        ]
        expected_results = [
            "[exists-relative-link](/docs/test/test.txt)",
            "[exists-relative-link-index](/docs/test/)",
            "[exists-relative-link-index](/docs/test/else/)",
            "[exists-relative-link-other-path](/docs/test/else/)",
            "[exists-relative-link-fragment](/docs/test/test.txt#Fragment)",
            "[notfound-relative-link](http://test.com/tree/docs/test/this/is/not/found.txt#FraGment)",
            "[notfound-relative-link-fragment](http://test.com/tree/docs/test/this/is/not/found.md#fraGmenT)",
            "[notfound-relative-link-dotdot](http://test.com/tree/docs/examples/notfound.txt)",
            "[invalid-absolute-link](http://test.com/tree/docs/www.github.com)",
            ("[valid-absolute-link](https://website-random321.net#FRagment) "
             "[valid-ref-link](#footer)"),
            ("Valid link broken on two lines [exists-link-in-list]("
            "/docs/test/test.txt)")
        ]

        for case, expected in zip(cases, expected_results):
            actual = transform_links_doc(
                text=case, base_path=base_path, local_files=local_files,
                rewrite_path='/docs/test', rewrite_url='http://test.com/tree/docs/test'
            )

    def test_read_front_matter(self):
        cases = [
            'abc',
            '---\ntest1',
            '---\ntest1: abc\ntest2: 1\n---\nabc',
            '<!--\n---\ntest1: abc\ntest2: 1\n---\n-->\nabc'
        ]
        expected = [
            ('abc', None),
            ('---\ntest1', None),
            ('abc', {"test1": "abc", "test2": 1}),
            ('abc', {"test1": "abc", "test2": 1})
        ]
        for case, exp in zip(cases, expected):
            actual = read_front_matter(case)
            self.assertEqual(actual, exp)

    def test_transform_doc(self):
        header = dict(test1='abc', test2=1, test3=True)
        with tempfile.TemporaryDirectory() as site_dir:
            expected_result = os.path.join(site_dir, 'target', 'target.md')
            expected_content = (
                "---\n"
                "test1: abc\n"
                "test2: 1\n"
                "test3: true\n"
                "---\n"
            )
            actual_result = transform_doc(
                self.doc, 'test-content', 'target.md', 'target', header, {},
                '/doc/test', 'http://test.com/test/tree', site_dir)
            self.assertEqual(actual_result, expected_result)

            with open(expected_result, 'r') as result:
                actual_content = result.read()
                self.assertEqual(actual_content, expected_content)

    def test_transform_docs(self):
        folders_config = {
            'test-content': {
                'index': 'content.md',
                'target': 'target',
                'include': ['*.md', '*.txt'],
                'exclude': ['unwanted.txt'],
                'header': {
                    'test1': 'abc'
                }
            }
        }
        with tempfile.TemporaryDirectory() as site_dir:
            expected_results = [
                os.path.join(site_dir, 'target', '_index.md'),
                os.path.join(site_dir, 'target', 'test.txt')]

            template = (
                "---\n"
                "test1: abc\n"
                "weight: {weight}\n"
                "---\n"
            )
            expected_contents = [template.format(weight=idx) for idx in range(2)]
            actual_results = transform_docs(
                self.gitrepo, self.tagname, folders_config, site_dir,
                '/doc/test', 'http://test.com/test/tree')
            self.assertEqual(set(actual_results), set(expected_results))

            for result, content in zip(expected_results, expected_contents):
                with open(result, 'r') as result:
                    actual_content = result.read()
                    self.assertEqual(actual_content, content)

    @mock.patch('sync.transform_docs')
    def test_download_resources_to_project(self, transform_docs_mock):
        folders_config = {
            'test-content': {
                'index': 'content.md',
                'target': 'target',
                'include': ['*.md', '*.txt'],
                'exclude': ['unwanted.txt'],
                'header': {
                    'test1': 'abc'
                }
            }
        }
        test_component = {
            'component': 'test',
            'repository': 'http://test.com/test',
            'docDirectory': 'docs',
            'tags': [{
                'name': self.tagname,
                'displayName': self.tagname,
                'folders': folders_config
            }]
        }
        clones = {'http://test.com/test': self.gitrepo}
        sync.download_resources_to_project([test_component], clones)
        transform_docs_mock.assert_called_once_with(
            git_repo=self.gitrepo,
            tag=self.tagname,
            folders=folders_config,
            site_folder=f'{sync.CONTENT_DIR}/test',
            base_path='/docs/test',
            base_url=f'http://test.com/test/tree/{self.tagname}/')


if __name__ == '__main__':
    unittest.main()
