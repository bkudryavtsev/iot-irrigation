#!/usr/bin/env python
#
# This code is for
#   Grove - Temperature & Humidity Sensor (DHT11)
#     (https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-DHT1-p-745.html)
#   Grove - Temperature & Humidity Sensor Pro (AM2302)
#     (https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-Pro-AM230-p-838.html)
#
# which is consists of a capacitive sensor element used for measuring relative humidity
# and a negative temperature coefficient(NTC) thermistor used for measuring temperature.
#
# Modified to work with Onion Omega2+ and DHT20
#
from OmegaExpansion import onionI2C
import time

class DHT(object):
    DEFAULT_ADDR    = 0x38
    RESET_REG_ADDR  = 0xba
    MAX_CNT = 320
    PULSES_CNT = 41

    def __init__(self):        
        self.bus = onionI2C.OnionI2C()
        self.addr = self.DEFAULT_ADDR
        self._dht10_init()

    ######################## dht10 ############################

    def _dht10_start_mess(self):
        reg_set = [0x33, 0x00]
        self.bus.writeBytes(self.addr, 0xac, reg_set)

    def _dht10_reset(self):
        self.bus.writeByte(self.addr, self.RESET_REG_ADDR, 0x01)
    
    def _dht10_set_system_cfg(self):
        reg_set = [0x08, 0x00]
        self.bus.writeBytes(self.addr, 0xe1, reg_set)

    def _dht10_read_status(self):
        return self.bus.readBytes(self.addr, 0, 1)[0]

    def _dht10_init(self):
        time.sleep(.5)
        self._dht10_reset()
        # delay is needed after reset
        time.sleep(.3)

        self._dht10_set_system_cfg()
        status = self._dht10_read_status()
        # we must check the calibrate flag, bit[3] : 1 for calibrated ok,0 for Not calibrated.
        while (status & 0x08 != 0x08):
            print("try calibrated again!n\n")
            self._dht10_reset()
            time.sleep(.5)
            self._dht10_set_system_cfg()
            status = self._dht10_read_status()
            time.sleep(.5)

    #########################################################
    def _read(self):
        t = 0
        h = 0
        self._dht10_start_mess()
        time.sleep(.075)
        # we must check the device busy flag, bit[7] : 1 for busy ,0 for idle.
        while((self._dht10_read_status() & 0x80) != 0):
            time.sleep(.5)
            print("wait for device not busy")
        from smbus2 import SMBus,i2c_msg,SMBusWrapper
        with SMBusWrapper(1) as bus:
            msg = i2c_msg.read(self.addr, 6)
            data = bus.i2c_rdwr(msg)

        data = list(msg)
        t = (t | data[1]) << 8
        t = (t | data[2]) << 8
        t = (t | data[3]) >> 4

        h = (h | data[3]) << 8
        h = (h | data[4]) << 8
        h = (h | data[5]) & 0xfffff

        t = t * 100.0 / 1024 / 1024
        h = h * 200.0 / 1024 / 1024 - 50
        #print(data)
        return t, h

    def read(self, retries = 15):
        for i in range(retries):
            humi, temp = self._read()
            if not humi is None:
                break
        if humi is None:
            return self._last_humi, self._last_temp
        self._last_humi,self._last_temp = humi, temp
        return humi, temp
