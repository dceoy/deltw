#!/usr/bin/env python


from zipfile import ZipFile
import re
import json
from functools import reduce
import sys
from requests_oauthlib import OAuth1Session


def tw_session(json_path):
    with open(json_path) as f:
        cr = json.load(f)

    return(OAuth1Session(cr['consumer_key'],
                         cr['consumer_secret'],
                         cr['access_token'],
                         cr['access_token_secret']))


def list_tw_ids(archive_zip):
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


def delete_tw(session, id_str):
    print('delete /status/%s' % id_str)
    return(session.post('https://api.twitter.com/1.1/statuses/destroy/%s.json' % id_str))


if __name__ == '__main__':
    data_path = sys.argv[1]
    tw = tw_session('credentials.json')
    [delete_tw(tw, id) for id in list_tw_ids(data_path)]
