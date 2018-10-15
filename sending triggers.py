from __future__ import absolute_import, division

from numpy.random import random, randint, normal, shuffle,uniform

import serial #for sending triggers from this computer to biosemi computer


port=serial.Serial('COM4',baudrate=115200)

for n in range(1,256):
    port.close()
    port.open()
    port.write(bytes([n]))
    port.flush()
    core.wait(.5)
    #port.close()