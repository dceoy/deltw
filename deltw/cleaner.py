#!/usr/bin/env python

from zipfile import ZipFile
import re
import json
from functools import reduce


def list_tweet_ids(archive_zip):
    def extract_id_str(js_path, zip_obj):
        return(list(map(lambda t: t['id_str'],
                        json.loads(re.sub(r'^Grailbird[^=]+=', '',
                                          zip_obj.read(js_path).decode('utf-8'))))))

    with ZipFile(archive_zip) as az:
        tw_dir = 'data/js/tweets/'
        tw_js_files = filter(lambda n: re.match(tw_dir, n),
                             map(lambda f: f.filename, az.infolist()))
        return(reduce(lambda a, b: a + b,
                      map(lambda js: extract_id_str(js, az), tw_js_files)))


def delete_tweets(tw_session, id_str):
    print('delete /status/%s' % id_str)
    return(tw_session.post('https://api.twitter.com/1.1/statuses/destroy/%s.json' % id_str))
