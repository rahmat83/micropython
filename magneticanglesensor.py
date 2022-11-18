from machine import Pin,I2C,SoftI2C
import utime

sdaPin=21
sclPin=22

AS5600_ADDRESS = const(0x36)   # AS5600 has a fixed address (so can only use one per I2C bus?)
ANGLE_H = const(0x0E)          # Angle register (high byte)
ANGLE_L = const(0x0F)          # Angle register (low byte)

i2c=SoftI2C(sda=Pin(sdaPin),scl=Pin(sclPin),freq=112500)
utime.sleep_ms(100)


def getnReg(reg, n):
    i2c.writeto(AS5600_ADDRESS, bytearray([reg]))
    t =	i2c.readfrom(AS5600_ADDRESS, n)
    return t    


def getAngle():
    buf = getnReg(ANGLE_H, 2)
    return ((buf[0]<<8) | buf[1])/ 4096.0*360

utime.sleep_ms(100)


while True:
    print(getAngle())
    utime.sleep_ms(1000)
    
