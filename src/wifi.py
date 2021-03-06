import time
import network
from machine import Pin

led = Pin(2, Pin.OUT)

def toggle(pin):
    pin.value(not pin.value())


def config_ap():
    print('Network not connected, using AP')
    import ubinascii
    ap_if = network.WLAN(network.AP_IF)
    essid = b"MicroPython-%s" % ubinascii.hexlify(ap_if.config("mac")[-3:])
    ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK,
                 password=b"micropythoN")
    # set how many clients can connect to the network
    ap_if.config(max_clients=10)
    ap_if.active(True)         # activate the interface
    print('AP SSID:{} PASS:{}'.format(essid, "micropythoN"))


def do_connect():
    start = time.time()
    from config import WIFI_SSID, WIFI_PASS
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to {}'.format(WIFI_SSID))
        sta_if.active(True)
        sta_if.scan()
        sta_if.connect(WIFI_SSID, WIFI_PASS)
        while not sta_if.isconnected():
            print('.', end='')
            toggle(led)
            time.sleep_ms(500)
            if time.time() - start > 60:
                print('Connecting timeout, abort.')
                break
    print('')
    if sta_if.isconnected():
        led.on()
        print('Network IP:{}'.format(sta_if.ifconfig()[0]))
    else:
        led.off()
        config_ap()

def connect():
    print('WiFi Connecting...')
    try:
        do_connect()
    except:
        print('[Boot] WiFi failed')