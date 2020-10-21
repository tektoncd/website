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

from sync import get_links
from sync import transform_text
from sync import is_url
from sync import is_ref
from sync import remove_ending_forward_slash
from sync import get_tags
from sync import download_files
from sync import load_config
from sync import save_config
from sync import get_files


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

    def test_multiple_get_links(self):
        """ This will ensure that get links will
        return a list of multiple md links """
        expected = ["www.link.com", "./link"]
        result = get_links("this is a [link](www.link.com) and [link](./link)")

        for index, link in enumerate(result):
            self.assertEqual(link.get("href"), expected[index])

    def test_is_ref(self):
        """ Verify if a string is a reference. A reference is
        defined as  a string where its first character is a hashtag """
        self.assertEqual(is_ref(""), False)
        self.assertEqual(is_ref("#footer"), True)
        self.assertEqual(is_ref("www.google.com"), False)

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

    def test_is_url(self):
        """This will return a test to see if the link is a valid url format"""
        expected = is_url("http://www.fake.g00gl3.com")
        self.assertEqual(True, expected)

        expected = is_url("http://www.google.com")
        self.assertEqual(True, expected)

        expected = is_url("http://www.github.com")
        self.assertEqual(True, expected)

        expected = is_url("./sync.py")
        self.assertEqual(False, expected)

        expected = is_url("www.github.com")
        self.assertEqual(False, expected)

    def test_transform_text(self):
        """Ensure that transform links will turns links to
        relative github link or existing file name"""

        expected = """
        [invalid-relative-link](test.com/./adw/a/d/awdrelative)
        [valid-relative-link](./sync.py)
        [valid-absolute-link](www.github.com)
        [invalid-absolute-link](https://website-invalid-random321.net)
        [valid-ref-link](#footer)
        """
        text = """
        [invalid-relative-link](./adw/a/d/awdrelative)
        [valid-relative-link](./sync.py)
        [valid-absolute-link](www.github.com)
        [invalid-absolute-link](https://website-invalid-random321.net)
        [valid-ref-link](#footer)
        """

        actual = None
        tmp_name = None

        # write to file
        with tempfile.NamedTemporaryFile(dir='/tmp', delete=False) as tmp:
            tmp_name = tmp.name
            name = self.path_leaf(tmp_name)
            tmp.write(text.strip().encode())

        # mutate file
        transform_text("", "/tmp", {name: name}, "test.com")
        # read and delete file
        actual = self.read_and_delete_file(tmp_name)

        self.assertEqual(actual.strip(), expected.strip())


if __name__ == '__main__':
    unittest.main()
