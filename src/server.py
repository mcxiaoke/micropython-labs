import picoweb
import sys
import os
import re
import gpio
import ulogging as logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('server')

site = picoweb.WebApp(__name__)
site.mount("/io", gpio.app)


@site.route(re.compile("^/(\S+\.py)$"))
def modules(req, resp):
    logger.info('path:%s', req.path)
    yield from picoweb.start_response(resp, content_type="text/plain; charset=utf-8")
    try:
        f = open(req.path, 'r')
        f.readline()
        f.seek(0)
        logger.info('open file: [%s]', req.path)
    except:
        try:
            f = open('/lib/{}'.format(req.path), 'r')
            f.readline()
            f.seek(0)
            logger.info('open file: [/lib/%s]', req.path)
        except:
            f = None
    if not f:
        yield from picoweb.start_response(resp, content_type="text/plain; charset=utf-8", status=404)
        yield from resp.awrite("404 NOT FOUND")
    else:
        yield from resp.awrite(f.read())
        f.close()


@site.route('/')
def index(req, resp):
    req.parse_qs()
    logger.info("%s,%s,%s", req.method, req.path, req.form)
    yield from picoweb.start_response(resp)
    yield from resp.awrite("<h2>MicroPython Modules: </h2>")
    yield from resp.awrite("<ul>")
    for key in sys.modules.keys():
        module = sys.modules[key]
        try:
            lib_path = module.__file__
        except:
            lib_path = module.__name__
        yield from resp.awrite("<li>")
        yield from resp.awrite("{}: <a href='{}'>{}</a>".format(key, lib_path, lib_path))
        yield from resp.awrite("</li>")
    yield from resp.awrite("</ul>")


def start():
    logger.info('web running on port 80')
    site.run(host='0.0.0.0', port=80)
