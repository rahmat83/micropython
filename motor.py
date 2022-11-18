
from machine import Pin,ADC,PWM,SoftI2C,I2C
import utime
import time

led=Pin(2,Pin.OUT)
IN1 = Pin(16, Pin.OUT)
IN2 = Pin(17, Pin.OUT)

en1 = Pin(15,Pin.OUT)

pot1=ADC(Pin(34))
pot1.atten(ADC.ATTN_11DB)

pot2=ADC(Pin(39))
pot2.atten(ADC.ATTN_11DB)

pwm = PWM(en1)
pwm.deinit()
pwm.init(freq=50,duty=2)

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

def cw():
    IN1.value(0)
    IN2.value(1)
    

def ccw():
    IN1.value(1)
    IN2.value(0)

led.off()
start_time=(time.ticks_ms())
start_angle=getAngle()

while True:
    current_time=(time.ticks_ms())
    current_angle=getAngle()
    print("current angle",current_angle)
    t=current_time-start_time
    print("t = ",t)
    k=(int(pot1.read()/4095*1000))
    l=(int((pot2.read()+1)/50))
    if l==0:
        l=1
    print(k,l)
    pwm.duty(k)
    print(pwm.duty())    
    cw()
    angle_dif=current_angle-start_angle
    start_angle=current_angle    
    time.sleep(1/l)
    ccw()
    time.sleep(1/l)

  

     


