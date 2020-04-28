deltw
=====

Twitter Tweet cleaner to delete archived tweets using a [Twitter Archive](https://support.twitter.com/articles/20170160) file

Twitter API: v1.1

[![wercker status](https://app.wercker.com/status/3a8a079c05b47177c33b968ab3f1bdd9/s/master "wercker status")](https://app.wercker.com/project/byKey/3a8a079c05b47177c33b968ab3f1bdd9)
![Upload Python Package](https://github.com/dceoy/deltw/workflows/Upload%20Python%20Package/badge.svg)

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
