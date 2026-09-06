import argparse
import re
import sys
from pathlib import Path

import progressbar
from PIL import Image

from classes import Downloader


def main(uri, output=None):
    # uri = "https://www.scribd.com/document/699509118/matematyka-zbio-r-zadan?_gl=1*11rp2yn*_up*MQ..*_ga*MTUxODM4MDA4LjE3ODgzNzU3MTk.*_ga_Z4ZC50DED6*czE3ODgzNzU3MTgkbzEkZzEkdDE3ODgzNzU3MTgkajYwJGwwJGgw*_ga_8KZ8BV0P5W*czE3ODgzNzU3MTgkbzEkZzEkdDE3ODgzNzU3MTgkajYwJGwwJGgw&v=0.573"
    downloader = Downloader(uri)
    if not downloader.dir.exists():
        downloader.create_dir()

    if output is None:
        output = Path(f"./{downloader._data_name}.pdf")

    # getting html code
    print("Getting html code...")
    html_cache = Downloader.read_file(downloader.main_html_path)
    if html_cache:
        html_str = html_cache
    else:
        html_response = Downloader.request_url(downloader.url)
        html_lines = html_response.content.splitlines()
        html_str = [str(line) for line in html_lines]
        Downloader.save_file(downloader.main_html_path, html_str)
    print("Done")

    # filtering html lines
    print("Filtering html lines...")
    json_uris = []
    for line in html_str:
        txt = re.search(r"https://\S*.jsonp", line)
        if txt:
            json_uris.append(txt.group())
    print("Done")

    # downloading jpg
    prog_bar = progressbar.ProgressBar(desc="downloading jpg", min_value=1, max_value=len(json_uris))

    jpg_paths = []

    for i, uri in enumerate(json_uris):
        jpg_path = downloader.dir.joinpath(f"{i}.jpg")
        jpg_paths.append(jpg_path)
        if jpg_path.exists():
            continue
        json_uri = uri
        json_txt = str(Downloader.request_url(json_uri).content)
        jpg_url = re.search(r"http\S*.jpg", json_txt)
        if jpg_url:
            jpg_response = Downloader.request_url(jpg_url.group())

            Downloader.save_file(jpg_path, jpg_response.content, mode="wb")

        prog_bar.update(i + 1)

    # creating pdf
    print("Creating pdf...")
    obrazy = [Image.open(p).convert("RGB") for p in jpg_paths]

    if obrazy:
        obrazy[0].save(output, save_all=True, append_images=obrazy[1:])
        print("PDF ready")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("scribd_uri", help="URI from SCRIBD page")
    parser.add_argument("--output", help="Path to output location")
    args = parser.parse_args()
    main(args.scribd_uri, args.output)
    sys.exit()
