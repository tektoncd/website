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

from ruamel.yaml import YAML

import versions

test_config_string = """
# This is a test config
component: test
displayOrder: 0
repository: https://foo.bar/org/test
docDirectory: docs
archive: https://foo.bar/tags
tags:
- name: foo
  displayName: foo
  files:
    FOO.md: _index.md
    bar.md: bar.md
- name: bar
  displayName: bar
  files:
    FOO.md: _index.md
    bar.md: bar.md
"""

test_config_string_new = """
# This is a test config
component: test
displayOrder: 0
repository: https://foo.bar/org/test
docDirectory: docs
archive: https://foo.bar/tags
tags:
- name: new
  displayName: new
  files:
    FOO.md: _index.md
    bar.md: bar.md
- name: foo
  displayName: foo
  files:
    FOO.md: _index.md
    bar.md: bar.md
- name: bar
  displayName: bar
  files:
    FOO.md: _index.md
    bar.md: bar.md
"""

yaml = YAML()
test_config = [{
    'filename': 'foo.md',
    'content': yaml.load(test_config_string)
}]
test_config_new = [{
    'filename': 'foo.md',
    'content': yaml.load(test_config_string_new)
}]


class TestAddVersion(unittest.TestCase):

    def test_add_version(self):
        expected = test_config_new
        actual, updated = versions.add_version(test_config, 'test', 'new')
        self.assertTrue(updated)
        self.assertEqual(actual, expected)

    def test_add_version_missing_component(self):
        expected = test_config
        actual, updated = versions.add_version(test_config, 'missing', 'new')
        self.assertFalse(updated)
        self.assertEqual(actual, expected)

