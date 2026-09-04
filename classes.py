import requests
import re
from pathlib import Path


class Downloader:
    def __init__(self, url: str):
        self.url = url
        txt = re.search(r"/\d{9}/", self.url).group()
        if txt is None:
            raise Exception("ID number was not found")
        self.data_name = txt.replace("/", "")
        self.data = Downloader.download_url(self.url, self.data_name)
        self.jpg_urls = []
        dir_path = Path(self.data_name)
        try:
            dir_path.mkdir()
        except FileExistsError:
            pass


    @staticmethod
    def save_file(filename, contents):
        with open(f"./cache/{filename}.txt", "w", encoding="utf-8") as file:
            for line in contents:
                line = line + "\n"
                file.write(line)

    @staticmethod
    def save_file_bin(filename, contents):
        with open(f"./cache/{filename}.txt", "wb", encoding="utf-8") as file:
            for line in contents:
                line = line + "\n"
                file.write(line)

    @staticmethod
    def read_file(filename):
        try:
            with open(f"./cache/{filename}.txt", "r", encoding="utf-8") as file:
                output = file.readlines()
                return output
        except Exception:
            return None

    @staticmethod
    def download_url(url, filename):
        data = Downloader.read_file(filename)
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
            with open(f"./{self.data_name}/{counter}.jpg", "wb") as file:
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


