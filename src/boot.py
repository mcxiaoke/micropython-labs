# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
# esp.osdebug(None)
import webrepl

webrepl.start()

print('[Boot] Boot Successful!')

# setup wifi
try:
    import wifi
    wifi.connect()
except:
    pass
