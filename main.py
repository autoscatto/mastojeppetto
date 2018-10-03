import argparse
import requests
import logging
import sys
import concurrent.futures
from urllib.parse import urlparse
import oss

parser = argparse.ArgumentParser()
parser.add_argument("url", help="Mastodon (or Pleroma) base url")
parser.add_argument("--path",
                    help="download destination [default: /tmp/${domainname}]",
                    type=str,
                    default="")
parser.add_argument("--concurrency",
                    help="how many parallel download processes will start [default: 4]",
                    type=int,
                    default=4)
parser.add_argument("--text",
                    help="generate also emoji.txt (for Pleroma) [default: True]",
                    type=bool,
                    default=True)
parser.add_argument("--endpoint",
                    help="custom api emoji endpoint (usually works without changes) "
                         "[default: \"/api/v1/custom_emojis\"]",
                    type=str,
                    default="/api/v1/custom_emojis")
parser.add_argument("--verbose",
                    help="be verbose [default: False]",
                    type=bool,
                    default=False)
args = parser.parse_args()


def emoji_downloader(data, path):
    try:
        url = data.get('static_url')
        fname = urlparse(url).path.split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        open("{}/{}".format(path, fname), 'wb').write(r.content)
        return "{}, /emoji/{}".format(data.get("shortcode"), fname)
    except:
        pass

r = None
try:
    r = requests.get("{base}{apiendpoint}".format(base=args.url, apiendpoint=args.endpoint))
except requests.exceptions.MissingSchema:
    r = requests.get("https://{base}{apiendpoint}".format(base=args.url, apiendpoint=args.endpoint))

if r.ok:
    try:
        data = r.json()
        hostname = urlparse(r.url).hostname
        base = "/tmp/{}".format(hostname) if args.path == "" else args.path
        download_path = os.path.normpath(base)
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(emoji_downloader, j, download_path): j for j in data}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    print(data)
    except Exception as e:
        logging.error("Connection error to mastodon base url {url}".format(url=args.url))
        print(e)
        sys.exit(1)

else:
    logging.error("Connection error to mastodon base url {url}".format(url=args.url))


