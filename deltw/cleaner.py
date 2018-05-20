#!/usr/bin/env python

import json
import logging
import os
import re
import signal
import yaml
from zipfile import ZipFile
from requests_oauthlib import OAuth1Session


class DeltwError(Exception):
    pass


def set_log_config(args):
    if args.debug:
        lv = logging.DEBUG
    elif args.info:
        lv = logging.INFO
    else:
        lv = logging.WARNING
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=lv
    )


def validate_args(args):
    logging.debug('args:{0}{1}'.format(os.linesep, args))
    if args.init:
        pass
    elif args.zip_archive:
        not_found = [p for p in [args.zip_archive, args.credentials_yml]
                     if not os.path.isfile(p)]
        if not_found:
            raise DeltwError('file not found: {}'.fromat(', '.join(not_found)))
        else:
            pass
    else:
        raise DeltwError('--init or --archive option is required.')


def write_credential_template(yml_path):
    if os.path.exists(yml_path):
        print('A file already exists: {}'.format(yml_path))
    else:
        logging.info('Write credential yaml: {}'.format(yml_path))
        with open(yml_path, 'w') as f:
            f.write(yaml.dump(
                {
                    'consumer_key': '', 'consumer_secret': '',
                    'access_token': '', 'access_token_secret': ''
                },
                default_flow_style=False
            ))


def _create_session(yml_path):
    logging.info('Create a Twitter session.')
    with open(yml_path) as f:
        cr = yaml.load(f)
    logging.debug('cr: {}'.format(cr))
    return OAuth1Session(
        cr['consumer_key'], cr['consumer_secret'],
        cr['access_token'], cr['access_token_secret']
    )


def _iter_tweet_files(zip_file):
    """Generator yielding files with tweets
    Args:
    - zip_file: instance of ZipFile

    Yields: instance of ZipInfo
    """
    for zip_info in zip_file.infolist():
        if zip_info.filename.startswith('data/js/tweets'):
            yield zip_info


def _decoded_tweets(zip_file, zip_info):
    """Read provided zip_info from zip_file with JSON tweets
     and return list of dict objects.
    """
    contents = zip_file.read(zip_info).decode('utf-8')
    json_str = re.sub(r'^Grailbird[^=]+=', '', contents)
    return json.loads(json_str)


def _filter_tweet_ids(zip_archive, regex=None):
    """Generates requests with filtered tweets
    """
    with ZipFile(zip_archive) as zf:
        for zip_info in _iter_tweet_files(zf):
            for tweet in _decoded_tweets(zf, zip_info):
                if regex is None or re.search(regex, tweet['text']):
                    yield tweet['id']


def _id2req(id):
    return 'https://api.twitter.com/1.1/statuses/destroy/{}.json'.format(id)


def delete_tweets(credentials_yml, zip_archive, test_print=False,
                  ignore_error=False, regex=None):
    logging.info('Delete tweets in an archive: {}'.format(zip_archive))
    tweet_ids = _filter_tweet_ids(zip_archive, regex)
    if test_print:
        print(*[_id2req(i) for i in tweet_ids], sep=os.linesep)
    else:
        tw_session = _create_session(yml_path=credentials_yml)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        print('Start to delete tweets.')
        n_succeeded = 0
        n_failed = 0
        for tw_id in tweet_ids:
            req = _id2req(tw_id)
            http_code = tw_session.post(req).status_code
            print('  POST {0} => {1}'.format(req, http_code))
            if http_code == 200:
                n_succeeded += 1
                logging.info(
                    '{}: HTTP request was received.'.format(http_code)
                )
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
        msg = '{0} {1} deleted.'.format(
            n_succeeded, ('tweets were' if n_succeeded > 1 else 'tweet was')
        )
        print(
            '{0} (succeeded: {1}, failed: {2})'.format(
                msg, n_succeeded, n_failed
            ) if ignore_error else msg
        )
