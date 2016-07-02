deltw
=====

Ad-hoc Twitter Client to Delete Tweets by Status ID

Setup of a Client
-----------------

Python (2.x or 3.x) is required.

```sh
$ pip install -U requests_oauthlib
$ git clone https://github.com/dceoy/del-tw.git
$ cd del-tw
```

Deletion of Tweets
------------------

Set credentials.json

```sh
$ cp template_credentials.json credentials.json
$ vi credentials.json   # => Enter keys
```

Delete archived tweets

```sh
$ python delete_tw.py /path/to/tweet_archive.zip
```
