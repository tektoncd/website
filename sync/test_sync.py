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

import unittest
import tempfile
import shutil
import ntpath
import os
from shutil import copytree
from urllib.parse import urlparse

from sync import (
    get_links, transform_text, is_absolute_url,
    is_fragment, remove_ending_forward_slash,
    get_tags, download_files, load_config, save_config,
    get_files, transform_link)


class TestSync(unittest.TestCase):

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
    def test_is_fragment(self):
        """ Verify if a string is a reference. A reference is
        defined as  a string where its first character is a hashtag """
        self.assertFalse(is_fragment(urlparse("")))
        self.assertTrue(is_fragment(urlparse("#footer")))
        self.assertFalse(is_fragment(urlparse("www.google.com")))

    def test_remove_ending_forward_slash(self):
        """ Remove a slash if it is the last character in a string """
        actual = remove_ending_forward_slash("www.google.com/")
        expected = "www.google.com"
        self.assertEqual(actual, expected)

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

    def test_download_files(self):
        """ Download file to tmp directory if url is valid """
        expected = True
        dirpath = tempfile.mkdtemp()
        actual = download_files(
            "https://raw.githubusercontent.com/tektoncd/pipeline/master",
            dirpath,
            {"README.md": "README.md"}
        )
        shutil.rmtree(dirpath)
        self.assertEqual(actual, expected)

        dirpath = tempfile.mkdtemp()
        self.assertRaises(
            Exception,
            download_files,
            "http://fake.c0m",
            dirpath,
            [{"test": "test"}]
        )
        shutil.rmtree(dirpath)

    def test_load_save_config(self):
        """ convert a list of files into a list of dictionaries """
        # create a tmp file with yaml txt
        text = "{displayOrder: 1}"
        actual = None
        tmp_name = None

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

    def test_get_files(self):
        """ create a list of files within a
        directory that contain a valid extension"""
        expected = None
        actual = None

        with tempfile.NamedTemporaryFile(dir='/tmp', delete=True) as tmp:
            expected = [tmp.name]
            actual = get_files("/tmp", self.path_leaf(tmp.name))

        self.assertEqual(actual, expected)

        with tempfile.NamedTemporaryFile(dir='/tmp', delete=True) as tmp:
            expected = [tmp.name]
            actual = get_files("/tmp", self.path_leaf(tmp.name))

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
        self.assertEqual(
            transform_link("", base_path, rewrite_path, rewrite_url), "")
        self.assertEqual(
            transform_link("http://test.com", base_path, rewrite_path, rewrite_url),
            "http://test.com")
        self.assertEqual(
            transform_link("test.txt", base_path, rewrite_path, rewrite_url),
            "/docs/foo/test.txt")
        self.assertEqual(
            transform_link("content.md", base_path, rewrite_path, rewrite_url),
            "/docs/foo/content/")
        self.assertEqual(
            transform_link("notthere.txt", base_path, rewrite_path, rewrite_url),
            "https://foo.bar/notthere.txt")

    def test_transform_text(self):
        """Ensure that transform links will turns links to
        relative github link or existing file name"""
        self.maxDiff = None

        expected = (
            "[exists-relative-link](test-content/test.txt)\n"
            "[exists-relative-link](test-content/content/)\n"
            "[exists-relative-link-fragment](test-content/test.txt#Fragment)\n"
            "[notfound-relative-link](http://test.com/tree/docs/this/is/not/found.txt#FraGment)\n"
            "[notfound-relative-link-fragment](http://test.com/tree/docs/this/is/not/found.md#fraGmenT)\n"
            "[notfound-relative-link-dotdot](http://test.com/tree/examples/notfound.txt)\n"
            "[invalid-absolute-link](http://test.com/tree/docs/www.github.com)\n"
            "[valid-absolute-link](https://website-random321.net#FRagment) "
            "[valid-ref-link](#footer)"
        )
        text = (
            "[exists-relative-link](./test.txt)\n"
            "[exists-relative-link](./content.md)\n"
            "[exists-relative-link-fragment](test.txt#Fragment)\n"
            "[notfound-relative-link](./this/is/not/found.txt#FraGment)\n"
            "[notfound-relative-link-fragment](./this/is/not/found.md#fraGmenT)\n"
            "[notfound-relative-link-dotdot](../examples/notfound.txt)\n"
            "[invalid-absolute-link](www.github.com)\n"
            "[valid-absolute-link](https://website-random321.net#FRagment) "
            "[valid-ref-link](#fooTEr)"
        )

        content_file = "content.md"

        # write to file
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(os.path.join(tmpdirname, content_file), 'w+') as content:
                content.write(text.strip())
            with open(os.path.join(tmpdirname, 'test.txt'), 'w+') as test:
                test.write(text.strip())

            # mutate file
            transform_text(folder=tmpdirname,
                           files={content_file: content_file},
                           base_path="test-content",
                           base_url="http://test.com/tree/docs/")
            # read the result
            actual = ""
            with open(os.path.join(tmpdirname, content_file), 'r') as result:
                actual = result.read()

            self.assertEqual(actual.strip(), expected.strip())


if __name__ == '__main__':
    unittest.main()
