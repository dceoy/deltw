#!/usr/bin/env python

import argparse
from pathlib import Path

import yaml

from . import __version__


def parse_options():
    parser = argparse.ArgumentParser(
        prog='deltw',
        description='Delete archived tweets on Twitter using Twitter Archive'
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )

    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    subparsers.add_parser(
        'init',
        help=(
            'Write a YAML template of Twitter credentials '
            'as `tw_credentials.yml`'
        )
    )
    _add_arch_args(
        subparsers.add_parser(
            'user', help='Extract user info from a ZIP file of Twitter Archive'
        )
    )
    _add_arch_args(
        subparsers.add_parser(
            'urls',
            help='Extract tweet URLs from a ZIP file of Twitter Archive'
        )
    )
    _add_del_args(
        _add_arch_args(
            subparsers.add_parser(
                'delete', help='Delete archived tweets on Twitter'
            )
        )
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


def _add_arch_args(subparser):
    subparser.add_argument(
        '-a', '--archive', dest='zip_path', required=True, metavar='ZIP',
        help='Path to a ZIP file of Twitter archive including tweets to delete'
    )
    subparser.add_argument(
        '-t', '--text-pattern', dest='pattern',
        help='Select the tweets including the text pattern'
    )
    return subparser


def _add_del_args(subparser):
    subparser.add_argument(
        '-c', '--credential', dest='cred_yml_path', required=True,
        metavar='YAML', help='Path to a YAML file for Twitter credentials'
    )
    subparser.add_argument(
        '--ignore-errors', dest='ignore_errors', action='store_true',
        help='Ignore errors in HTTP requests'
    )
    return subparser


def write_credentials_template(default_yml='tw_credentials.yml'):
    if Path(default_yml).is_file():
        print(f'A file already exists:\t{default_yml}')
    else:
        print(f'Write YAML:\t{default_yml}')
        with open(default_yml, 'w') as f:
            f.write(
                yaml.dump(
                    {
                        'consumer_key': '', 'consumer_secret': '',
                        'access_token': '', 'access_token_secret': ''
                    },
                    default_flow_style=False
                )
            )
