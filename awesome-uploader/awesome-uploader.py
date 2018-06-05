#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import fnmatch
import requests
import subprocess
import multiprocessing
from shutil import copyfile
from os.path import basename
from conf.config import (tracker, user, api, cat, team, regex, patterns)
from conf.history import (logger, formatter, file_handler, stream_handler)
(releases_title, releases_category, releases_size, releases_pieces,
    available_files, rls_without_nfo, upload_queue) = ([] for i in range(7))


def filemanager():
    logger.info('Run Filemanager...')
    for release in os.listdir(user['working_dir']):

        # release need to be a folder so delete all files
        if os.path.isfile(os.path.join(user['working_dir'], release)):
            os.remove(os.path.join(user['working_dir'], release))
            logger.warning('DELETED: {}'.format(
                os.path.join(user['working_dir'], release)))

        # prevent duplicates
        elif os.path.isdir(os.path.join(user['upload_dir'], release)):
            logger.debug('SKIPPED: {} (release exists)'.format(release))

        # get releases titles
        else:
            releases_title.append('{}'.format(release))
            logger.debug('ADDED: {}'.format(release))

    # includes/excludes patterns
    (includes, excludes) = (patterns['includes'], patterns['excludes'])

    # transform glob patterns to regular expressions
    includes = r'|'.join([fnmatch.translate(x) for x in includes])
    excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

    for root, dirs, files in os.walk(user['working_dir']):

        # exclude dirs
        dirs[:] = [os.path.join(root, d) for d in dirs]
        dirs[:] = [d for d in dirs if not re.match(excludes, d)]

        # exclude/include files
        files = [os.path.join(root, f) for f in files]
        files = [f for f in files if not re.match(excludes, f)]
        files = [f for f in files if re.match(includes, f)]

        for name in files:

            # get available files
            if basename(name) not in available_files:
                available_files.append('{}'.format(basename(name)))

            # get releases without nfo
            if not any(name.endswith('.nfo') for name in files):
                without_nfo = os.path.splitext(basename(name))[0]
                if without_nfo not in rls_without_nfo:
                    if without_nfo in releases_title:
                        rls_without_nfo.append('{}'.format(without_nfo))

    for root, dirs, files in os.walk(user['working_dir']):
        for name in files:

            # delete undesirable files
            if name not in available_files:
                os.remove(os.path.join(root, name))
                logger.warning('DELETED: {}'.format(os.path.join(root, name)))

            # rename NFO if != release_title
            if name.endswith('.nfo') and name[:-4] != basename(root):
                os.rename(os.path.join(root, name), '{}.nfo'.format(
                    os.path.join(root, basename(root))))
                logger.debug('RENAMED: {0} to {1}.nfo'.format(
                    name, basename(root)))


def get_release_nfo():
    logger.info('Scan releases NFO...')
    for release in rls_without_nfo:

        # add missing NFO to available files
        logger.info('Missing NFO for: {}'.format(release))
        available_files.append('{}.nfo'.format(release))

        # search NFO on srrdb
        nfo = requests.get('{0}{1}'.format(api['srrdb_url'], release)).json()

        # download NFO when available on srrdb
        if nfo['nfolink']:
            get = requests.get('{}'.format(nfo['nfolink'][0]))
            with open('{0}/{1}.nfo'.format(os.path.join(
                    user['working_dir'], release), release), 'wb') as code:
                code.write(get.content)
            logger.info('DOWNLOADED: {}'.format(basename(nfo['nfolink'][0])))

        # otherwise search NFO on Layer13
        elif api['layer13_apikey']:
            nfo = requests.get('{0}?getpre={1}$key={2}'.format(
                api['layer13_url'], release, api['layer13_apikey'])).json()
            if nfo['id']:
                nfo = requests.get('{0}?listfiles={1}$key={2}'.format(
                    api['layer13_url'], nfo['id'][0],
                    api['layer13_apikey'])).json()

                # download NFO when available on Layer13
                if nfo['filename'] and ".nfo" in nfo['filename'][0]:
                    get = requests.get(
                        '{0}?getfile={1}$key={2}&filename={3}'.format(
                            api['layer13_url'], release,
                            api['layer13_apikey'], nfo['filename'][0]))
                    with open(
                        '{0}/{1}.nfo'.format(os.path.join(
                            user['working_dir'], release), release),
                            'wb') as code:
                                code.write(get.content)
                    logger.info('DOWNLOADED: {}'.format(nfo['filename'][0]))

        # skip release if NFO not found
        else:
            logger.info('NFO not found: {}'.format(release))
            releases_title.remove('{}'.format(release))
            logger.info('SKIPPED: {} (NFO not found)'.format(release))


