#!/usr/bin/env python

import argparse
from . import __version__
from .cleaner import create_session, write_credential_template,\
                     extract_tweet_ids, delete_tweets


def parse_options(default_credentials):
    parser = argparse.ArgumentParser(
        prog='deltw',
        description='Delete all of archived tweets from Twitter.'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s ' + __version__
    )
    parser.add_argument(
        '--init',
        action='store_true',
        help='Write `%s` as a YAML template for Twitter credentials'
             % default_credentials
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
                      extract_tweet_ids(arg.zip_archive))


if __name__ == '__main__':
    main()
