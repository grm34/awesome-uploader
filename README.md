# ![icon](https://github.com/grm34/awesome-uploader/blob/master/doc/awesome-uploader.png) awesome-uploader

[![version](https://img.shields.io/badge/version-1.0.1-green.svg)](https://github.com/grm34/awesome-uploader/releases) [![beta](https://img.shields.io/badge/status-beta-lightgrey.svg)](https://github.com/grm34/awesome-uploader/releases) [![author](https://img.shields.io/badge/author-grm34-red.svg)](https://github.com/grm34) [![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/grm34/awesome-uploader/blob/master/LICENSE) [![maintenance](https://img.shields.io/maintenance/yes/2018.svg)](https://github.com/grm34/awesome-uploader/pulse)

## Dependencies

* python3 (3.4, 3.5, 3.6, 3.8)
* python-requests
* mktorrent

## Installation

```shell
git clone git@github.com:grm34/awesome-uploader.git
nano awesome-uploader/awesome-uploader/conf/config.py
```

## Configuration

* **Logs**:
  * level: set loglevel (*level: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET*)
  * path: set path to store activity logs

* **Tracker**:
  * authkey: set your tracker authkey
  * url_announce: set tracker announce url
  * url_api: set tracker api url

* **User**:
  * working_dir: path of releases to upload
  * torrents_dir: path to store .torrents files
  * watch_dir: your watch dir path
  * upload_dir: path of releases in seed

* **Api**:
  * layer13_url: `http://api.layer13.net/v1/`
  * layer13_apikey: set your layer13 api key
  * srrdb_url: `https://www.srrdb.com/api/nfo/`

* **Releases category**:
  * Set tracker category number

* **Teams**:
  * Match only some animes and games teams.

* **Regex**:
  * Match tracker categories

* **Patterns**:
  * includes: match only included files
  * excludes: delete excluded files

## Usage

`python3 awesome-uploader.py`

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/for-you.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/its-not-a-lie-if-you-believe-it.svg)](https://forthebadge.com)