def get_release_category():
    logger.info('Get releases category...')
    for title in releases_title:

        # DOCS
        if re.search(regex['docs'], title) is not None:
            releases_category.append('{}'.format(cat['docs']))

        # MOVIES
        elif re.search(regex['movies'], title) is not None:
            if title.split('-')[-1] not in team['animes']:
                releases_category.append('{}'.format(cat['movies']))

        # ANIMES
        elif re.search(regex['animes'], title) is not None:
            if title.split('-')[-1] not in team['animes']:
                releases_category.append('{}'.format(cat['animes']))

        # SERIES
        elif re.search(regex['series'], title) is not None:
            releases_category.append('{}'.format(cat['series']))

        # GAMES
        elif title.split('-')[-1] in team['games']:
            releases_category.append('{}'.format(cat['games']))

        else:
            logger.info('Category not found for: {}'.format(title))
            category = input('Enter category code: ')
            while not category or category.isdigit() is False\
                    or int(category) < 1 or int(category) > 10:
                category = input(
                    'Error, enter a valid category code: ')
            releases_category.append('{}'.format(category))


def get_release_size():
    logger.info('Get releases size...')
    for release in releases_title:
        path = os.path.join(user['working_dir'], release)
        size = subprocess.check_output(
            ['du', '-sh', path]).split()[0].decode('utf-8')
        releases_size.append('{}'.format(size))


def get_torrent_pieces():
    logger.info('Get torrents pieces...')
    for size in releases_size:
        if 'K' in size or ('M' in size and float(size[:-1]) < 400):
            torrent_pieces = '18'
        elif 'M' in size and float(size[:-1]) < 650:
            torrent_pieces = '19'
        elif 'M' in size or ('G' in size and float(size[:-1]) < 2.5):
            torrent_pieces = '20'
        elif 'G' in size and float(size[:-1]) < 5:
            torrent_pieces = '21'
        else:
            torrent_pieces = '22'
        releases_pieces.append('{}'.format(torrent_pieces))


def get_upload_queue():
    logger.info('Get upload queue list...')
    upload_queue.append(list(zip(
        releases_title, releases_size, releases_category, releases_pieces)))


def create_torrent():
    logger.info('Creating torrents...')
    cpu_threads = multiprocessing.cpu_count()
    for entry in upload_queue:
        for value in entry:
            returncode = subprocess.call(
                'mktorrent -a {0} -p -t {1} -l {2} -o {3}{4}.torrent \
                {5}{4} >/dev/null 2>&1'
                .format(tracker['url_announce'], cpu_threads, value[3],
                        user['torrents_dir'], value[0], user['working_dir']),
                shell=True)
            if returncode > 0:
                logger.info('Error creating {}.torrent (file exists)'
                            .format(value[0]))
            else:
                logger.info('CREATED: {}.torrent'.format(value[0]))


def upload_torrent():
    logger.info('Uploading torrents...')
    for release in upload_queue:
        for value in release:
            torrent = '{}.torrent'.format(
                os.path.join(user['torrents_dir'], value[0]))
            nfo = '{0}/{1}.nfo'.format(
                os.path.join(user['working_dir'], value[0]), value[0])
            headers = {'X-AUTH-TOKEN': '{}'.format(tracker['user_authkey'])}
            files = {
                'torrentFile': (torrent, open(torrent, 'rb')),
                'nfoFile': (nfo, open(nfo, 'rb')),
                'cat': (None, '{}'.format(value[2])),
                'internal': (None, '0'),
            }
            upload = requests.post(
                tracker['url_api'], headers=headers, files=files)
            if upload.status_code == 200:
                logger.info('UPLOADED: {}'.format(value[0]))
            time.sleep(5)


def start_seeding():
    logger.info('Start seeding...')

    # move releases to upload folder
    for release in releases_title:
        os.rename(
            os.path.join(user['working_dir'], release),
            os.path.join(user['upload_dir'], release))
        logger.debug('MOVED: {0} to {1}'.format(
            release, user['upload_dir']))

    # copy .torrents to watch folder
    for torrent in os.listdir(user['torrents_dir']):
        copyfile(
            os.path.join(user['torrents_dir'], torrent),
            os.path.join(user['watch_dir'], torrent))
        logger.debug('COPIED: {0} to {1}'.format(
            torrent, user['watch_dir']))


# Nothing to do?
if not os.listdir(user['working_dir']):
    logger.info('INFO: up to date. {} is empty.'.format(user['working_dir']))
    sys.exit(0)

# Run
filemanager()
get_release_nfo()
get_release_category()
get_release_size()
get_torrent_pieces()
get_upload_queue()
create_torrent()
upload_torrent()
start_seeding()

# DEBUG
logger.debug('Releases title: {}'.format(releases_title))
logger.debug('Releases category: {}'.format(releases_category))
logger.debug('Releases size: {}'.format(releases_size))
logger.debug('Releases pieces: {}'.format(releases_pieces))
logger.debug('Available files: {}'.format(available_files))
logger.debug('Releases without NFO: {}'.format(rls_without_nfo))
logger.debug('Upload queue: {}'.format(upload_queue))
