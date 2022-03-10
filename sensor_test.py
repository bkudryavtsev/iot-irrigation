import time

import si114x
import dht20
import soil

def main():
    SI1145 = si114x.SI114X()
    DHT20 = dht20.DHT20()
    soil_moisture = soil.SoilMoistureSensor(0)

    while True:
        s = soil_moisture.get_moisture()
        h = DHT20.get_humidity()
        t = DHT20.get_temperature()
        print('Visible %03d | UV %.2f | IR %03d | Soil %.2f | Humidity %.2f | Temp %.2f'  % (SI1145.ReadVisible , SI1145.ReadUV/100 , SI1145.ReadIR, s, h, t), end=' ')
        print('\r', end='')
        time.sleep(0.5)

if __name__  == '__main__':
    main()
