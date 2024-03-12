from jinja2 import Environment, FileSystemLoader, select_autoescape
from aiohttp.web import Response, Application, get as set_get_handler
from crawler.urls import UrlStatus

env = Environment(
    loader=FileSystemLoader('crawler/templates'), autoescape=select_autoescape()
)


async def get_index(request):
    template = env.get_template('index.html')
    body = template.render(urls=request.app['urls'].get_urls())
    return Response(body=body, content_type='text/html')


def build_application():
    app = Application()
    app.add_routes([set_get_handler('/', get_index)])
    return app
