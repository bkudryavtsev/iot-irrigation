import time

import seeed_si114x
import seeed_dht
from OmegaExpansion import AdcExp

def main():
    SI1145 = seeed_si114x.grove_si114x()
    DHT20 = seeed_dht.DHT20()
    adc = AdcExp.AdcExp()

    DHT20.begin()

    while True:
        a0 = adc.read_voltage(0)
        soil = (a0 / 5) * 100
        h = DHT20.get_humidity()
        t = DHT20.get_temperature()
        print('Visible %03d | UV %.2f | IR %03d | Soil %f | Humidity %f | Temp %f'  % (SI1145.ReadVisible , SI1145.ReadUV/100 , SI1145.ReadIR, soil, h, t), end=" ")
        print('\r', end='')
        time.sleep(0.5)

if __name__  == '__main__':
    main()
