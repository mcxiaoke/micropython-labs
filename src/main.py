import micropython
import ulogging as logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')


# setup time
try:
    import utils
    utils.setup_time()
except:
    logger.warning('NTP failed')

# print mem info
# logger.info('Memory Info:')
# micropython.mem_info()

# setup web server
logger.info('Starting server...')
try:
    import server
    server.start()
except:
    logger.warning('Server Failed')
