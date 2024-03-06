from enum import Enum


class UrlStatus(Enum):
    NEW = 'new'
    DOWNLOADING = 'downloading'
    ERROR = 'error'
    DONE = 'done'


class Urls:
    def __init__(self, url_states=None):
        self.url_states = url_states if url_states is not None else {}

    def add(self, urls):
        for url in urls:
            self.url_states[url] = {'value': url,
                                    'status': UrlStatus.NEW,
                                    'download_url': None
                                    }

    def get_urls(self):
        return list(self.url_states.values())

    def set_status_downloading(self, url):
        self.url_states[url]['status'] = UrlStatus.DOWNLOADING

    def set_status_error(self, url):
        self.url_states[url]['status'] = UrlStatus.ERROR

    def set_status_done(self, url, download_url=None):
        self.url_states[url]['status'] = UrlStatus.DONE
        self.url_states[url]['download_url'] = download_url
