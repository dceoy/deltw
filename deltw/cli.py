#!/usr/bin/env python

import os
import yaml
import click
from . import __version__
from .cleaner import create_session, extract_tweet_ids, delete_tweets

credentials_yml = 'tw_credentials.yml'


def write_credential_template(ctx, param, value):
    yml = param.default
    if os.path.exists(yml):
        click.echo('%s already exists' % yml)
    else:
        with open(yml, 'w') as f:
            f.write(yaml.dump({'consumer_key': '',
                               'consumer_secret': '',
                               'access_token': '',
                               'access_token_secret': ''},
                              default_flow_style=False))
    ctx.exit()


@click.command()
@click.option(
    '--init',
    is_flag=True,
    default=credentials_yml,
    callback=write_credential_template,
    help='Write a YAML template `%s` for Twitter credentials'
         % credentials_yml
)
@click.option(
    '--credentials',
    metavar='YAML',
    show_default=True,
    default=credentials_yml,
    help='Read Twitter credentials from a YAML file'
)
@click.version_option(
    version=__version__
)
@click.argument(
    'archive_zip',
    metavar='tweet_archive.zip',
)
def main(credentials, archive_zip):
    """Delete all of archived tweets from Twitter."""
    delete_tweets(create_session(credentials),
                  extract_tweet_ids(archive_zip))


if __name__ == '__main__':
    main()
