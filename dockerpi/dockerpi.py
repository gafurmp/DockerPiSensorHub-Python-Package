# -*- coding: utf-8 -*-

"""
dockerpi.dockerpi
~~~~~~~~~~

This module contains functionality for reading sensor data from Docker Pi sensor hub.
"""

import warnings
import logging
from consts import *
import smbus

#log file configuration
logfile = '/var/log/DockerPi.log'

#configure logger
logging.basicConfig(filename=logfile, level=logging.DEBUG)
 
# create logger
logger = logging.getLogger('DockerPi')

class DockerPi(object):

  def __init__(self, devicebus, deviceaddr):
     self._aReceiveBuf = []
     self._aReceiveBuf.append(0x00)
     self._devicebus = devicebus
     self._deviceaddr = deviceaddr
     self._bus = smbus.SMBus(self._devicebus)

  def __repr__(self):
      print("Docker Pi Package v{}".format(__version__))

  def _readSensorData(self):
    for i in range(TEMP_REG,HUMAN_DETECT + 1) :
      self._aReceiveBuf.append(self._bus.read_byte_data(self._deviceaddr, i))

  def isHumanDetected(self):
     self._readSensorData()
     if(self._aReceiveBuf[HUMAN_DETECT] == 1):
        logger.debug("DockerPi: Live body detected within 5 seconds!")
     else:
        logger.debug("DockerPi: No human ditected!")
     return (self._aReceiveBuf[HUMAN_DETECT] == 1)

  def getOffChipTemperature(self, unit = 'DEGREECELSIUS'):
     self._readSensorData()

     if self._aReceiveBuf[STATUS_REG] & 0x01 :
        logger.debug("DockerPi: Off-chip temperature sensor overrange!")
     elif self._aReceiveBuf[STATUS_REG] & 0x02 :
        logger.debug("DockerPi: No external temperature sensor!")
     else :
        if unit == 'DEGREECELSIUS':
          logger.debug("DockerPi: Current Off-chip temperature sensor value = %d Celsius" %  self._aReceiveBuf[TEMP_REG])
          return self._aReceiveBuf[TEMP_REG]
        else:
          fahrenheit = ( ((self._aReceiveBuf[TEMP_REG] * 9) / 5) + 32 )
          logger.debug("DockerPi: Current Off-chip temperature sensor value = %d Celsius" %  fahrenheit)
          return fahrenheit

  def getOnBoardBrightness(self):
    self._readSensorData()

    if self._aReceiveBuf[STATUS_REG] & 0x04 :
       logger.debug("DockerPi: Onboard brightness sensor overrange!")
    elif self._aReceiveBuf[STATUS_REG] & 0x08 :
       logger.debug("DockerPi: Onboard brightness sensor failure!")
    else :
       logger.debug("DockerPi: Current onboard sensor brightness = %d Lux" % (self._aReceiveBuf[LIGHT_REG_H] << 8 | self._aReceiveBuf[LIGHT_REG_L]))
       return (self._aReceiveBuf[LIGHT_REG_H] << 8 | self._aReceiveBuf[LIGHT_REG_L])


  def getOnBoardTemperature(self, unit = 'DEGREECELSIUS'):
     self._readSensorData()

     if self._aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        logger.debug("DockerPi: Onboard temperature sensor data may not be up to date!")

     if unit == 'DEGREECELSIUS':
       logger.debug("DockerPi: Current onboard sensor temperature = %d Celsius" % self._aReceiveBuf[ON_BOARD_TEMP_REG])
       return self._aReceiveBuf[ON_BOARD_TEMP_REG]
     else:
       fahrenheit = ( ((self._aReceiveBuf[ON_BOARD_TEMP_REG] * 9) / 5) + 32 )
       logger.debug("DockerPi: Current onboard sensor temperature = %d Fahrenheit" % fahrenheit)
       return fahrenheit


  def getOnBoardHumidity(self):
     self._readSensorData()

     if self._aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        logger.debug("DockerPi: Onboard humidity sensor data may not be up to date!")
     logger.debug("DockerPi: Current onboard sensor humidity = %d %%" % self._aReceiveBuf[ON_BOARD_HUMIDITY_REG])
     return self._aReceiveBuf[ON_BOARD_HUMIDITY_REG]


  def getBarometerTemperature(self, unit = 'DEGREECELSIUS'):
     self._readSensorData()

     if self._aReceiveBuf[BMP280_STATUS] == 0 :
        logger.debug("DockerPi: Current barometer temperature = %d Celsius" % self._aReceiveBuf[BMP280_TEMP_REG])
        if unit == 'DEGREECELSIUS':
          return self._aReceiveBuf[BMP280_TEMP_REG]
        else:
          fahrenheit = ( ((self._aReceiveBuf[BMP280_TEMP_REG]* 9) / 5) + 32 )
          logger.debug("DockerPi: Current barometer temperature = %d Fahrenheit" %  fahrenheit)
          return fahrenheit
     else :
        logger.debug("DockerPi: Onboard barometer works abnormally!")

  def getBarometerPressure(self):
     self._readSensorData()

     if self._aReceiveBuf[BMP280_STATUS] == 0 :
        logger.debug("DockerPi: Current barometer pressure = %d pascal" % (self._aReceiveBuf[BMP280_PRESSURE_REG_L] | self._aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | self._aReceiveBuf[BMP280_PRESSURE_REG_H] << 16))
        return ( (self._aReceiveBuf[BMP280_PRESSURE_REG_L] | self._aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | self._aReceiveBuf[BMP280_PRESSURE_REG_H] << 16) )
     else :
        logger.debug("DockerPi: Onboard barometer works abnormally!")
