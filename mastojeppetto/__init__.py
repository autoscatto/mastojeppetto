import argparse
import requests
import logging
import sys
import concurrent.futures
from urllib.parse import urlparse
import os
VERSION = "0.0.2"

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


PATH = ""
CONCURRENCY = 4
TEXT = True
TEXTFILE = "emoji.txt"
ENDPOINT = "/api/v1/custom_emojis"
VERBOSE = False


def th_downloader(data, path, verbose=False):
    try:
        url = data.get('static_url')
        fname = urlparse(url).path.split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        open("{}/{}".format(path, fname), 'wb').write(r.content)
        if verbose:
            logging.info("Downloaded {shortcode} in {fname}".format(shortcode=data.get("shortcode"), fname=fname))
        return data.get("shortcode"), fname
    except Exception as e:
        if verbose:
            logging.info("Downloaded {shortcode} failed: [{error}]".format(shortcode=data.get("shortcode"),
                                                                              error=e.__repr__()))


def download_all(url, path=PATH, concurrency=CONCURRENCY, text=TEXT, endpoint=ENDPOINT, verbose=VERBOSE):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)


    try:
        r = requests.get("{base}{apiendpoint}".format(base=url, apiendpoint=endpoint))
    except requests.exceptions.MissingSchema:
        new_url = "https://{base}{apiendpoint}".format(base=url, apiendpoint=endpoint)
        logging.info("Missing Url Schema, trying {new_url}".format(new_url=new_url))
        r = requests.get(new_url)

    if r.ok:
        try:
            data = r.json()
            hostname = urlparse(r.url).hostname
            base = "/tmp/{}".format(hostname) if path == "" else path
            download_path = os.path.normpath(base)
            logging.info("Download path: \"{path}\"".format(path=download_path))

            if not os.path.exists(download_path):

                logging.info("Download path \"{path}\" not exist, mkdir".format(path=download_path))
                os.makedirs(download_path)

            logging.info("Starting {concurrency} concurrent executor".format(concurrency=concurrency))

            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
                # Start the load operations and mark each future with its URL
                future_to_url = {executor.submit(th_downloader, j, download_path): j for j in data}
                oks = []
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        logging.info("{url} generated an exception: {ex}".format(url=url, ex=exc.__repr__()))
                    else:
                        oks.append(data)


            if text:
                with open("{path}/{textfile}".format(path=download_path, textfile=TEXTFILE), "w") as textf:
                    textf.writelines([
                        "{shortcode}, /emoji/{fname}\n".format(shortcode=shortcode,
                                                             fname=fname) for shortcode, fname in oks])

            logging.info("ENDED! check your emojis in {}".format(download_path))
            return data

        except Exception as e:
            logging.error("Connection error to mastodon base url {url}".format(url=url))
            print(e)
            sys.exit(1)

    else:
        logging.error("Connection error to mastodon base url {url}".format(url=url))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Mastodon (or Pleroma) base url")
    parser.add_argument("--path",
                        help="download destination [default: /tmp/${domainname}]",
                        type=str,
                        default=PATH)
    parser.add_argument("--concurrency",
                        help="how many parallel download processes will start [default: 4]",
                        type=int,
                        default=CONCURRENCY)
    parser.add_argument("--text",
                        help="generate also {} (for Pleroma) [default: True]".format(TEXTFILE),
                        type=bool,
                        default=TEXT)
    parser.add_argument("--endpoint",
                        help="custom api emoji endpoint (usually works without changes) "
                             "[default: \"/api/v1/custom_emojis\"]",
                        type=str,
                        default=ENDPOINT)
    parser.add_argument("--verbose",
                        help="be verbose [default: False]",
                        action="store_true")
    args = parser.parse_args()

    download_all(url=args.url,
                 path=args.path,
                 concurrency=args.concurrency,
                 text=args.text,
                 endpoint=args.endpoint,
                 verbose=args.verbose)
