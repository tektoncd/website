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

# This script helps synchronize contents from their respective sources of
# truth (usually GitHub repositories of each Tekton
# components, such as tektoncd/pipelines) to tektoncd/website.

import fileinput
import json
import logging
import markdown
from multiprocessing import Pool
import os
import os.path
from pathlib import Path
import shutil
from urllib.error import URLError
from urllib.parse import urlparse, urljoin, urlunparse
import wget

from absl import app
from absl import flags
from jinja2 import Environment
from jinja2 import FileSystemLoader
from lxml import etree
from ruamel.yaml import YAML


FLAGS = flags.FLAGS

# Flag names are globally defined!  So in general, we need to be
# careful to pick names that are unlikely to be used by other libraries.
# If there is a conflict, we'll get an error at import time.
flags.DEFINE_string(
    'config',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'),
    'Config directory', short_name='c')

CONTENT_DIR = './content/en/docs'
JS_ASSET_DIR = './assets/js'
TEMPLATE_DIR = './templates'
VAULT_DIR = './content/en/vault'
BUCKET_NAME = 'tekton-website-assets'

jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def transform_text(folder, files, base_path, base_url):
    """ change every link to point to a valid relative file or absolute url """
    files_in_folder = [f'{folder}/{f}' for f in files.values()]

    def process_file(file_in_folder):
        for line in fileinput.input(file_in_folder, inplace=1):
            # add a line of text to the payload
            # transform_links mutates text and set the lines provided
            print(transform_line(line, folder, base_path, base_url))

    for file_in_folder in files_in_folder:
        process_file(file_in_folder)


def transform_line(line, base_path, rewrite_path, rewrite_url):
    """ transform all the links in one line """
    line = line.rstrip()
    links = get_links(line)
    # If there are links in this line we may need to fix them
    for link in links:
        # link contains the text and href
        href =link.get("href")
        href_mod = transform_link(href, base_path, rewrite_path, rewrite_url)
        line = line.replace(href, href_mod)
    return line


def transform_link(link, base_path, rewrite_path, rewrite_url):
    """ Transform hrefs to be valid URLs on the web-site

    Absolute URLs are not changed (they may be external)
    Fragments are relative to the page and do not need changes
    Path only links should point to a file synced to the website
    but sometimes the file may be missing (if it's not in the sync
    configuration), so we follow this approach:
    - prefix with base_path and check for the file locally
    - if not found, prefix with base_url instead

    Note that urlparse treats URLs without scheme like path only
    URLs, so 'github.com' will be rewritten to base_url/github.com
    """
    # ignore empty links
    if not link:
        return link
    # urlparse returns a named tuple
    parsed = urlparse(link)
    if is_absolute_url(parsed) or is_fragment(parsed):
        return link
    path = os.path.normpath(parsed.path)
    if os.path.isfile(os.path.join(base_path, path)):
        filename, ext = os.path.splitext(path)
        # md files links are in the format .../[md filename]/
        if ext == '.md':
            path = filename + '/'
        return urlunparse(parsed._replace(path="/".join([rewrite_path, path])))
    # when not found on disk, append to the base_url
    return urljoin(rewrite_url, link)


def is_absolute_url(parsed_url):
    """ check if it is an absolute url """
    return all([parsed_url.scheme, parsed_url.netloc])


def is_fragment(parsed_url):
    """ determine if the url is an a link """
    return len(parsed_url.fragment) > 0 and not any(parsed_url[:-1])


def get_links(md):
    """ return a list of all the links in a string formatted in markdown """
    md = markdown.markdown(md)
    try:
        doc = etree.fromstring(md)
        return doc.xpath('//a')
    except etree.XMLSyntaxError:
        pass

    return []


