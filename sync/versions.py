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
import logging
import sys

from absl import app
from absl import flags

import sync

FLAGS = flags.FLAGS

flags.DEFINE_string(
    'project', 'pipeline', 'Name of the component', short_name='p')
flags.DEFINE_string(
    'version', None, 'Version of the component', short_name='r')

def add_version(config, component, version):
    """ add a new version for the component in the config """
    updated = False
    for idx, c in enumerate(config):
        if c['content']['repository'].endswith(f'/{component}'):
            updated = True
            tags = c['content']['tags']
            new_tag = copy.deepcopy(tags[0])
            new_tag['name'] = version
            new_tag['displayName'] = version
            config[idx]['content']['tags'] = [new_tag]
            config[idx]['content']['tags'].extend(tags)
    return config, updated


def main(argv):
    """ add a new version to a component """
    # load the configs
    config_files = sync.get_files(f'{FLAGS.config}', ".yaml")
    config = sync.load_config(config_files)
    # add a version to the config
    new_config, updated = add_version(config, FLAGS.project, FLAGS.version)
    if updated:
        sync.save_config(new_config)
    else:
        logging.error(f'Could not find any config file for {FLAGS.project} to update')
        sys.exit(1)


if __name__ == '__main__':
    app.run(main)
