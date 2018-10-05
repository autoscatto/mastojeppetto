# mastojeppetto


Mastodon (and pleroma) python3 emoji downloader 


## Badges
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/autoscatto) [![Build Status](https://travis-ci.org/autoscatto/mastojeppetto.svg?branch=master)](https://travis-ci.org/autoscatto/mastojeppetto)

### installation
#### from src:
```bash
git clone https://github.com/autoscatto/mastojeppetto
cd mastojeppetto
python setup.py install
```

#### from pip:
```bash
pip3 install mastojeppetto
```

### usage
```
mastojeppetto [-h] [--path PATH] [--concurrency CONCURRENCY]
                     [--text TEXT] [--endpoint ENDPOINT] [--verbose]
                     url

positional arguments:
  url                   Mastodon (or Pleroma) base url

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           download destination [default: /tmp/${domainname}]
  --concurrency CONCURRENCY
                        how many parallel download processes will start
                        [default: 4]
  --text TEXT           generate also emoji.txt (for Pleroma) [default: True]
  --endpoint ENDPOINT   custom api emoji endpoint (usually works without
                        changes) [default: "/api/v1/custom_emojis"]
  --verbose             be verbose [default: False]
```