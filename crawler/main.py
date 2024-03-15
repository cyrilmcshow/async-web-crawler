from os import getenv
from crawler.files import read_lines_from_file, save_file
from crawler.urls import Urls
from crawler.app import build_application
from crawler.downloader import Downloader
from aiohttp import web
from aiohttp.client import ClientSession
from asyncio import Queue, gather, run
from functools import partial


def build_urls_from_file(path):
    file_contents = read_lines_from_file(path)
    urls = Urls()
    urls.add(file_contents)
    return urls


async def main():
    urls_file_path = '../urls.txt'
    if urls_file_path is None:
        raise ValueError('URLS_FILE_PATH environment variable must be set')

    workers = int(getenv('WORKERS', 1))

    print(f'URLS_FILE_PATH={urls_file_path}')
    print(f'WORKERS={workers}')

    urls = build_urls_from_file(urls_file_path)
    app = build_application()
    app['urls'] = urls
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8000)

    queue = Queue()
    for url in urls.get_urls():
        await queue.put(url['value'])
    coros = []
    async with ClientSession() as session:
        downloader = Downloader(
            queue=queue,
            urls=urls,
            client_session=session,
            save_file=partial(save_file, 'downloads'),
        )
        coros.append(site.start())
        for _ in range(workers):
            coros.append(downloader.run())
        print('starting service at http://localhost:8000')
        await gather(*coros)


if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        print('bye')
