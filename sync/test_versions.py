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

import copy
import os
import tempfile
import unittest

from click.testing import CliRunner
from ruamel.yaml import YAML

import versions

test_config_string = """
# This is a test config
component: test
repository: https://foo.bar/org/test
archive: https://foo.bar/tags
tags:
- name: foo
  displayName: foo
  folders:
    docs:
        include: ['*']
- name: bar
  displayName: bar
  folders:
    docs:
        include: ['*']
"""

test_config2_string = """
# This is a test config
component: test2
repository: https://foo.bar/org/test2
archive: https://foo.bar/tags2
tags:
- name: foo
  displayName: foo
  folders:
    docs:
        include: ['*']
"""

test_config_string_new = """
# This is a test config
component: test
repository: https://foo.bar/org/test
archive: https://foo.bar/tags
tags:
- name: new
  displayName: new
  folders:
    docs:
        include: ['*']
- name: foo
  displayName: foo
  folders:
    docs:
        include: ['*']
- name: bar
  displayName: bar
  folders:
    docs:
        include: ['*']
"""

yaml = YAML()
test_config = {
    'filename': 'test.yaml',
    'content': yaml.load(test_config_string)
}
test_config_new = {
    'filename': 'test.yaml',
    'content': yaml.load(test_config_string_new)
}
test_config2 = {
    'filename': 'test.yaml',
    'content': yaml.load(test_config2_string)
}
test_configs = [test_config, test_config2]


class TestVersions(unittest.TestCase):

    def test_select_config(self):
        expected = test_config
        actual = versions.select_config(test_configs, 'test')
        self.assertEqual(actual, expected)

    def test_select_config_missing(self):
        actual = versions.select_config(test_configs, 'missing')
        self.assertIsNone(actual)

    def test_add_version(self):
        self.maxDiff = None
        expected = test_config_new
        actual = versions.add_version(copy.deepcopy(test_config), 'new')
        self.assertEqual(actual, expected)

    def test_rm_version(self):
        self.maxDiff = None
        expected = test_config
        actual = versions.rm_version(copy.deepcopy(test_config_new), 'new')
        self.assertEqual(actual, expected)

    def test_rm_version_missing(self):
        version = 'missing'
        self.assertRaisesRegex(
            versions.VersionNotFoundError, f'Version {version} not found in',
            versions.rm_version, test_config, version)

    def test_add_remove(self):
        self.maxDiff = None
        config_filename = 'test.yaml'
        expected_after_add = test_config_new['content']
        expected_after_rm = test_config['content']
        runner = CliRunner()

        # write to config file
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(os.path.join(tmpdirname, config_filename), 'w+') as config_file:
                config_file.write(test_config_string)

            # Test adding a version
            runner.invoke(versions.versions, ['add', 'new',
                                     '--config-folder', tmpdirname,
                                     '--project', 'test'])
            # read the result
            with open(os.path.join(tmpdirname, config_filename), 'r') as result:
                actual = yaml.load(result.read())

            self.assertEqual(actual, expected_after_add)

            # Test removing a version
            runner.invoke(versions.versions, ['rm', 'new',
                                     '--config-folder', tmpdirname,
                                     '--project', 'test'])
            # read the result
            with open(os.path.join(tmpdirname, config_filename), 'r') as result:
                actual = yaml.load(result.read())

            self.assertEqual(actual, expected_after_rm)
