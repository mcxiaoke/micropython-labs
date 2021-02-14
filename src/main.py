import ulogging as logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')

def reload(mod):
    import sys
    mod_name = mod.__name__
    del sys.modules[mod_name]
    return __import__(mod_name)

import wifi
logger.info('WiFi Connecting...')
wifi.do_connect()

import server
logger.info('Starting server...')
server.start()

