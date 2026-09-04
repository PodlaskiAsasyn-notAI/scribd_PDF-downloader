import requests
import re
from pathlib import Path


class Downloader:
    def __init__(self, url: str):
        self.url = url
        txt = re.search(r"/\d{9}/", self.url)
        if txt is None:
            raise Exception("ID number was not found")
        self._data_name = txt.group().strip('/')
        self.dir = Path()
        self.create_dir()
        self._main_html = self.dir / self._data_name
        self._main_html = self._main_html.with_suffix(".txt")

    def create_dir(self):
        self.dir = self.dir.cwd() / 'cache' / self._data_name
        if not self.dir.exists():
            self.dir.mkdir(parents=True)


    @staticmethod
    def save_file(filepath: Path, contents, mode="w"):
        with open(filepath.as_uri(), mode=f"{mode}", encoding="utf-8") as file:
            for line in contents:
                line = line + "\n"
                file.write(line)

    @staticmethod
    def read_file(filepath: Path, mode="r"):
        if not filepath.exists():
            print(f"file: {filepath.as_uri()} does not exist.")
            return None
        try:
            with open(filepath.as_uri(), mode=f"{mode}", encoding="utf-8") as file:
                output = file.readlines()
                return output
        except Exception:
            return None

    @staticmethod
    def request_url(url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"could not request for {url} \nstatus code: {response.status_code}")
        return response

    def get_page_html(self):
        Downloader.read_file(self._main_html)
        data = Downloader.request_url(self.url)
        lines = []
        if data is not None:
            return data
        else:
            data = requests.get(url).content.splitlines()
            for line in data:
                lines.append(str(line))
            Downloader.save_file(filename, lines)
            return data

    def filter_lines(self):
        for line in self.data:
            txt = re.search(r"https://\S*.jsonp", line)
            if txt:
                # print(txt.group())
                json_response = requests.get(f"{txt.group()}")
                jpg_url = re.search(r"http\S*.jpg", str(json_response.content))
                if jpg_url:
                    self.jpg_urls.append(jpg_url.group())
                    print(jpg_url.group())

    def download_jpg(self):
        counter = 0
        for i in range(10):
            counter += 1
            response = requests.get(f"{self.jpg_urls[i]}")
            with open(f"./{self._data_name}/{counter}.jpg", "wb") as file:
                file.write(response.content)


        # for url in self.jpg_urls:
        #     counter += 1
        #     response = requests.get("url")
        #     with open(f"./{self.data_name}/{counter}.jpg", "wb") as file:
        #         file.write(response.content)



a = Downloader("https://www.scribd.com/document/699509118/matematyka-zbio-r-zadan?_gl=1*11rp2yn*_up*MQ..*_ga*MTUxODM4MDA4LjE3ODgzNzU3MTk.*_ga_Z4ZC50DED6*czE3ODgzNzU3MTgkbzEkZzEkdDE3ODgzNzU3MTgkajYwJGwwJGgw*_ga_8KZ8BV0P5W*czE3ODgzNzU3MTgkbzEkZzEkdDE3ODgzNzU3MTgkajYwJGwwJGgw")
a.filter_lines()
pass
a.download_jpg()

# Downloader.save_file("testfile", ['a','b','c'])

# b = "string"
# b.``
pass


