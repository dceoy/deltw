#!/usr/bin/env python


import sys
import json
from requests_oauthlib import OAuth1Session


def tw_session(json_path):
    with open(json_path) as f:
        cr = json.load(f)

    return(OAuth1Session(cr['consumer_key'],
                         cr['consumer_secret'],
                         cr['access_token'],
                         cr['access_token_secret']))


def extract_id_str(json_path):
    with open(json_path) as f:
        tweets = json.load(f)

    id_ls = []
    for m in tweets:
        for e in m:
            id_ls.append(e['id_str'])

    return(id_ls)


def delete_tweet(session, id_str):
    print('delete /status/%s' % id_str)
    return(session.post('https://api.twitter.com/1.1/statuses/destroy/%s.json' % id_str))


if __name__ == '__main__':
    data_path = sys.argv[1]
    tw = tw_session('credentials.json')
    id_ls = extract_id_str(data_path)

    for id in id_ls:
        delete_tweet(tw, id)
