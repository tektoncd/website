#!/usr/bin/env python

# Copyright 2020-2026 The Tekton Authors
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
import os
import sys

import click

import sync

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'config')

class ConfigNotFoundError(Exception):
    pass

class VersionNotFoundError(Exception):
    pass


@click.group()
def versions():
    pass


@versions.command()
@click.option('--config-folder', default=DEFAULT_CONFIG_FOLDER,
              help='the folder that contains the config files')
@click.option('--project', required=True,
              help='the tekton project name')
@click.argument('version')
def add(config_folder, project, version):
    """ add a new version in the config for the specified project """
    command(add_version, config_folder, project, version)


@versions.command()
@click.option('--config-folder', default=DEFAULT_CONFIG_FOLDER,
              help='the folder that contains the config files')
@click.option('--project', required=True,
              help='the tekton project name')
@click.argument('version')
def rm(config_folder, project, version):
    """ remove a version from the config for the specified project """
    command(rm_version, config_folder, project, version)


def command(cmd_fn, config_folder, project, version):
    configs = load_config(config_folder)
    config = select_config(configs, project)
    if not config:
        raise ConfigNotFoundError(f'Cound not find a config for {project} in {configs}')
    try:
        cmd_fn(config, version)
        sync.save_config(configs)
    except VersionNotFoundError as e:
        logger.error(f'Could not update config for {project}: {e}')
        sys.exit(1)


def select_config(configs, project):
    """ returns the first config that matches the project """
    for c in configs:
        if c['content']['repository'].endswith(f'/{project}'):
            return c
    return None


def add_version(config, version):
    tags = config['content']['tags']
    new_tag = copy.deepcopy(tags[0])
    new_tag['name'] = version
    new_tag['displayName'] = version
    config['content']['tags'] = [new_tag]
    config['content']['tags'].extend(tags)
    return config


def rm_version(config, version):
    for idx, tag in enumerate(config['content']['tags']):
        logger.info(f'{idx}, {tag}')
        if version == tag['name']:
            del config['content']['tags'][idx]
            return config
    raise VersionNotFoundError(f'Version {version} not found in {config}')


def load_config(config_folder):
    """ wrapper around sync.load_config that takes an input folder """
    config_files = sync.get_files_in_path(config_folder, ".yaml")
    return sync.load_config(config_files)


if __name__ == '__main__':
    versions()
