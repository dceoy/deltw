#!/usr/bin/env python

import argparse
from . import __version__, __description__
from .cleaner import create_session, write_credential_template,\
                     extract_tweet_ids, delete_tweets


def parse_options(default_credentials):
    parser = argparse.ArgumentParser(
        prog='deltw',
        description=__description__
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s {}'.format(__version__)
    )
    parser.add_argument(
        '--init',
        dest='init',
        action='store_true',
        help='Write `%s` as a YAML template for Twitter credentials'
             % default_credentials
    )
    parser.add_argument(
        '--test-print',
        dest='test_print',
        action='store_true',
        help='Print requests to delete tweets from Twitter and exit'
    )
    parser.add_argument(
        '--credentials',
        dest='credentials',
        default=default_credentials,
        metavar='YAML',
        help='Read Twitter credentials from a YAML file [default: %s]'
             % default_credentials
    )
    parser.add_argument(
        '--archive',
        dest='zip_archive',
        metavar='ZIP',
        help='a ZIP file of Twitter archive containing tweets to delete'
    )
    return parser.parse_args()


def main(default_credentials='tw_credentials.yml'):
    arg = parse_options(default_credentials)
    if arg.init:
        write_credential_template(default_credentials)
    else:
        delete_tweets(create_session(arg.credentials),
                      extract_tweet_ids(arg.zip_archive),
                      arg.test_print)


if __name__ == '__main__':
    main()
