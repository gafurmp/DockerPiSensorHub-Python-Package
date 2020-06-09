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
     self.__aReceiveBuf = []
     self.__aReceiveBuf.append(0x00)
     self.__devicebus = devicebus
     self.__deviceaddr = deviceaddr
     self.__bus = smbus.SMBus(self.__devicebus)
     if display is not None:
       self.__display = display
     else:
       self.__display = 'OFF'

  def __repr__(self):
      print("Docker Pi Package v{}".format(__version__))

  def __readSensorData(self):
    for i in range(TEMP_REG,HUMAN_DETECT + 1) :
      self.__aReceiveBuf.append(self.__bus.read_byte_data(self.__deviceaddr, i))

  def setDisplay(self, display):
      self.__display = display

  def isHumanDetected(self):
     self.__readSensorData()
     if(self.__display == 'ON'):
       if(self.__aReceiveBuf[HUMAN_DETECT] == 1):
         print("DockerPi: Live body detected within 5 seconds!")
       else:
         print("DockerPi: No human ditected!")
     return (self.__aReceiveBuf[HUMAN_DETECT] == 1)

  def getOffChipTemperature(self, unit = 'DEGREECELSIUS'):
     self.__readSensorData()

     if self.__aReceiveBuf[STATUS_REG] & 0x01 :
        if(self.__display == 'ON'):
          print("DockerPi: Off-chip temperature sensor overrange!")
     elif self.__aReceiveBuf[STATUS_REG] & 0x02 :
        if(self.__display == 'ON'):
          print("DockerPi: No external temperature sensor!")
     else :
        if unit == 'DEGREECELSIUS':
          print("DockerPi: Current Off-chip temperature sensor value = %d Celsius" %  self.__aReceiveBuf[TEMP_REG])
          return self.__aReceiveBuf[TEMP_REG]
        else:
          fahrenheit = ( ((self.__aReceiveBuf[TEMP_REG] * 9) / 5) + 32 )
          print("DockerPi: Current Off-chip temperature sensor value = %d Celsius" %  fahrenheit)
          return fahrenheit

  def getOnBoardBrightness(self):
    self.__readSensorData()

    if self.__aReceiveBuf[STATUS_REG] & 0x04 :
       if(self.__display == 'ON'):
         print("DockerPi: Onboard brightness sensor overrange!")
    elif self.__aReceiveBuf[STATUS_REG] & 0x08 :
       if(self.__display == 'ON'):
         print("DockerPi: Onboard brightness sensor failure!")
    else :
       if(self.__display == 'ON'):
         print("DockerPi: Current onboard sensor brightness = %d Lux" % (self.__aReceiveBuf[LIGHT_REG_H] << 8 | self.__aReceiveBuf[LIGHT_REG_L]))
       return (self.__aReceiveBuf[LIGHT_REG_H] << 8 | self.__aReceiveBuf[LIGHT_REG_L])

  def getOnBoardTemperature(self, unit = 'DEGREECELSIUS'):
     self.__readSensorData()

     if self.__aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        if(self.__display == 'ON'):
          print("DockerPi: Onboard temperature sensor data may not be up to date!")

     if unit == 'DEGREECELSIUS':
       if(self.__display == 'ON'):
         print("DockerPi: Current onboard sensor temperature = %d Celsius" % self.__aReceiveBuf[ON_BOARD_TEMP_REG])
       return self.__aReceiveBuf[ON_BOARD_TEMP_REG]
     else:
       fahrenheit = ( ((self.__aReceiveBuf[ON_BOARD_TEMP_REG] * 9) / 5) + 32 )
       if(self.__display == 'ON'):
         print("DockerPi: Current onboard sensor temperature = %d Fahrenheit" % fahrenheit)
       return fahrenheit

  def getOnBoardHumidity(self):
     self.__readSensorData()

     if self.__aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        if(self.__display == 'ON'):
          print("DockerPi: Onboard humidity sensor data may not be up to date!")
     if(self.__display == 'ON'):
       print("DockerPi: Current onboard sensor humidity = %d %%" % self.__aReceiveBuf[ON_BOARD_HUMIDITY_REG])
     return self.__aReceiveBuf[ON_BOARD_HUMIDITY_REG]

  def getBarometerTemperature(self, unit = 'DEGREECELSIUS'):
     self.__readSensorData()

     if self.__aReceiveBuf[BMP280_STATUS] == 0 :
        if(self.__display == 'ON'):
          print("DockerPi: Current barometer temperature = %d Celsius" % self.__aReceiveBuf[BMP280_TEMP_REG])
        if unit == 'DEGREECELSIUS':
          return self.__aReceiveBuf[BMP280_TEMP_REG]
        else:
          fahrenheit = ( ((self.__aReceiveBuf[BMP280_TEMP_REG]* 9) / 5) + 32 )
          print("DockerPi: Current barometer temperature = %d Fahrenheit" %  fahrenheit)
          return fahrenheit
     else :
        if(self.__display == 'ON'):
          print("DockerPi: Onboard barometer works abnormally!")

  def getBarometerPressure(self):
     self.__readSensorData()

     if self.__aReceiveBuf[BMP280_STATUS] == 0 :
        if(self.__display == 'ON'):
          print("DockerPi: Current barometer pressure = %d pascal" % (self.__aReceiveBuf[BMP280_PRESSURE_REG_L] | self.__aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | self.__aReceiveBuf[BMP280_PRESSURE_REG_H] << 16))
          return ( (self.__aReceiveBuf[BMP280_PRESSURE_REG_L] | self.__aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | self.__aReceiveBuf[BMP280_PRESSURE_REG_H] << 16) )
     else :
        if(self.__display == 'ON'):
          print("DockerPi: Onboard barometer works abnormally!")