def download_file(src_url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    logging.info(f'Downloading {src_url} to {dest_path}...\n')
    try:
        wget.download(src_url, out=dest_path, bar=None)
    except (FileExistsError, URLError):
        raise Exception(f'download failed for {src_url}')


def download_files(url_prefix, dest_prefix, files):
    """ download the file and create the
    correct folders that are necessary """
    if os.path.isdir(dest_prefix):
        shutil.rmtree(dest_prefix)
    os.mkdir(dest_prefix)
    download_args = [
        (f'{url_prefix}/{u}', f'{dest_prefix}/{f}')
        for u, f in files.items()]
    with Pool() as pool:
        pool.starmap(download_file, download_args)
    return True


def remove_ending_forward_slash(word):
    """ remove the last character if it is backslash """
    return word[:-1] if word.endswith('/') else word


def download_resources_to_project(yaml_list):
    """ download the files based on a certain spec.
    The YAML sync spec can be found in sync/config/README.md """
    for entry in yaml_list:
        component = entry['component']
        repository = remove_ending_forward_slash(entry['repository'])
        doc_directory = remove_ending_forward_slash(entry['docDirectory'])

        for index, tag in enumerate(entry['tags']):
            logging.info(f'Syncing {component}@{tag["name"]}')
            download_url = f'{repository}/raw/{tag["name"]}/{doc_directory}'
            link_base_url = f'{repository}/tree/{tag["name"]}/{doc_directory}/'
            if index == 0:
                # first links belongs on the home page
                download_dir = f'/docs/{component}'.lower()
                site_dir = f'{CONTENT_DIR}/{component}'
            else:
                # the other links belong in the other versions a.k.a vault
                download_dir = f'/vault/{component}-{tag["displayName"]}'
                site_dir = f'{VAULT_DIR}/{component}-{tag["displayName"]}'

            download_files(download_url, site_dir, tag["files"])
            transform_text(site_dir, tag["files"], download_dir, link_base_url)


def get_files(path, file_type):
    """ return a list of all the files with the correct type """
    file_list = []

    # walk through every file in directory and its sub directories
    for root, dirs, files in os.walk(path):
        for file in files:
            # append the file name to the list if is it the correct type
            if file.endswith(file_type):
                file_list.append(os.path.join(root, file))

    return file_list


def load_config(files):
    """ return a list of yaml files sorted based on a field called displayOrder """
    yaml = YAML()
    dic_list = []

    for file in files:
        with open(file, 'r') as text:
            # get the paths from the config file
            dic_list.append({
                "filename": file,
                "content": yaml.load(text)
            })

    dic_list.sort(key=lambda x: x['content']['displayOrder'])

    return dic_list


def save_config(config):
    """ save config files back to yaml """
    yaml = YAML()
    for c in config:
        out = Path(c['filename'])
        yaml.dump(c['content'], out)


def get_tags(sync_config):
    """ return a list of tags with, there name, and displayName """
    tags = []
    for tag in sync_config['tags']:
        tags.append({'name': tag['name'], 'displayName': tag['displayName']})
    return tags


def get_versions(sync_configs):
    """ return the list of all the versions and there tag, name, archive """
    component_versions = []
    for sync_config in sync_configs:
        component_versions.append({
            'name': sync_config['component'],
            'tags': get_tags(sync_config),
            'archive': sync_config['archive']
        })
    return component_versions


def create_resource(dest_prefix, file, versions):
    """ create site resource based on the version and file """
    resource_template = jinja_env.get_template(f'{file}.template')
    if file.endswith(".js"):
        serialize = json.dumps(versions)
        resource = resource_template.render(component_versions_json=serialize)
    elif file.endswith(".md"):
        resource = resource_template.render(component_versions=versions)
    else:
        logging.warning(f'Cannot create resource for {file}. Only .js and .md supported')
        return

    with open(f'{dest_prefix}/{file}', 'w') as f:
        f.write(resource)


def sync(argv):
    """ fetch all the files and sync it to the website """
    # get the path of the urls needed
    config_files = get_files(f'{FLAGS.config}', ".yaml")
    config = [x["content"] for x in load_config(config_files)]
    # download resources
    download_resources_to_project(config)
    versions = get_versions(config)
    # create version switcher script
    create_resource(JS_ASSET_DIR, "version-switcher.js", versions)
    # create index for vault
    create_resource(VAULT_DIR, "_index.md", versions)


if __name__ == '__main__':
    app.run(sync)
