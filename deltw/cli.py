#!/usr/bin/env python

import argparse
from . import __version__
from .session import create_session
from .cleaner import list_tweet_ids, delete_tweets


def parse_arg_path():
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
        'archive_zip',
        metavar='tweet_archive.zip',
        help='a zip file of tweet archive containing tweets to delete'
    )
    parser.add_argument(
        '--credentials',
        dest='credentials_yml',
        default='credentials.yml',
        help='a yaml file for Twitter credentials (default: credentials.yml)'
    )
    return parser.parse_args()


def main():
    args = parse_arg_path()
    tw = create_session(args.credentials_yml)
    [delete_tweets(tw, id)
     for id in list_tweet_ids(args.archive_zip)]


if __name__ == '__main__':
    main()
