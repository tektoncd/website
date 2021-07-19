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

import copy
import fnmatch
import json
import logging
import markdown
from multiprocessing import Pool
import os
import os.path
import re
import sys
from urllib.error import URLError
from urllib.parse import urlparse, urljoin, urlunparse

from bs4 import BeautifulSoup
import click
import git
from jinja2 import Environment
from jinja2 import FileSystemLoader
from ruamel.yaml import YAML


CONTENT_DIR = './content/en/docs'
VAULT_DIR = './content/en/vault'
JS_ASSET_DIR = './assets/js'
TEMPLATE_DIR = './templates'

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FOLDER = os.path.join(BASE_FOLDER, 'config')
DEFAULT_CACHE_FOLDER = os.path.join(BASE_FOLDER, '.cache')

jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

FM_BOUNDARY = re.compile(r"^(?:<!--\n)?-{3,}\s*$(?:\n-->)?", re.MULTILINE)
YAML_SEPARATOR = "---\n"

FOLDER_INDEX = '_index.md'


def doc_config(doc, folder_config, weight=None):
    """ Return the target name, folder and header for doc based on folder_config

    :param doc: the doc as a gitpython Blob
    :param folder_config: a dict with the configuration of the folder the doc
      was found in, as specified in the sync config file under `folders`
    :params weight: optional weight of the doc. When specified it's set in the
      returned header dict
    :returns: a tuple (target_filename, target_folder, header), which describes
      which files `doc` should be written to, in which folder, with which header
    """

    index_file = folder_config.get('index', FOLDER_INDEX)
    target_folder = folder_config.get('target', '')
    # If the doc name is configured as index, rewrite it to FOLDER_INDEX
    target_filename = FOLDER_INDEX if doc.name == index_file else doc.name
    # If an header is specified, build it an return it
    header_dict = None
    if 'header' in folder_config:
        header_dict = copy.deepcopy(folder_config['header'])
        if weight is not None:
            header_dict['weight'] = weight
    return target_filename, target_folder, header_dict


def docs_from_tree(tree, include=['*'], exclude=[]):
    """ Get matching docs (git blobs) from a git tree

    Filter all blobs directly under a tree based on include and
    exclude lists. Filters are specified as list of unix style
    filename pattern:
    (https://docs.python.org/3/library/fnmatch.html) """
    return filter(lambda b:
            any(fnmatch.fnmatch(b.name, i) for i in include) and
            not any(fnmatch.fnmatch(b.name, e) for e in exclude), tree.blobs)


def transform_docs(git_repo, tag, folders, site_folder, base_path, base_url):
    """ Transform all folders configured for a tag

    :param git_repo: a gitpython Repo object, that points to the source git repo
    :param tag: a string that represent the git tag to be used
    :param folders: a list of folder names with a dict config each, loaded from
      sync config file
    :param site_folder: the root folder on disk where files shall be written to
    :param base_path: used to rewrite relative links to sync'ed files
    :param base_url: used to rewrite relative links to unknown files
    """

    # Get the root tree for the requested version from the repo
    try:
        tag = next(x for x in git_repo.tags if x.name == tag)
    except StopIteration:
        # When no tag is found try to match a branch (references)
        try:
            tag = next(x for x in git_repo.references if x.name == tag)
        except StopIteration:
            logging.error(f'No tag {tag} found in {git_repo}')
            sys.exit(1)

    # List all relevant blobs based on the folder config
    files = []
    for folder, folder_config in folders.items():
        root = tag.commit.tree.join(folder)
        docs = docs_from_tree(
            tree=root, include=folder_config.get('include', ['*']),
            exclude=folder_config.get('exclude', []))
        # zip doc, folder, targer and header so we can process them in parallel later
        files.extend([(doc, folder, *doc_config(doc, folder_config, idx))
            for idx, doc in enumerate(docs)])

    # Build a dict of all valid local links
    # This is used by `transfor_line` to identify local links
    local_files = {doc.path: (target, target_folder) for
                    doc, _, target, target_folder, _ in files}

    # Build a list of tuple of `transform_doc` parameters
    tranform_args = [
        (*f, local_files, base_path, base_url, site_folder) for f in files]

    with Pool() as pool:
        results = pool.starmap(transform_doc, tranform_args)

    # Return the list of files transformed
    return results


def safe_makedirs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except FileExistsError:
        pass


