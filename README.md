# del-tw

Ad-hoc Twitter Client to Delete Tweets by Status ID

Setup of a Client
-----------------

```sh
$ pip install -U requests_oauthlib
$ git clone https://github.com/dceoy/del-tw.git
$ cd del-tw
```

Collection of Tweet Data
------------------------

Unzip an archive file

```sh
$ mkdir archive data
$ cd archive
$ unzip /path/to/your_twitter_archive.zip
$ cd -
```

Gather tweet data to a json file

```sh
$ cat archive/data/js/tweets/*.js | sed -e 's/^Grailbird.*$/\[/' | sed -e 's/Grailbird.*$/,/g' > data/tweets.json
$ echo ']' >> data/tweets.json
```

Deletion of Tweets
------------------

Set credentials.json

```sh
$ cp template_credentials.json credentials.json
$ vi credentials.json   # => Enter keys
```

Delete tweets by status id

```sh
$ python delete_tw.py data/tweets.json
```
