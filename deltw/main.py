#!/usr/bin/env python

import logging
import os
from pprint import pformat
from .util import parse_options, set_log_config, write_credentials_template
from .cleaner import print_tweet_urls, print_user_details, delete_tweets


def main():
    args = parse_options()
    set_log_config(args=args)
    logging.debug('args:{0}{1}'.format(os.linesep, pformat(vars(args))))
    if args.subcommand == 'init':
        write_credentials_template()
    elif args.subcommand == 'user':
        print_user_details(zip_path=args.zip_path)
    elif args.subcommand == 'urls':
        print_tweet_urls(zip_path=args.zip_path, regex=args.regex)
    elif args.subcommand == 'delete':
        delete_tweets(
            zip_path=args.zip_path,
            cred_yml_path=args.cred_yml_path,
            ignore_error=args.ignore_error,
            regex=args.regex
        )
