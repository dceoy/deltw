#!/usr/bin/env python

import json
import logging
import os
import re
import signal
from pathlib import Path
from pprint import pformat
from zipfile import ZipFile, is_zipfile

import yaml
from requests_oauthlib import OAuth1Session


def print_user_info(zip_path):
    """Print user details in a ZIP archive
    """
    logging.info(f'Print user details in a ZIP archive:\t{zip_path}')
    _validate_files(zip_path=zip_path)
    print(
        yaml.dump(
            _extract_user_info(zip_path=zip_path),
            default_flow_style=False, allow_unicode=True
        )
    )


def _validate_files(zip_path=None, yml_path=None):
    if zip_path and not is_zipfile(zip_path):
        raise RuntimeError(f'invalid ZIP path:\t{zip_path}')
    elif yml_path and not Path(yml_path).is_file():
        raise RuntimeError(f'invalid YAML path:\t{yml_path}')
    else:
        logging.debug('Paths were validatated.')


def _extract_user_info(zip_path):
    with ZipFile(zip_path) as zf:
        name_set = set(zf.namelist())
        if 'data/account.js' in name_set:
            target = 'data/account.js'
        elif 'data/js/user_details.js' in name_set:
            target = 'data/js/user_details.js'
        else:
            raise ValueError('user info detection failed.')
        js_str = zf.read(target).decode('utf-8')
    user_info = json.loads(re.sub(r'^[^=]+=', '', js_str))
    logging.debug('user_info:' + os.linesep + pformat(user_info))
    return user_info


def print_tweet_urls(zip_path, pattern=None):
    """Print URLs of tweets in a ZIP archive
    """
    logging.info(f'Print URLs of tweets in a ZIP archive: {zip_path}')
    _validate_files(zip_path=zip_path)
    user_info = _extract_user_info(zip_path=zip_path)
    if isinstance(user_info, list):
        username = user_info[0]['account']['username']
    elif isinstance(user_info, dict):
        username = user_info['screen_name']
    else:
        raise RuntimeError('invalid user info')
    print(
        *[
            f'https://twitter.com/{username}/status/{i}'
            for i in _extract_tweet_ids(zip_path=zip_path, pattern=pattern)
        ],
        sep=os.linesep
    )


def delete_tweets(zip_path, cred_yml_path, ignore_errors=False, pattern=None):
    """Delete tweets on Twitter
    """
    logging.info(f'Delete tweets in a ZIP archive: {zip_path}')
    _validate_files(zip_path=zip_path, yml_path=cred_yml_path)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    tw_session = _create_session(yml_path=cred_yml_path)
    n_succeeded = 0
    n_failed = 0
    print('Start to delete tweets on Twitter.')
    for id in _extract_tweet_ids(zip_path=zip_path, pattern=pattern):
        req = f'https://api.twitter.com/2/tweets/{id}'
        response = tw_session.delete(req)
        print(f'  POST {req} => {response.status_code}')
        logging.debug(f'response:{os.linesep}{response.json()}')
        if response.status_code == 200:
            n_succeeded += 1
            logging.info(f'{response.status_code}: HTTP request was received.')
        else:
            n_failed += 1
            warn = (
                f'{response.status_code}: URL was not found.'
                if response.status_code == 404
                else f'{response.status_code}: HTTP request failed.'
            )
            if ignore_errors:
                logging.warning(warn)
            else:
                raise RuntimeError(warn)
    print(
        '{0} {1} deleted on Twitter.{2}'.format(
            n_succeeded, ('tweets were' if n_succeeded > 1 else 'tweet was'),
            (
                f' (succeeded: {n_succeeded}, failed: {n_failed})'
                if ignore_errors else ''
            )
        )
    )


