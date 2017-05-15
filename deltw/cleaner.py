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


def extract_all_ids(zip_archive):
    with ZipFile(zip_archive) as za:
        nested_id_lists = [
            [t['id_str']
             for t in json.loads(re.sub(r'^Grailbird[^=]+=', '',
                                        za.read(j).decode('utf-8')))]
            for j in filter(lambda f: re.match('data/js/tweets/', f.filename),
                            za.infolist())
        ]
    return list(reduce(lambda a, b: a + b, nested_id_lists))


def make_requests(ids):
    return ['https://api.twitter.com/1.1/statuses/destroy/{}.json'.format(id)
            for id in ids]


def delete_tweets(credentials_yml, zip_archive, test_print=False):
    reqs = make_requests(ids=extract_all_ids(zip_archive=zip_archive))
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
