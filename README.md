deltw
=====

Twitter Tweet cleaner to delete archived tweets using a [Twitter Archive](https://support.twitter.com/articles/20170160) file

Twitter API: v1.1

[![Test](https://github.com/dceoy/deltw/actions/workflows/test.yml/badge.svg)](https://github.com/dceoy/deltw/actions/workflows/test.yml)
[![Upload Python Package](https://github.com/dceoy/deltw/actions/workflows/python-publish.yml/badge.svg)](https://github.com/dceoy/deltw/actions/workflows/python-publish.yml)

Installation
------------

```sh
$ pip install -U deltw
```

Usage
-----


1.  Download your [Twitter archive](https://support.twitter.com/articles/20170160) as a ZIP file.

2.  Set credentials to use Twitter API.

    ```sh
    $ deltw init
    $ vi tw_credentials.yml  # => Enter keys
    ```

3.  Delete archived tweets in your Twitter archive on Twitter.

    ```sh
    $ deltw delete --credential tw_credentials.yml --archive /path/to/tweet_archive.zip
    ```

Run `deltw --help` for more information about options.
