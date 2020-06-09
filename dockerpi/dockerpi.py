# -*- coding: utf-8 -*-

"""
dockerpi.dockerpi
~~~~~~~~~~

This module contains functionality for reading sensor data from Docker Pi sensor hub.
"""

import warnings

from consts import *
import smbus


class DockerPi(object):

  def __init__(self, devicebus, deviceaddr, display = None):
     self._aReceiveBuf = []
     self._aReceiveBuf.append(0x00)
     self._devicebus = devicebus
     self._deviceaddr = deviceaddr
     self._bus = smbus.SMBus(self._devicebus)
     if display is not None:
       self._display = display
     else:
       self._display = 'OFF'

  def __repr__(self):
      print("Docker Pi Package v{}".format(__version__))

  def _readSensorData(self):
    for i in range(TEMP_REG,HUMAN_DETECT + 1) :
      self._aReceiveBuf.append(self._bus.read_byte_data(self._deviceaddr, i))

  @property
  def setDisplay(self, display):
      self._display = display
  
  @property
  def isHumanDetected(self):
     self._readSensorData()
     if(self._display == 'ON'):
       if(self._aReceiveBuf[HUMAN_DETECT] == 1):
         print("DockerPi: Live body detected within 5 seconds!")
       else:
         print("DockerPi: No human ditected!")
     return (self._aReceiveBuf[HUMAN_DETECT] == 1)
  
  @property
  def getOffChipTemperature(self, unit = 'DEGREECELSIUS'):
     self._readSensorData()

     if self._aReceiveBuf[STATUS_REG] & 0x01 :
        if(self._display == 'ON'):
          print("DockerPi: Off-chip temperature sensor overrange!")
     elif self._aReceiveBuf[STATUS_REG] & 0x02 :
        if(self._display == 'ON'):
          print("DockerPi: No external temperature sensor!")
     else :
        if unit == 'DEGREECELSIUS':
          print("DockerPi: Current Off-chip temperature sensor value = %d Celsius" %  self._aReceiveBuf[TEMP_REG])
          return self._aReceiveBuf[TEMP_REG]
        else:
          fahrenheit = ( ((self._aReceiveBuf[TEMP_REG] * 9) / 5) + 32 )
          print("DockerPi: Current Off-chip temperature sensor value = %d Celsius" %  fahrenheit)
          return fahrenheit
  
  @property
  def getOnBoardBrightness(self):
    self._readSensorData()

    if self._aReceiveBuf[STATUS_REG] & 0x04 :
       if(self._display == 'ON'):
         print("DockerPi: Onboard brightness sensor overrange!")
    elif self._aReceiveBuf[STATUS_REG] & 0x08 :
       if(self._display == 'ON'):
         print("DockerPi: Onboard brightness sensor failure!")
    else :
       if(self._display == 'ON'):
         print("DockerPi: Current onboard sensor brightness = %d Lux" % (self._aReceiveBuf[LIGHT_REG_H] << 8 | self._aReceiveBuf[LIGHT_REG_L]))
       return (self._aReceiveBuf[LIGHT_REG_H] << 8 | self._aReceiveBuf[LIGHT_REG_L])
  
  @property
  def getOnBoardTemperature(self, unit = 'DEGREECELSIUS'):
     self._readSensorData()

     if self._aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        if(self._display == 'ON'):
          print("DockerPi: Onboard temperature sensor data may not be up to date!")

     if unit == 'DEGREECELSIUS':
       if(self._display == 'ON'):
         print("DockerPi: Current onboard sensor temperature = %d Celsius" % self._aReceiveBuf[ON_BOARD_TEMP_REG])
       return self._aReceiveBuf[ON_BOARD_TEMP_REG]
     else:
       fahrenheit = ( ((self._aReceiveBuf[ON_BOARD_TEMP_REG] * 9) / 5) + 32 )
       if(self._display == 'ON'):
         print("DockerPi: Current onboard sensor temperature = %d Fahrenheit" % fahrenheit)
       return fahrenheit
  
  @property
  def getOnBoardHumidity(self):
     self.__readSensorData()

     if self._aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        if(self._display == 'ON'):
          print("DockerPi: Onboard humidity sensor data may not be up to date!")
     if(self._display == 'ON'):
       print("DockerPi: Current onboard sensor humidity = %d %%" % self._aReceiveBuf[ON_BOARD_HUMIDITY_REG])
     return self._aReceiveBuf[ON_BOARD_HUMIDITY_REG]

  @property
  def getBarometerTemperature(self, unit = 'DEGREECELSIUS'):
     self._readSensorData()

     if self._aReceiveBuf[BMP280_STATUS] == 0 :
        if(self._display == 'ON'):
          print("DockerPi: Current barometer temperature = %d Celsius" % self._aReceiveBuf[BMP280_TEMP_REG])
        if unit == 'DEGREECELSIUS':
          return self._aReceiveBuf[BMP280_TEMP_REG]
        else:
          fahrenheit = ( ((self._aReceiveBuf[BMP280_TEMP_REG]* 9) / 5) + 32 )
          print("DockerPi: Current barometer temperature = %d Fahrenheit" %  fahrenheit)
          return fahrenheit
     else :
        if(self._display == 'ON'):
          print("DockerPi: Onboard barometer works abnormally!")

  @property
  def getBarometerPressure(self):
     self._readSensorData()

     if self._aReceiveBuf[BMP280_STATUS] == 0 :
        if(self._display == 'ON'):
          print("DockerPi: Current barometer pressure = %d pascal" % (self._aReceiveBuf[BMP280_PRESSURE_REG_L] | self._aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | self._aReceiveBuf[BMP280_PRESSURE_REG_H] << 16))
          return ( (self._aReceiveBuf[BMP280_PRESSURE_REG_L] | self._aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | self._aReceiveBuf[BMP280_PRESSURE_REG_H] << 16) )
     else :
        if(self._display == 'ON'):
          print("DockerPi: Onboard barometer works abnormally!")
