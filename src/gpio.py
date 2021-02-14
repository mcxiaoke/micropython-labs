import picoweb
import re
from machine import Pin, ADC
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
    # HTTP GPIO Handler
    req.parse_qs()
    ps = req.path.split('/')
    pin = to_int(ps[1])
    action = req.form.get('action')
    value = to_int(req.form.get('value'))
    logger.info("gpio_handler: %s %s [%s]", req.method, req.path, req.qs)
    logger.info("gpio_handler: pin=%d,action=%s,value=%s", pin, action, value)
    yield from picoweb.start_response(resp)
    # GET /io/10?action=read - digitalRead()\n\
    if not action or action == 'read':
        # no action = read
        v = Pin(pin).value()
        yield from resp.awrite(str(v))
    # POST|GET /io/10?action=mode&value=in|out - pinMode()\n\
    elif action == 'mode':
        if value == 'in':
            p = Pin(pin, Pin.IN)
            yield from resp.awrite("in")
        elif value == 'out':
            p = Pin(pin, Pin.OUT)
            yield from resp.awrite("out")
        else:
            yield from resp.awrite("error:mode")
    # POST|GET /io/10?action=write&value=1 - digitalWrite()\n\
    elif action == 'write':
        if value < 0:
            yield from resp.awrite("error:write")
        else:
            p = Pin(pin, Pin.OUT)
            p.value(value)
            yield from resp.awrite(str(value))
    else:
        yield from resp.awrite("error:action")


@app.route(re.compile("^/.*$"))
def gpio_others(req, resp):
    logger.info('gpio_others: %s', req.path)
    yield from picoweb.start_response(resp)
    yield from resp.awrite(req.path)


if __name__ == "__main__":
    app.run(debug=True)
