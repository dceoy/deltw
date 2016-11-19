deltw
=====

Tweet cleaner to delete archived tweets in [Twitter Archive](https://support.twitter.com/articles/20170160) from Twitter

Twitter API: v1.1

Installation
------------

Python 3 is required.

```sh
$ pip install -U git+https://github.com/dceoy/deltw
```

Usage
-----


1.  Download your [Twitter archive](https://support.twitter.com/articles/20170160) as a ZIP file.

2.  Set credentials to use Twitter API.

    ```sh
    $ deltw --init
    $ vi tw_credentials.yml  # => Enter keys
    ```

3.  Delete archived tweets in your Twitter archive from Twitter.

    ```sh
    $ deltw --credentials tw_credentials.yml --archive /path/to/tweet_archive.zip
    ```

Run `deltw --help` for more information about options.