def _create_session(yml_path):
    logging.info('Create a Twitter session.')
    with open(yml_path) as f:
        cr = yaml.load(f, Loader=yaml.FullLoader)
    logging.debug(f'cr: {cr}')
    if cr.get('access_token') and cr.get('access_token_secret'):
        return OAuth1Session(
            client_key=cr['consumer_key'], client_secret=cr['consumer_secret'],
            resource_owner_key=cr['access_token'],
            resource_owner_secret=cr['access_token_secret']
        )
    else:
        req_session = OAuth1Session(
            client_key=cr['consumer_key'], client_secret=cr['consumer_secret']
        )
        req_response = req_session.post(
            'https://api.twitter.com/oauth/request_token',
            params={'oauth_callback': cr['callback_url']}
        )
        logging.debug(f'req_response: {req_response}')
        logging.info(f'req_response.text: {req_response.text}')
        try:
            req_token_dict = dict([
                s.split('=', maxsplit=1) for s in req_response.text.split('&')
            ])
        except ValueError as e:
            logging.error(req_response.text)
            raise e
        else:
            logging.debug(f'req_token_dict: {req_token_dict}')
            assert 'oauth_token' in req_token_dict, req_response.text
        print(
            'Please go here and authorize:',
            'https://api.twitter.com/oauth/authenticate?oauth_token={}'.format(
                req_token_dict['oauth_token']
            )
        )
        oauth_verifier = input('Paste the OAuth verifier here: ')
        acc_session = OAuth1Session(
            client_key=cr['consumer_key'], client_secret=cr['consumer_secret'],
            resource_owner_key=req_token_dict['oauth_token'],
            resource_owner_secret=oauth_verifier
        )
        acc_response = acc_session.post(
            'https://api.twitter.com/oauth/access_token',
            params={'oauth_verifier': oauth_verifier}
        )
        logging.debug(f'acc_response: {acc_response}')
        logging.info(f'acc_response.text: {acc_response.text}')
        try:
            acc_token_dict = dict([
                s.split('=', maxsplit=1) for s in acc_response.text.split('&')
            ])
        except ValueError as e:
            logging.error(acc_response.text)
            raise e
        else:
            logging.debug(f'acc_token_dict: {acc_token_dict}')
            for k in ['oauth_token', 'oauth_token_secret']:
                assert k in acc_token_dict, acc_response.text
        return OAuth1Session(
            client_key=cr['consumer_key'], client_secret=cr['consumer_secret'],
            resource_owner_key=acc_token_dict['oauth_token'],
            resource_owner_secret=acc_token_dict['oauth_token_secret']
        )


def _extract_tweet_ids(zip_path, pattern=None):
    """Extract tweet IDs
    """
    with ZipFile(zip_path) as zf:
        name_set = set(zf.namelist())
        if 'data/tweets.js' in name_set:
            tweets = json.loads(
                re.sub(
                    r'^[^=]+=', '', zf.read('data/tweets.js').decode('utf-8')
                )
            )
            for d in tweets:
                tw = d['tweet']
                if pattern is None or re.search(pattern, tw['full_text']):
                    yield tw['id']
        elif 'data/tweet.js' in name_set:
            tweets = json.loads(
                re.sub(
                    r'^[^=]+=', '', zf.read('data/tweet.js').decode('utf-8')
                )
            )
            for d in tweets:
                tw = d['tweet']
                if pattern is None or re.search(pattern, tw['full_text']):
                    yield tw['id']
        elif {n for n in name_set if n.startswith('data/js/tweets/')}:
            tw_js_names = [
                z.filename for z in zf.infolist()
                if z.filename.startswith('data/js/tweets')
            ]
            logging.debug('tw_js_names:' + os.linesep + pformat(tw_js_names))
            for js in tw_js_names:
                for d in _extract_tweets_from_old_zip(zf, js):
                    if pattern is None or re.search(pattern, d['text']):
                        yield d['id']
        else:
            raise ValueError('tweet detection failed.')


def _extract_tweets_from_old_zip(zipfile, zipinfo):
    """Read zipinfo from zipfile with JSON tweets and return a dict list.
    """
    return json.loads(
        re.sub(r'^[^=]+=', '', zipfile.read(zipinfo).decode('utf-8'))
    )