def transform_doc(doc, source_folder, target, target_folder, header,
                  local_files, base_path, base_url, site_folder):
    """ Transform a single doc to the target file

    Read a doc (git blob), transform links in it
    and writes the results in to a target file

    :param doc: The source doc as gitpython Blob
    :param source_folder: the name of the folder in the source repo where
    the file comes from
    :param target: the name of the file the transformed doc shall be written to
    :param target_folder: the folder within `site_folder` where the transformed
      doc shall be written to
    :param header: a dict with the content of a header (if any) to be prepended
      in the transformed doc
    :param local_files: a dict source file -> target used to rewrite
        relative links to sync'ed files
    :param base_path: used to rewrite relative links to sync'ed files
    :param base_url: used to rewrite relative links to unknown files
    :param site_folder: the root folder on disk where files shall be written to
    """
    # Some machines seem to use text/plain (e.g. running on a mac) and some use
    # text/markdown (e.g. running in a fresh ubuntu container)
    if doc.mime_type != 'text/plain' and doc.mime_type != 'text/markdown':
        logging.error(f'Cannot process {doc.mime_type} file {doc.path}')
        sys.exit(1)
    site_target_folder = os.path.normpath(os.path.join(site_folder, target_folder))
    safe_makedirs(site_target_folder)
    target = os.path.join(site_target_folder, target)
    with open(target, 'w+') as target_doc:
        # If there is an header configured, write it (in YAML)
        doc_all = decode(doc.data_stream.read())
        doc_markdown, fm = read_front_matter(doc_all)
        # Update the doc front matter with the configured one and write it
        write_front_matter(target_doc, fm, header)
        doc_markdown = transform_links_doc(
            doc_markdown, source_folder, local_files, base_path, base_url)
        target_doc.write(doc_markdown)
    return target


def decode(s, encodings=('utf8', 'latin1', 'ascii')):
    for encoding in encodings:
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            pass
    return s.decode('ascii', 'ignore')


def read_front_matter(text):
    """ returns a tuple text, frontmatter (as dict) """
    if FM_BOUNDARY.match(text):
        try:
            _, fm, content = FM_BOUNDARY.split(text, 2)
        except ValueError:
            # Not enough values to unpack, boundary was matched once
            return text, None
        if content.startswith('\n'):
            content = content[1:]
        return content, YAML().load(fm)
    else:
        return text, None

def write_front_matter(target_doc, fm_doc, fm_config):
    fm_doc = fm_doc or {}
    fm_config = fm_config or {}
    fm_doc.update(fm_config)
    if fm_doc:
        target_doc.write(YAML_SEPARATOR)
        YAML().dump(fm_doc, target_doc)
        target_doc.write(YAML_SEPARATOR)

def transform_links_doc(text, base_path, local_files, rewrite_path, rewrite_url):
    """ transform all the links the text """
    links = get_links(text)
    # Rewrite map, only use links with an href
    rewrite_map = {x.get("href"): transform_link(x.get("href"), base_path, local_files, rewrite_path, rewrite_url)
        for x in links if x.get("href")}
    for source, target in rewrite_map.items():
        text = text.replace(source, target)
    return text


def get_links(md):
    """ return a list of all the links in a string formatted in markdown """
    md = markdown.markdown(md)
    soup = BeautifulSoup(md, 'html.parser')
    return soup.find_all("a")


def transform_link(link, base_path, local_files, rewrite_path, rewrite_url):
    """ Transform hrefs to be valid URLs on the web-site

    Relative URLs are rewritten to `rewrite_path` when `link`
    points to a sync'ed file. Else they're rewritten to `rewrite_url`.
    Absolute URLs are not changed (they may be external)
    Fragments are relative to the page and do not need changes,
    except for lower() on local files because hugo generated
    anchors are always lower case.
    :param link: the link to be re-written
    :param base_path: the folder where the source document that contains
      the link lives
    :param local_files: a dict source file -> (target file, folder) that
      maps sync'ed files from their fully qualified source name into their
      filename in the site folder
    :param rewrite_path: the file local (sync'ed) files are rewritten to
    :param rewrite_url: the URL remote files are rewritten to

    :note: urlparse treats URLs without scheme like path only URLs,
      so 'github.com' will be rewritten to 'rewrite_url/github.com'
    """
    # ignore empty links
    if not link:
        return link
    # urlparse returns a named tuple
    parsed = urlparse(link)
    if is_absolute_url(parsed):
        return link
    if is_fragment(parsed):
        # A fragment only link points to an .md file
        return urlunparse(parsed._replace(fragment=parsed.fragment.lower()))
    path = os.path.normpath(parsed.path)

    # The list if local_file includes paths based on the root of the git
    # repo, so we need join base_path and normalize to fq_path to find the
    # link in the list of local files
    fq_path = os.path.normpath(os.path.join(base_path, parsed.path))
    if fq_path in local_files:
        target_file = local_files[fq_path][0]
        target_folder = local_files[fq_path][1]
        is_index = (target_file == FOLDER_INDEX)
        filename, ext = os.path.splitext(target_file)
        # Special handling for md files
        if ext == '.md':
            # Links to the index file are rendered as base_path/
            if is_index:
                target_file = ''
            # links to md other files are rendered as .../[md filename]/
            else:
                target_file = filename + '/'
            # for .md files, lower the case of fragments to match hugo's behaviour
            parsed = parsed._replace(fragment=parsed.fragment.lower())
        if target_folder:
            new_path = [rewrite_path, target_folder, target_file]
        else:
            new_path = [rewrite_path, target_file]
        return parsed._replace(path="/".join(new_path)).geturl()
    # when not found on disk, append to the base_url
    return urljoin(rewrite_url, parsed._replace(path=fq_path).geturl())


