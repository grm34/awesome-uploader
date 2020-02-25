#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Logs
logs = {

    # level: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
    'level': 'DEBUG',
    'path': ''
}

# Tracker infos
tracker = {
    'user_authkey': '',
    'url_announce': '',
    'url_api': ''
}

# User
user = {
    'working_dir': '',
    'torrents_dir': '',
    'watch_dir': '',
    'upload_dir': ''
}

# API
api = {
    'layer13_url': 'http://api.layer13.net/v1/',
    'layer13_apikey': '',
    'srrdb_url': 'https://www.srrdb.com/api/nfo/'
}

# Release category
cat = {
    'movies': '1',
    'series': '2',
    'docs': '3',
    'tv': '4',
    'sports': '5',
    'anime': '6',
    'apps': '7',
    'games': '8',
    'ebook': '9',
    'cartoon': '10'
}

# Teams
team = {
    'animes': [
        'MANGACiTY' 'BOOLZ', 'D4KiD', 'NEECHAN', 'SaSHiMi',
        'SHiNiGAMi', 'DIEBEX', 'KAZETV', 'SLEEPINGFOREST', 'OOKAMI'],
    'games': [
        'CPY', 'SKiDROW', 'FLT', 'RELOADED', 'PLAZA', 'CODEX']
}

# Regex
regex = {
    'series': r'\.S[0-9]{1,2}[E|x][0-9]{1,3}\.',
    'movies': r'\.[0-9]{4}\.',
    'docs': r'\.DOC(S|)\.',
    'animes': r'\.VOL[0-9]{1,2}\.'
}

# Patterns
patterns = {

    # for files only
    'includes': ['*.nfo', '*.avi', '*.mkv'],

    # for dirs and files
    'excludes': ['*.srr', '*.flv', '*.sub', '*.idx', '*.nzb', '*sample*']
}
