from crawler.files import read_lines_from_file
from crawler.urls import Urls


def build_urls_from_file(path):
    file_contents = read_lines_from_file(path)
    urls = Urls()
    urls.add(file_contents)
    return urls
