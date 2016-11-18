#!/usr/bin/env python

import yaml
from requests_oauthlib import OAuth1Session


def create_session(yml_path):
    with open(yml_path) as f:
        cr = yaml.load(f)

    return(OAuth1Session(cr['consumer_key'],
                         cr['consumer_secret'],
                         cr['access_token'],
                         cr['access_token_secret']))
