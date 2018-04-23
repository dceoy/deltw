#!/usr/bin/env python

from functools import reduce
import json
import os
import re
import signal
import yaml
from zipfile import ZipFile
from requests_oauthlib import OAuth1Session


def write_credential_template(yml_path):
    if os.path.exists(yml_path):
        print('%s already exists' % yml_path)
    else:
        with open(yml_path, 'w') as f:
            f.write(yaml.dump({'consumer_key': '',
                               'consumer_secret': '',
                               'access_token': '',
                               'access_token_secret': ''},
                              default_flow_style=False))


def create_session(yml_path):
    with open(yml_path) as f:
        cr = yaml.load(f)
    return OAuth1Session(cr['consumer_key'],
                         cr['consumer_secret'],
                         cr['access_token'],
                         cr['access_token_secret'])


def iter_tweet_files(zip_file):
    """Generator yielding files with tweets
    Args:
    - zip_file: instance of ZipFile

    Yields: instance of ZipInfo
    """
    for zip_info in zip_file.infolist():
        if zip_info.filename.startswith('data/js/tweets'):
            yield zip_info


def decoded_tweets(zip_file, zip_info):
    """Read provided zip_info from zip_file with JSON tweets
     and return list of dict objects.
    """
    contents = zip_file.read(zip_info).decode('utf-8')
    json_str = re.sub(r'^Grailbird[^=]+=', '', contents)
    return json.loads(json_str)


def filtered_ids(zip_archive, text_pattern=None):
    "Generates ids with filtered tweets"
    with ZipFile(zip_archive) as zip_file:
        for zip_info in iter_tweet_files(zip_file):
            for tweet in decoded_tweets(zip_file, zip_info):
                if text_pattern is None:
                    yield tweet['id']
                elif re.search(text_pattern, tweet['text']):
                    yield tweet['id']


def make_requests(ids):
    return ['https://api.twitter.com/1.1/statuses/destroy/{}.json'.format(id)
            for id in ids]


def delete_tweets(credentials_yml, zip_archive, test_print=False, text_pattern=None):
    reqs = make_requests(ids=filtered_ids(zip_archive, text_pattern))
    if test_print:
        print(*reqs, sep=os.linesep)
    else:
        tw_session = create_session(yml_path=credentials_yml)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        print('%d tweets are to be deleted:' % len(reqs))
        for req in reqs:
            print('  POST %s' % req)
            tw_session.post(req)
        print('done.')
