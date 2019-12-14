#!/usr/bin/env python

import argparse
import logging
import os

import yaml

from . import __version__


class DeltwError(Exception):
    pass


def parse_options():
    parser = argparse.ArgumentParser(
        prog='deltw',
        description='Delete archived tweets on Twitter using Twitter Archive'
    )
    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s {}'.format(__version__)
    )

    subparsers = parser.add_subparsers(
        title='subcommands', dest='subcommand'
    )
    subparsers.add_parser(
        'init',
        help=(
            'Write a YAML template of Twitter credentials '
            'as `tw_credentials.yml`'
        )
    )
    _add_arch_args(subparsers.add_parser(
        'user', help='Extract user details from a ZIP file of Twitter Archive'
    ))
    _add_arch_args(subparsers.add_parser(
        'urls', help='Extract tweet URLs from a ZIP file of Twitter Archive'
    ))
    _add_del_args(_add_arch_args(subparsers.add_parser(
        'delete', help='Delete archived tweets on Twitter'
    )))

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


def _add_arch_args(subparser):
    subparser.add_argument(
        '--archive', dest='zip_path', required=True, metavar='ZIP',
        help='Path to a ZIP file of Twitter archive including tweets to delete'
    )
    subparser.add_argument(
        '--text-pattern', dest='regex',
        help='Regex pattern of tweets to match'
    )
    return subparser


def _add_del_args(subparser):
    subparser.add_argument(
        '--credential', dest='cred_yml_path', required=True, metavar='YAML',
        help='Path to a YAML file for Twitter credentials'
    )
    subparser.add_argument(
        '--ignore-error', dest='ignore_error', action='store_true',
        help='Ignore errors in HTTP requests'
    )
    return subparser


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


def write_credentials_template(default_yml='tw_credentials.yml'):
    if os.path.exists(default_yml):
        print('A file already exists: {}'.format(default_yml))
    else:
        print('Write YAML: {}'.format(default_yml))
        with open(default_yml, 'w') as f:
            f.write(yaml.dump(
                {
                    'consumer_key': '', 'consumer_secret': '',
                    'access_token': '', 'access_token_secret': ''
                },
                default_flow_style=False
            ))
