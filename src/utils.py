import machine
import time
import ntptime
import ulogging as logging

GAP_1970_2000 = 946684800

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('utils')

def setup_time():
    # json time api
    # http://worldtimeapi.org/api/timezone/Asia/Shanghai
    # or http://worldtimeapi.org/api/ip
    # or http://quan.suning.com/getSysTime.do
    # setup datetime
    try:
        ntptime.host = 'ntp.aliyun.com'
        ntptime.settime()
    except:
        ntptime.host = 'ntp.neu.edu.cn'
        ntptime.settime()
    rtc=machine.RTC()
    # utc_time = time.time()
    logger.info("Timestamp: %u", GAP_1970_2000 + time.time())
    prc_time = time.time() + 3600*8 # timezone +8
    (year, month, mday, hour, minute, second, weekday, yearday)=time.localtime(prc_time)
    rtc.datetime((year, month, mday, 0, hour, minute, second, 0))
    t = time.localtime()
    # "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(*time.localtime())
    logger.info("Time: %04u-%02u-%02u %02u:%02u:%02u" % t[0:6])
    # unix timestamp = GAP_1970_2000 + time.time() # seconds since 20000101