class Downloader:
    def __init__(self, queue, urls, client_session, save_file):
        self.queue = queue
        self.urls = urls
        self.http_session = client_session
        self.save_file = save_file

    async def save_file_and_set_status_done(self, url, file_content):
        file_name = url.split('/')[-1]
        saved_path = await self.save_file(file_name, file_content)
        self.urls.set_status_done(url, saved_path)

    async def fetch_url(self, url):
        # set url as download
        self.urls.set_status_downloading(url)
        async with self.http_session.get(url) as response:
            if response.status != 200:
                self.urls.set_status_error(url)
                return
            file_content = await response.read()
        await self.save_file_and_set_status_done(url, file_content)

    async def fetch_from_queue(self):
        url = await self.queue.get()
        await self.fetch_url(url)

    async def run(self):
        while True:
            await self.fetch_from_queue()
