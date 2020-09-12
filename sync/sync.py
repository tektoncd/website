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
from yaml import load
from yaml import Loader


FLAGS = flags.FLAGS

# Flag names are globally defined!  So in general, we need to be
# careful to pick names that are unlikely to be used by other libraries.
# If there is a conflict, we'll get an error at import time.
flags.DEFINE_string('config', os.path.dirname(os.path.abspath(__file__)) + '/config', 'Config directory', short_name='c')

CONTENT_DIR = './content/en/docs'
JS_ASSET_DIR = './assets/js'
TEMPLATE_DIR = './templates'
VAULT_DIR = './content/en/vault'
BUCKET_NAME = 'tekton-website-assets'

GCP_NETLIFY_ENV_CRED = os.environ.get('GCP_CREDENTIAL_JSON')
GCP_PROJECT = os.environ.get('GCP_PROJECT')

RELATIVE_LINKS_RE = r'\[([^\]]*)\]\((?!.*://|/)([^)]*).md(#[^)]*)?\)'

jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def transform_links(link_prefix, dest_prefix, files, url):
    ''' go through every line to ensure that each url in a line is valid '''
    logging.info('Running: transforming files...')

    lines = get_lines(dest_prefix, files)
    transformed_lines = []

    for line, file in lines:
        line, is_transformed = sanitize_text(link_prefix, line)
        links = get_links(line) 

        if is_transformed:
            for link in links:
                link = link.get("href")
                if not(os.path.isfile(link) or is_valid_url(link) or is_reference(link)):
                    line = line.replace(link, github_link(url, link))
        
        transformed_lines.append(line)
    
    set_lines(dest_prefix, files, transformed_lines)

    logging.info('Completed: transformed files')


def set_lines(dest_prefix, files, lines):
    ''' get all the files into a ball of text and replace each line with a list '''
    for f in files:
        for k in f:
            dest_path = f'{dest_prefix}/{f[k]}'
            for line in fileinput.input(dest_path, inplace=1):
                # Print set's line in the file inplace
                print(lines[0])
                lines = lines[1:]

def get_lines(dest_prefix, files):
    ''' save all the lines from a directory and list of files into a list'''
    lines = []

    for f in files:
        for k in f:
            dest_path = f'{dest_prefix}/{f[k]}'
            for line in fileinput.input(dest_path):
                lines.append((line, f))

    return lines

def github_link(url, link):
    ''' given a github raw link convert it to the main github link '''
    return f'{url.replace("raw", "tree", 1)}/{link}'

def sanitize_text(link_prefix, text):
    ''' santize every line of text to exclude relative links and have proper markdown '''
    old_line = text.rstrip()
    new_line = re.sub(RELATIVE_LINKS_RE, r'[\1](' + link_prefix + r'\2\3)', old_line)
    return (new_line, old_line == new_line)

def is_valid_url(url):
    ''' check if it is a valid url '''
    try:
        urlopen(url).read()
    except HTTPError as e:
        return True
    except URLError as e:
        return True
    except ValueError as e:
        return False

    return True

def is_reference(url):
    ''' determine if the url is an a href '''
    if len(url) < 0:
        return False

    return url[0] == "#"

def get_links(md):
    ''' return a list of all the links in a string formatted in markdown '''
    md = markdown.markdown(md)
    try:
        doc = etree.fromstring(md)
        return doc.xpath('//a')
    except:
        return []

def download_files(url_prefix, dest_prefix, files):
    ''' download the file and create the correct folders that are neccessary '''
    if os.path.isdir(dest_prefix):
        shutil.rmtree(dest_prefix)
    os.mkdir(dest_prefix)
    for f in files:
        for k in f:
            src_url = f'{url_prefix}/{k}'
            dest_path = f'{dest_prefix}/{f[k]}'
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            logging.info(f'Downloading {src_url} to {dest_path}...\n')
            wget.download(src_url, out=dest_path)
            logging.info(f'\n')


def remove_ending_forward_slash(word):
    ''' remove the last character if it is backslash '''
    return word[:-1] if word.endswith('/') else word

def get_file_directories(entry, index, source_dir, dest_dir):
    ''' return the files and there directories. Their relative and absolute counterpart is needed to download the files properly to the website '''
    tag = entry['tags'][index]
    repository = remove_ending_forward_slash(entry['repository'])
    doc_directory = remove_ending_forward_slash(entry['docDirectory'])
    host_dir = f'{repository}/raw/{tag["name"]}/{doc_directory}'
    files = tag['files']

    return ( host_dir, source_dir, dest_dir, files )

def download_resources_to_project(yaml_list):
    ''' download the files based on a certain spec. The YAML sync spec can be found in sync/config/README.md'''
    for entry in yaml_list:
        directories = None
        component = entry['component'].lower()

        for index, tag in enumerate(entry['tags']):
            # get the link for the item as well as the output dir
            if index == 0:
                directories = get_file_directories(entry, index, f'/docs/{component}/', f'{CONTENT_DIR}/{component}')
            else:
                directories = get_file_directories(entry, index, f'/vault/{component}-{tag["displayName"]}/', f'{VAULT_DIR}/{component}-{tag["displayName"]}')
        
            if directories:
                host_dir, source_dir, dest_dir, files = directories
                # download file from link
                download_files(host_dir, dest_dir, files)
                # change the textr in the file download from link
                transform_links(source_dir, dest_dir, files, host_dir)

def get_files(path, file_type):
    ''' return a list of all the files with the correct type '''
    filelist = []

    # walk through every file in directory and its sub directories
    for root, dirs, files in os.walk(path):
        for file in files:
            # append the file name to the list if is it the correct type
            if file_type in file:
                filelist.append(os.path.join(root,file))

    return filelist

def yaml_files_to_list(files):
    ''' return a list of yaml files to a sorted list based on a field called displayOrder '''
    dic = []
    
    for file in files:
        with open(file) as text:
            # get the paths from the config file
            dic.append(yaml.load(text, Loader=yaml.FullLoader))
    
    dic.sort(key=lambda x: x['displayOrder'])

    return dic


def get_versions(sync_configs):
    ''' return the list of all the versions and there tag, name, archive '''
    component_versions = []
    for sync_config in sync_configs:
        component_versions.append({
            'name': sync_config['component'],
            'tags': [ {'name': tag['name'], 'displayName': tag['displayName']} for tag in sync_config['tags'] ],
            'archive': sync_config['archive']
        })
    return component_versions


def create_site_resource(dest_prefix, file, versions):
    ''' create site resource based on the version and file '''
    resource_template = jinja_env.get_template(f'{file}.template')
    resource = resource_template.render(component_versions_json=json.dumps(versions))
    with open(f'{dest_prefix}/{file}', 'w') as f:
        f.write(resource)


def sync(argv):
    ''' fetch all the files and sync it to the website '''
    logging.info("Syncing files")
    # get the path of the urls needed
    config_files = get_files(f'{FLAGS.config}', ".yaml")
    config = yaml_files_to_list(config_files)
    # download resources
    download_resources_to_project(config)
    create_site_resource(JS_ASSET_DIR, "version-switcher.js", get_versions(config))
    create_site_resource(VAULT_DIR, "_index.md", get_versions(config))
    logging.info("Sync Complete")

if __name__ == '__main__':
  app.run(sync)