# This script helps synchronize contents from their respective sources of
# truth (usually GitHub repositories of each Tekton
# components, such as tektoncd/pipelines) to tektoncd/website.

import os

import wget
from yaml import load, Loader


CONTENT_DIR = '/content/'
SYNC_CONFIG_FILENAME = 'sync.yaml'


def parseSyncConfig(syncConfigPath, destDir):
    with open(syncConfigPath) as f:
        syncConfig = load(f, Loader=Loader)
    repo = syncConfig['repository']
    docDir = syncConfig['docDirectory']
    tag = syncConfig.get('tag', 'master')
    urlPrefix = f'{repo}/raw/{tag}/{docDir}'

    res = []
    for f in syncConfig['files']:
        for k in f:
            srcUrl = f'{urlPrefix}/{k}'
            destPath = f'{destDir}/{f[k]}'
            res.append((srcUrl, destPath))
    return res


def getFiles(syncConfigPath):
    destDir = syncConfigPath.replace(f'/{SYNC_CONFIG_FILENAME}', '')
    srcDestPairs = parseSyncConfig(syncConfigPath, destDir)
    for p in srcDestPairs:
        srcUrl = p[0]
        destPath = p[1]
        wget.download(srcUrl, out=destPath)

def scan(dirPath):
    entries = os.scandir(dirPath)
    for entry in entries:
        if entry.name == SYNC_CONFIG_FILENAME:
            getFiles(entry.path)
        elif entry.is_dir():
            scan(entry.path)

if __name__ == '__main__':
    scan(f'./{CONTENT_DIR}')