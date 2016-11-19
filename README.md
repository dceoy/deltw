deltw
=====

Tweet cleaner using [Twitter Archive](https://support.twitter.com/articles/20170160)

This tool extracts archived tweets, and deletes them from Twitter.

Installation
------------

Python 3 is required.

```sh
$ pip install git+https://github.com/dceoy/deltw
```

Usage
-----


1.  Downloading your [Twitter archive](https://support.twitter.com/articles/20170160)

2.  Set credentials to use Twitter API.

    ```sh
    $ deltw --init
    $ vi tw_credentials.yml  # => Enter keys
    ```

3.  Delete archived tweets

    ```sh
    $ deltw --credentials tw_credentials.yml /path/to/tweet_archive.zip
    ```

Run `deltw --help` for more information about options
