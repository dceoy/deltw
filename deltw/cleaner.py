#!/usr/bin/env python

import yaml
from requests_oauthlib import OAuth1Session
from zipfile import ZipFile
import re
import json
from functools import reduce
import click


def create_session(yml_path):
    with open(yml_path) as f:
        cr = yaml.load(f)

    return(OAuth1Session(cr['consumer_key'],
                         cr['consumer_secret'],
                         cr['access_token'],
                         cr['access_token_secret']))


def extract_tweet_ids(archive_zip):
    def list_id_str(js_path, zip_obj):
        return(list(map(lambda t: t['id_str'],
                        json.loads(re.sub(r'^Grailbird[^=]+=', '',
                                          zip_obj.read(js_path).decode('utf-8'))))))

    with ZipFile(archive_zip) as az:
        tw_dir = 'data/js/tweets/'
        tw_js_files = filter(lambda n: re.match(tw_dir, n),
                             map(lambda f: f.filename, az.infolist()))
        return(tuple(reduce(lambda a, b: a + b,
                            map(lambda js: list_id_str(js, az), tw_js_files))))


def delete_tweets(tw_session, *id_tuple):
    def destroy_tw(tw_session, id):
        click.echo('delete /status/%s' % id)
        tw_session.post('https://api.twitter.com/1.1/statuses/destroy/%s.json' % id)

    map(lambda id: destroy_tw(tw_session, id), id_tuple)
