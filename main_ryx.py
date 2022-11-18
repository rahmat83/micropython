from machine import UART, Pin
import uasyncio as asyncio
import as_GPS as as_GPS

from pico_i2c_lcd import I2cLcd
from machine import I2C
import utime as time

time.sleep(5)

sda=machine.Pin(2)
scl=machine.Pin(3)
i2c=machine.I2C(1,sda=sda, scl=scl, freq=10000)

lcd = I2cLcd(i2c, 0x27, 2, 16)


# pin tx and rx
uart= UART(0,baudrate=9600,tx=Pin(16),rx=Pin(17),bits=8,parity=None,stop=1,timeout=1)


def gps_calculation(x,y):
     DD = int(x)
  
     SS = float(y)/60.0 
    
     Com=DD+SS     
     return Com
    

async def sender():
    swriter = asyncio.StreamWriter(uart, {})
    
    while True:
        print('Wrote')
        await asyncio.sleep(1)

async def receiver():
    sreader = asyncio.StreamReader(uart)

    
    while True:
        
        try:
            nmea = await sreader.readline()
           
           
            if nmea.startswith( '$GPRMC' ) :
                gps=nmea.rstrip().decode('utf-8')
                location=gps.split(",")
                
                
                lat_raw=location[3][1],location[3][2:]
                long_raw=location[5][:3],location[5][3:]
         
                lat=gps_calculation(lat_raw[0],lat_raw[1])
                long=gps_calculation(long_raw[0],long_raw[1])
                
                print(lat,long)
                
                lcd.putstr(str(lat)+ "        ")
                lcd.putstr(str(long))
                time.sleep(2)
                    
                #lcd.putstr(location[32:46])
                lcd.clear()
        except IndexError:
            pass
          

loop = asyncio.get_event_loop()

loop.create_task(sender())
loop.create_task(receiver())
loop.run_forever()