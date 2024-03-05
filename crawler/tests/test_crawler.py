from unittest.mock import patch
from crawler.main import build_urls_from_file
from crawler.urls import UrlStatus

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