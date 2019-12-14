#!/usr/bin/env python

import json
import logging
import os
import re
import signal
from pprint import pformat
from zipfile import ZipFile, is_zipfile

import yaml
from requests_oauthlib import OAuth1Session

from .util import DeltwError


def print_user_details(zip_path):
    """Print user details in a ZIP archive
    """
    logging.info('Print user details in a ZIP archive: {}'.format(zip_path))
    _validate_files(zip_path=zip_path)
    print(yaml.dump(
        _extract_user_details(zip_path=zip_path),
        default_flow_style=False, allow_unicode=True
    ))


def _validate_files(zip_path=None, yml_path=None):
    if zip_path and not is_zipfile(zip_path):
        raise DeltwError('invalid ZIP path: {}'.format(zip_path))
    elif yml_path and not os.path.isfile(yml_path):
        raise DeltwError('invalid YAML path: {}'.format(yml_path))
    else:
        logging.debug('Paths were validatated.')


def _extract_user_details(zip_path):
    with ZipFile(zip_path) as zf:
        js_str = zf.read('data/js/user_details.js').decode('utf-8')
    user_details = json.loads(re.sub(r'^var user_details *=', '', js_str))
    logging.debug(
        'user_details:{0}{1}'.format(os.linesep, pformat(user_details))
    )
    return user_details


def print_tweet_urls(zip_path, regex=None):
    """Print URLs of tweets in a ZIP archive
    """
    logging.info('Print URLs of tweets in a ZIP archive: {}'.format(zip_path))
    _validate_files(zip_path=zip_path)
    screen_name = _extract_user_details(zip_path=zip_path)['screen_name']
    print(
        *[
            'https://twitter.com/{0}/status/{1}'.format(screen_name, i)
            for i in _extract_tweet_ids(zip_path=zip_path, regex=regex)
        ],
        sep=os.linesep
    )


def delete_tweets(zip_path, cred_yml_path, ignore_error=False, regex=None):
    """Delete tweets on Twitter
    """
    logging.info('Delete tweets in a ZIP archive: {}'.format(zip_path))
    _validate_files(zip_path=zip_path, yml_path=cred_yml_path)
    tw_session = _create_session(yml_path=cred_yml_path)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    n_succeeded = 0
    n_failed = 0
    print('Start to delete tweets on Twitter.')
    for tweet_id in _extract_tweet_ids(zip_path=zip_path, regex=regex):
        req = 'https://api.twitter.com/1.1/statuses/destroy/{}.json'.format(
            tweet_id
        )
        http_code = tw_session.post(req).status_code
        print('  POST {0} => {1}'.format(req, http_code))
        if http_code == 200:
            n_succeeded += 1
            logging.info('{}: HTTP request was received.'.format(http_code))
        else:
            n_failed += 1
            warn = (
                '{}: URL was not found.'.format(http_code)
                if http_code == 404 else
                '{}: HTTP request failed.'.format(http_code)
            )
            if ignore_error:
                logging.warning(warn)
            else:
                raise DeltwError(warn)
    print(
        '{0} {1} deleted on Twitter.{2}'.format(
            n_succeeded, ('tweets were' if n_succeeded > 1 else 'tweet was'),
            (
                ' (succeeded: {0}, failed: {1})'.format(n_succeeded, n_failed)
                if ignore_error else ''
            )
        )
    )


def _create_session(yml_path):
    logging.info('Create a Twitter session.')
    with open(yml_path) as f:
        cr = yaml.load(f)
    logging.debug('cr: {}'.format(cr))
    return OAuth1Session(
        cr['consumer_key'], cr['consumer_secret'], cr['access_token'],
        cr['access_token_secret']
    )


def _extract_tweets(zipfile, zipinfo):
    """Read provided zip_info from zip_file with JSON tweets
     and return list of dict objects.
    """
    return json.loads(
        re.sub(r'^Grailbird[^=]+=', '', zipfile.read(zipinfo).decode('utf-8'))
    )


def _extract_tweet_ids(zip_path, regex=None):
    """Extract tweet IDs
    """
    with ZipFile(zip_path) as zf:
        tw_js_names = [
            z.filename for z in zf.infolist()
            if z.filename.startswith('data/js/tweets')
        ]
        logging.debug(
            'js_paths_in_zip:{0}{1}'.format(os.linesep, pformat(tw_js_names))
        )
        for zip_info in tw_js_names:
            for tweet in _extract_tweets(zf, zip_info):
                if regex is None or re.search(regex, tweet['text']):
                    yield tweet['id']
                else:
                    pass
