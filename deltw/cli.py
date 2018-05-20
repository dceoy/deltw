#!/usr/bin/env python

import argparse
from . import __version__, __description__
from .cleaner import delete_tweets, set_log_config, validate_args, \
    write_credential_template


def parse_options(default_credentials):
    parser = argparse.ArgumentParser(prog='deltw', description=__description__)
    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s {}'.format(__version__)
    )
    parser.add_argument(
        '--credentials', dest='credentials_yml', default=default_credentials,
        metavar='YAML', help=(
            'Path to a YAML file for Twitter credentials '
            '[default: {}]'.format(default_credentials)
        )
    )
    parser.add_argument(
        '--init', dest='init', action='store_true',
        help='Write `{}` as a YAML template for Twitter credentials'.format(
            default_credentials
        )
    )
    parser.add_argument(
        '--archive', dest='zip_archive', metavar='ZIP',
        help='Path to a ZIP file of Twitter archive including tweets to delete'
    )
    parser.add_argument(
        '--test-print', dest='test_print', action='store_true',
        help='Print requests to delete tweets from Twitter and exit'
    )
    parser.add_argument(
        '--ignore-error', dest='ignore_error', action='store_true',
        help='Ignore errors in HTTP requests'
    )
    parser.add_argument(
        '--text-pattern', dest='regex',
        help='Regex pattern of tweets to match'
    )
    log_parser = parser.add_mutually_exclusive_group()
    log_parser.add_argument(
        '--debug', dest='debug', action='store_true',
        help='Log with DEBUG level'
    )
    log_parser.add_argument(
        '--info', dest='info', action='store_true',
        help='Log with INFO level'
    )
    return parser.parse_args()


def main(default_credentials='tw_credentials.yml'):
    args = parse_options(default_credentials)
    set_log_config(args)
    validate_args(args)
    if args.init:
        write_credential_template(default_credentials)
    else:
        delete_tweets(
            credentials_yml=args.credentials_yml, zip_archive=args.zip_archive,
            test_print=args.test_print, ignore_error=args.ignore_error,
            regex=args.regex
        )
