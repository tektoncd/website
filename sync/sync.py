# This script helps synchronize contents from their respective sources of
# truth (usually GitHub repositories of each Tekton
# components, such as tektoncd/pipelines) to tektoncd/website.

import json
import os
import shutil

from google.oauth2 import service_account
from google.cloud import storage
from jinja2 import Environment, FileSystemLoader
import wget
from yaml import load, Loader


CONTENT_DIR = './content/en/docs'
JS_ASSET_DIR = './assets/js'
SYNC_DIR = './sync/config'
TEMPLATE_DIR = './templates'
VAULT_DIR = './content/en/vault'
BUCKET_NAME = 'tekton-website-assets'

GCP_NETLIFY_ENV_CRED = os.environ.get('GCP_CREDENTIAL_JSON')
GCP_PROJECT = os.environ.get('GCP_PROJECT')

jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def retrieve_files(url_prefix, dest_prefix, files):
    if os.path.isdir(dest_prefix):
        shutil.rmtree(dest_prefix)
    os.mkdir(dest_prefix)
    for f in files:
        for k in f:
            src_url = f'{url_prefix}/{k}'
            dest_path = f'{dest_prefix}/{f[k]}'
            print(f'Downloading file (from {src_url} to {dest_path}).\n')
            wget.download(src_url, out=dest_path)
            print('\n')


def verify_name_format(word):
    pass


def remove_ending_forward_slash(word):
    return word[:-1] if word.endswith('/') else word


def sync(sync_config):
    component = sync_config['component']
    repository = remove_ending_forward_slash(sync_config['repository'])
    doc_directory = remove_ending_forward_slash(sync_config['docDirectory'])
    tags = sync_config['tags']

    # Get the latest version of contents
    url_prefix = f'{repository}/raw/{tags[0]["name"]}/{doc_directory}'
    dest_prefix = f'{CONTENT_DIR}/{component}'
    files = tags[0]['files']
    print(f'Retrieving the latest version ({tags[0]["displayName"]}) of Tekton {component} documentation (from {url_prefix} to {dest_prefix}).\n')
    retrieve_files(url_prefix, dest_prefix, files)

    # Get the previous versions of contents
    for tag in tags[1:]:
        url_prefix = f'{repository}/raw/{tag["name"]}/{doc_directory}'
        dest_prefix = f'{VAULT_DIR}/{component}-{tag["displayName"]}'
        files = tag['files']
        print(f'Retrieving version {tag["displayName"]} of Tekton {component} documentation (from {url_prefix} to {dest_prefix}).\n')
        retrieve_files(url_prefix, dest_prefix, files)


def get_component_versions(sync_configs):
    component_versions = []
    for sync_config in sync_configs:
        component_versions.append({
            'name': sync_config['component'],
            'tags': [ {'name': tag['name'], 'displayName': tag['displayName']} for tag in sync_config['tags'] ],
            'archive': sync_config['archive']
        })
    return component_versions


def prepare_version_switcher_script(component_versions):
    script_template = jinja_env.get_template('version-switcher.js.template')
    script = script_template.render(component_versions_json=json.dumps(component_versions))
    with open(f'{JS_ASSET_DIR}/version-switcher.js', 'w') as f:
        f.write(script)


def prepare_vault_landing_page(component_versions):
    md_template = jinja_env.get_template('_index.md.template')
    md = md_template.render(component_versions=component_versions)
    with open(f'{VAULT_DIR}/_index.md', 'w') as f:
        f.write(md)


def scan(dir_path):
    entries = os.scandir(dir_path)
    sync_config_paths = []
    for entry in entries:
        if entry.name.endswith('.yaml'):
            sync_config_paths.append(entry.path)
        elif entry.is_dir():
            scan(entry.path)
    
    return sync_config_paths

if __name__ == '__main__':
    sync_config_paths = scan(f'./{SYNC_DIR}')
    sync_configs = []
    for sync_config_path in sync_config_paths:
        with open(sync_config_path) as f:
            sync_config = load(f, Loader=Loader)
        sync_configs.append(sync_config)
        sync(sync_config)
    sync_configs.sort(key=lambda x: x['displayOrder'])
    component_versions = get_component_versions(sync_configs)
    prepare_version_switcher_script(component_versions)
    prepare_vault_landing_page(component_versions)