def is_absolute_url(parsed_url):
    """ check if it is an absolute url """
    return all([parsed_url.scheme, parsed_url.netloc])


def is_fragment(parsed_url):
    """ determine if the url is an a link """
    return len(parsed_url.fragment) > 0 and not any(parsed_url[:-1])


def download_resources_to_project(yaml_list, clones):
    """ download the files from local clones based on a spec.
    The YAML sync spec can be found in sync/config/README.md """
    for entry in yaml_list:
        component = entry['component']
        repository = entry['repository']
        local_clone = clones.get(repository)
        if not local_clone:
            logging.error(f'No git clone found for {repository} in {clones}')
            sys.exit(1)

        for index, tag in enumerate(entry['tags']):
            logging.info(f'Syncing {component}@{tag["name"]}')
            link_base_url = f'{repository}/tree/{tag["name"]}/'
            if index == 0:
                # first links belongs on the home page
                base_path = f'/docs/{component}'.lower()
                site_dir = f'{CONTENT_DIR}/{component}'
                os.makedirs(site_dir, exist_ok=True)
            else:
                # the other links belong in the other versions a.k.a vault
                base_path = f'/vault/{component}-{tag["displayName"]}'
                site_dir = f'{VAULT_DIR}/{component}-{tag["displayName"]}'
                os.makedirs(site_dir, exist_ok=True)

            results = transform_docs(
                git_repo=local_clone,
                tag=tag['name'],
                folders=tag['folders'],
                site_folder=site_dir,
                base_path=base_path,
                base_url=link_base_url)
            logging.debug(f'Finished syncing {component}@{tag["name"]}: ')
            logging.debug(f'{results}')


def get_files_in_path(path, file_type):
    """ return a list of all the files in path that match the file_type """
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
        with open(c['filename'], 'w') as out:
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


def clone_repo(repo, update):
    project = repo.split('/')[-1]
    clone_dir = os.path.join(DEFAULT_CACHE_FOLDER, project)

    if os.path.isdir(clone_dir):
        if not update:
            print(f'{project}: Cache folder {clone_dir} found, skipping clone.')
            return repo, git.Repo(clone_dir)
        # Cleanup and update via fetch --all
        print(f'{project}: updating started')
        cloned_repo = git.Repo(clone_dir)
        cloned_repo.git.reset('--hard')
        cloned_repo.git.clean('-xdf')
        cloned_repo.git.fetch('--all')
        print(f'{project}: updating completed')
        return repo, cloned_repo

    # Clone the repo
    print(f'{project}: cloning started')
    cloned_repo = git.Repo.clone_from(repo, clone_dir)
    print(f'{project}: cloning completed')
    return repo, cloned_repo


def clone_repos(sync_configs, update):
    # Make sure the cache folder exists
    safe_makedirs(DEFAULT_CACHE_FOLDER)

    with Pool() as pool:
        results = pool.starmap(clone_repo, [(x['repository'], update) for x in sync_configs])
    return {x: y for x, y in results}


@click.command()
@click.option('--config-folder', default=DEFAULT_CONFIG_FOLDER,
              help='the folder that contains the config files')
@click.option('--update-cache/--no-update-cache', default=False,
              help='update clone caches. !! This will force cleanup caches !!')
def sync(config_folder, update_cache):
    """ fetch all the files and sync it to the website """
    # get the path of the urls needed
    config_files = get_files_in_path(config_folder, ".yaml")
    config = [x["content"] for x in load_config(config_files)]
    # clone all relevant repos
    clones = clone_repos(config, update_cache)
    # download resources from the clone cache
    download_resources_to_project(config, clones)
    versions = get_versions(config)
    # create version switcher script
    create_resource(JS_ASSET_DIR, "version-switcher.js", versions)
    # create index for vault
    create_resource(VAULT_DIR, FOLDER_INDEX, versions)


if __name__ == '__main__':
    sync()
