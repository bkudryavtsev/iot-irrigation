import time

import seeed_si114x
from OmegaExpansion import AdcExp

def main():
    SI1145 = seeed_si114x.grove_si114x()
    adc = AdcExp.AdcExp()

    while True:
      	a0 = adc.read_voltage(0)
        print('Soil %d' % (a0))

        print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible , SI1145.ReadUV/100 , SI1145.ReadIR),end=" ")
        print('\r', end='')
        time.sleep(0.5)

if __name__  == '__main__':
    main()