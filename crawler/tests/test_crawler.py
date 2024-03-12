import pytest, pytest_asyncio

from unittest.mock import patch
from asyncio.queues import Queue
from unittest.mock import AsyncMock

import pytest
from aiohttp.client import ClientResponse

from crawler.main import build_urls_from_file
from crawler.urls import UrlStatus, Urls
from crawler.downloader import Downloader

from crawler.app import build_application


class Session:
    def __init__(self, response_codes):
        self.response_codes = response_codes

    def get(self, url):
        response = AsyncMock(ClientResponse)
        expected_status, expected_body = self.response_codes[url]
        response.status = expected_status
        response.body = expected_body

        context_manager = AsyncMock()
        context_manager.__aenter__.return_value = response
        return context_manager


def test_build_urls_from_file():
    urls_file_path = 'testing_path.txt'
    with patch('crawler.main.read_lines_from_file') as mock:
        mock.return_value = [
            'https://example.com/image1.png',
            'https://example.com/image2.png'
        ]
        urls = build_urls_from_file(urls_file_path)

    assert len(urls.get_urls()) == 2
    written_urls = iter(urls.get_urls())
    url = next(written_urls)
    assert url['value'] == 'https://example.com/image1.png'
    assert url['status'] == UrlStatus.NEW

    url = next(written_urls)
    assert url['value'] == 'https://example.com/image2.png'
    assert url['status'] == UrlStatus.NEW


@pytest.mark.asyncio
async def test_fetch_urls():
    response_codes = {
        'https://example.com/image1.png': (200, b'image1.jpg'),
        'https://example.com/image2.png': (400, None)
    }
    client_session = Session(response_codes)
    urls = Urls()
    urls.add(['https://example.com/image1.png', 'https://example.com/image2.png'])
    queue = Queue()
    await queue.put('https://example.com/image1.png')
    await queue.put('https://example.com/image2.png')
    mock = AsyncMock()
    mock.return_value = 'downloads/image1.jpg'

    downloader = Downloader(queue, urls, client_session, mock)
    await downloader.fetch_from_queue()
    url = urls.url_states['https://example.com/image1.png']
    assert url['status'] == UrlStatus.DONE
    assert url['download_url'] == 'downloads/image1.jpg'

    await downloader.fetch_from_queue()
    url = urls.url_states['https://example.com/image2.png']
    assert url['status'] == UrlStatus.ERROR

