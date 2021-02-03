#!/usr/bin/env python

import logging
import os
from pprint import pformat

from .cleaner import delete_tweets, print_tweet_urls, print_user_info
from .util import parse_options, write_credentials_template


def main():
    args = parse_options()
    _set_log_config(args=args)
    logging.debug('args:' + os.linesep + pformat(vars(args)))
    if args.subcommand == 'init':
        write_credentials_template()
    elif args.subcommand == 'user':
        print_user_info(zip_path=args.zip_path)
    elif args.subcommand == 'urls':
        print_tweet_urls(zip_path=args.zip_path, pattern=args.pattern)
    elif args.subcommand == 'delete':
        delete_tweets(
            zip_path=args.zip_path, cred_yml_path=args.cred_yml_path,
            ignore_errors=args.ignore_errors, pattern=args.pattern
        )


def _set_log_config(args):
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
