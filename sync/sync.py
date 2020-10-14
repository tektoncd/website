# This script helps synchronize contents from their respective sources of
# truth (usually GitHub repositories of each Tekton
# components, such as tektoncd/pipelines) to tektoncd/website.

import json
import fileinput
import os
import re
import shutil
import markdown
import os.path
import wget
import logging
import yaml

from urllib.request import urlopen
from urllib.request import HTTPError
from urllib.request import URLError
from lxml import etree
from absl import app
from absl import flags
from jinja2 import Environment
from jinja2 import FileSystemLoader


FLAGS = flags.FLAGS

# Flag names are globally defined!  So in general, we need to be
# careful to pick names that are unlikely to be used by other libraries.
# If there is a conflict, we'll get an error at import time.
flags.DEFINE_string(
    'config',
    os.path.dirname(os.path.abspath(__file__)) + '/config',
    'Config directory', short_name='c')

CONTENT_DIR = './content/en/docs'
JS_ASSET_DIR = './assets/js'
TEMPLATE_DIR = './templates'
VAULT_DIR = './content/en/vault'
BUCKET_NAME = 'tekton-website-assets'

GCP_NETLIFY_ENV_CRED = os.environ.get('GCP_CREDENTIAL_JSON')
GCP_PROJECT = os.environ.get('GCP_PROJECT')

LINKS_RE = r'\[([^\]]*)\]\((?!.*://|/)([^)]*).md(#[^)]*)?\)'

jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def get_list_of_files(prefix, list_dic):
    """"get all the values from the key-value pairs and
    inserts them into a list with a prefix"""
    files = []

    for f in list_dic:
        for k in f:
            files.append(f'{prefix}/{f[k]}')

    return files


def transform_text(link_prefix, dest_prefix, files, url):
    """ change every link to point to a valid relative file or absolute url """

    logging.info(f'Running: transforming files in {dest_prefix}')
    payload = (url, link_prefix)
    list_of_files = get_list_of_files(dest_prefix, files)
    set_lines(list_of_files, payload, transform_links)
    logging.info(f'Completed: transformed files in {dest_prefix}')


def transform_links(line, url, link_prefix):
    line, is_transformed = sanitize_text(link_prefix, line)
    links = get_links(line)
    if is_transformed:
        for link in links:
            link = link.get("href")
            if not(os.path.isfile(link) or is_url(link) or is_ref(link)):
                line = line.replace(link, github_link(url, link))
    print(line)


def set_lines(files, payload, callback):
    """ get all the text from the files and replace
    each line of text with the list lines """
    for line in fileinput.input(files=(files), inplace=1):
        # add a line of text to the payload
        # Callback function will mutate text and set the lines provided
        callback(line, *payload)


def github_link(url, link):
    """ given a github raw link convert it to the main github link """
    return f'{url.replace("raw", "tree", 1)}/{link}'


def sanitize_text(link_prefix, text):
    """ santize every line of text to exclude relative
    links and to turn markdown file url's to html """
    old_line = text.rstrip()
    new_line = re.sub(LINKS_RE, r'[\1](' + link_prefix + r'\2\3)', old_line)
    return (new_line, old_line == new_line)


def is_url(url):
    """ check if it is a valid url """
    try:
        urlopen(url).read()
    except (HTTPError, URLError):
        return True
    except ValueError:
        return False

    return True


def is_ref(url):
    """ determine if the url is an a link """
    if len(url) <= 0:
        return False

    return url[0] == "#"


def get_links(md):
    """ return a list of all the links in a string formatted in markdown """
    md = markdown.markdown(md)
    try:
        doc = etree.fromstring(md)
        return doc.xpath('//a')
    except etree.XMLSyntaxError:
        pass

    return []


def download_files(url_prefix, dest_prefix, files):
    """ download the file and create the
    correct folders that are neccessary """
    if os.path.isdir(dest_prefix):
        shutil.rmtree(dest_prefix)
    os.mkdir(dest_prefix)
    for f in files:
        for k in f:
            src_url = f'{url_prefix}/{k}'
            dest_path = f'{dest_prefix}/{f[k]}'
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            logging.info(f'Downloading {src_url} to {dest_path}...\n')
            try:
                wget.download(src_url, out=dest_path)
            except (FileExistsError, URLError):
                raise Exception(f'download failed for {src_url}')
            logging.info('\n')

    return True


def remove_ending_forward_slash(word):
    """ remove the last character if it is backslash """
    return word[:-1] if word.endswith('/') else word


def get_file_dirs(entry, index, source_dir, dest_dir):
    """ return the files and there directories. Their relative and absolute
    counterpart is needed to download the files properly to the website """
    tag = entry['tags'][index]
    repository = remove_ending_forward_slash(entry['repository'])
    doc_directory = remove_ending_forward_slash(entry['docDirectory'])
    host_dir = f'{repository}/raw/{tag["name"]}/{doc_directory}'
    files = tag['files']

    return (host_dir, source_dir, dest_dir, files)


def download_resources_to_project(yaml_list):
    """ download the files based on a certain spec.
    The YAML sync spec can be found in sync/config/README.md """
    for entry in yaml_list:
        component = entry['component']

        for index, tag in enumerate(entry['tags']):
            if index == 0:
                # first links belongs on the home page
                download_dir = f'/docs/{component}/'
                site_dir = f'{CONTENT_DIR}/{component}'
            else:
                # the other links belong in the other versions a.k.a vault
                download_dir = f'/vault/{component}-{tag["displayName"]}/'
                site_dir = f'{VAULT_DIR}/{component}-{tag["displayName"]}'

            dirs = get_file_dirs(entry, index, download_dir, site_dir)

            host_dir, source_dir, dest_dir, files = dirs
            download_files(host_dir, dest_dir, files)
            transform_text(source_dir, dest_dir, files, host_dir)


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


def yaml_files_to_dic_list(files):
    """ return a list of yaml files to a sorted
     list based on a field called displayOrder """

    dic_list = []

    for file in files:
        with open(file, 'r') as text:
            # get the paths from the config file
            dic_list.append(yaml.load(text, Loader=yaml.FullLoader))

    dic_list.sort(key=lambda x: x['displayOrder'])

    return dic_list


def get_tags(list):
    """ return a list of tags with, there name, and displayName """
    tags = []
    for tag in list['tags']:
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
    if ".js" in file:
        serialize = json.dumps(versions)
        resource = resource_template.render(component_versions_json=serialize)
    elif ".md" in file:
        resource = resource_template.render(component_versions=versions)

    with open(f'{dest_prefix}/{file}', 'w') as f:
        f.write(resource)


def sync(argv):
    """ fetch all the files and sync it to the website """
    # get the path of the urls needed
    config_files = get_files(f'{FLAGS.config}', ".yaml")
    config = yaml_files_to_dic_list(config_files)
    # download resources
    download_resources_to_project(config)
    # create version switcher script
    create_resource(JS_ASSET_DIR, "version-switcher.js", get_versions(config))
    # create index for valut
    create_resource(VAULT_DIR, "_index.md", get_versions(config))


if __name__ == '__main__':
    app.run(sync)
