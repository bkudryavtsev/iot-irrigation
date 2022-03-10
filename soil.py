from OmegaExpansion import AdcExp

MIN_VOLTAGE = 2.68
MAX_VOLTAGE = 3.72

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

class SoilMoistureSensor:
    def __init__(self, pin):
        self.adc = AdcExp.AdcExp()
        self.pin = pin

    def get_moisture(self):
        v = self.get_voltage();
        return 100 - translate(v, MIN_VOLTAGE, MAX_VOLTAGE, 0, 100)

    def get_voltage(self):
        return self.adc.read_voltage(self.pin)

