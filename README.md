# DockerPi Package

This is a Docker PI sensor hub package.

# Installation
Change your directory in to root folder of this package and then execute below pip command
**"pip install ."**



# Example Code

~~~
import warnings
from dockerpi import DockerPi
from time import sleep
import time


def main():
  print("Docker Pi: Sensor Hub Started")
  while True:
    sensor = DockerPi(devicebus = 0x1, deviceaddr = 0x17, display = 'ON')
    x = sensor.isHumanDetected()
    y = sensor.getOffChipTemperature()
    z = sensor.getOnBoardBrightness()
    a = sensor.getOnBoardTemperature()
    b = sensor.getOnBoardHumidity()
    c = sensor.getBarometerTemperature()
    d = sensor.getBarometerPressure()

    sleep(15)

if __name__=='__main__':
    main()
~~~
