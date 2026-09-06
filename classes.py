import re
from pathlib import Path

import requests


class Downloader:
    def __init__(self, url: str):
        self.url = url
        txt = re.search(r"/\d{9}/", self.url)
        if txt is None:
            raise Exception("ID number was not found")
        self._data_name = txt.group().strip('/')
        self.dir = Path()
        self.create_dir()
        self.main_html_path = self.dir / self._data_name
        self.main_html_path = self.main_html_path.with_suffix(".txt")

    def create_dir(self):
        self.dir = self.dir.cwd() / 'cache' / self._data_name
        if not self.dir.exists():
            self.dir.mkdir(parents=True)

    @staticmethod
    def save_file(filepath: Path, contents, mode="w"):
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if "b" in mode:
            # Zapis binarny (np. obrazy, PDF-y) - przekazujemy sam filepath, bez .as_uri()
            with open(filepath, mode=mode) as file:
                file.write(contents)
        else:
            # Zapis tekstowy
            with open(filepath, mode=mode, encoding="utf-8") as file:
                if isinstance(contents, (list, tuple)):
                    for line in contents:
                        file.write(f"{line}\n")
                else:
                    file.write(contents)

    @staticmethod
    def read_file(filepath: Path, mode="r"):
        if not filepath.exists():
            # print(f"file: {filepath.as_uri()} does not exist.")
            return None
        try:
            with open(filepath, mode=f"{mode}", encoding="utf-8") as file:
                output = file.readlines()
                return output
        except Exception as e:
            # return None
            raise Exception(e)

    @staticmethod
    def request_url(url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"could not request for {url} \nstatus code: {response.status_code}")
        return response

    def download_jpg(self):
        counter = 0
        for i in range(10):
            counter += 1
            response = requests.get(f"{self.jpg_urls[i]}")
            with open(f"./{self._data_name}/{counter}.jpg", "wb") as file:
                file.write(response.content)

