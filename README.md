deltw
=====

Tweet Cleaner using Twitter Archive

Setup of a Client
-----------------

Python (2.x or 3.x) is required.

```sh
$ git clone https://github.com/dceoy/deltw.git
$ pip install deltw
```

Deletion of Tweets
------------------

Set tw_credentials.yml

```sh
$ cp deltw/template_credentials.yml tw_credentials.yml
$ vi tw_credentials.yml  # => Enter keys
```

Delete archived tweets

```sh
$ deltw /path/to/tweet_archive.zip
```
