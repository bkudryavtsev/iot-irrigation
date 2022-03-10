# -*- coding: utf-8 -*
"""
  *@file DFRobot_DHT20.py
  *@brief Define the basic structure of class DFRobot_DHT20
  *@copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  *@licence     The MIT License (MIT)
  *@author [fengli](li.feng@dfrobot.com)
  *@version  V1.0
  *@date  2021-6-25
  *@get from https://www.dfrobot.com
  *@https://github.com/DFRobot/DFRobot_DHT20

  Modified to work with the Onion Omega2+ platform
"""
import time

from OmegaExpansion import onionI2C

I2C_ADDR = 0x38 
                
class DHT20(object):
  ''' Conversion data '''

  def __init__(self):
    self.i2cbus = onionI2C.OnionI2C()
    self._addr = I2C_ADDR
    self.idle = 0

    if not self.begin():
        print("Error initializing DHT20")

  '''
    @brief init function
    @return Return 0 if initialization succeeds, otherwise return non-zero and error code.
   '''
  def begin(self):
    time.sleep(0.5)
    data = self.read_reg(0x71, 1)
    
    if (data[0] | 0x08) == 0:
      return False
    else:
      return True

  '''
    @brief Get ambient temperature, unit: °C
    @return ambient temperature,the measurement range is -40°C ~ 80°C
  '''
  def get_temperature(self):
     self.write_reg(0xac,[0x33,0x00])
     time.sleep(0.1)
     data = self.read_reg(0x71,7)
     rawData = ((data[3]&0xf) <<16) + (data[4]<<8)+data[5]
     #print(rawData)
     temperature = float(rawData)/5242 -50
     return temperature
     
  '''
    @brief Get relative humidity, unit: %RH. 
    @return relative humidity, the measurement range is (1-100%)
  '''
  def get_humidity(self):
     self.write_reg(0xac,[0x33,0x00])
     time.sleep(0.1)
     data = self.read_reg(0x71,7)
     rawData = ((data[3]&0xf0) >>4) + (data[1]<<12)+(data[2]<<4)
     humidity = float(rawData)/0x100000
     return humidity*100
     
  
  def write_reg(self, reg, data):
    time.sleep(0.01)
    self.i2cbus.writeBytes(self._addr, reg, data)
  
  
  def read_reg(self,reg,len):
    time.sleep(0.01)
    rslt = self.i2cbus.readBytes(self._addr, reg, len)
    #print(rslt)
    return rslt
