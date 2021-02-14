from machine import Pin
import picoweb
import ure as re
from machine import Pin
import ulogging as logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('gpio')


def to_int(s):
    try:
        return int(s)
    except Exception as e:
        return -1


app = picoweb.WebApp(__name__)


@app.route('/')
def gpio_index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Welcome to GPIO API")


@app.route(re.compile("^/(\\d+)(\\?\\S*)?$"))
def gpio_handler(req, resp):
    '''
    POST|GET /gpio/10?action=mode&value=in|out - pinMode()\n\
    POST|GET /gpio/10?action=write&value=1 - digitalWrite()\n\
    POST|GET /gpio/10?action=awrite&value=99 - analogWrite()\n\
    GET /gpio/10?action=read - digitalRead()\n\
    GET /gpio/10?action=aread - analogRead()\n\
    '''

    req.parse_qs()
    ps = req.path.split('/')
    pin = to_int(ps[1])
    action = req.form.get('action')
    value = req.form.get('value')
    logger.info("%s %s [%s]", req.method, req.path, req.qs)
    logger.info("pin=%d,action=%s,value=%s", pin, action, value)
    yield from picoweb.start_response(resp)
    yield from resp.awrite("%s %s [%s]<br />" % (req.method, req.path, req.qs))
    yield from resp.awrite("pin=%d,action=%s,value=%s<br />" %
                           (pin, action, value))


if __name__ == "__main__":
    app.run(debug=True)
