# DockerPi Package

This is a Docker PI sensor hub package.<br>


While instanciating the class object, two mandatory arguments (**devicebus** and **deviceaddr**) and one optional argument (**disaplay**) must be passed.<br>

**devicebus** - the number of device.<br>
**deviceaddr** - configured address of DockerPi i2c.<br>
**display** - turn the print statements 'ON' or 'OFF'. Default: 'OFF'.<br>


All temperature methods can be called with an optional **unit** argument. i.e, 'DEGREECELSIUS' or 'FAHRENHEIT'. by default, 'DEGREECELSIUS' is returned.<br>

# Installation

Change your directory in to root folder of this package and then execute below pip command.<br>
**"pip install ."**<br>

# Example Code

~~~
import warnings
from dockerpi import DockerPi
from time import sleep
import time


def main():
  print("Docker Pi: Sensor Hub Started")
  while True:
    sensor = DockerPi(devicebus = 0x1, deviceaddr = 0x17)
    x = sensor.isHumanDetected()
    y = sensor.getOffChipTemperature()
    z = sensor.getOnBoardBrightness()
    a = sensor.getOnBoardTemperature('FAHRENHEIT')
    b = sensor.getOnBoardHumidity()
    c = sensor.getBarometerTemperature('DEGREECELSIUS')
    d = sensor.getBarometerPressure()

    sleep(15)

if __name__=='__main__':
    main()
~~~
