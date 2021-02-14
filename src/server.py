import picoweb
import gpio
import ulogging as logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('server')

site = picoweb.WebApp(__name__)
site.mount("/gpio", gpio.app)

@site.route("/")
def index(req, resp):
    req.parse_qs()
    logger.info("%s,%s,%s", req.method, req.path, req.form)
    yield from picoweb.start_response(resp)
    yield from resp.awrite("<h1>Hello, World</h1>")


def start():
    logger.info('Server running on 8081')
    site.run(host='0.0.0.0')