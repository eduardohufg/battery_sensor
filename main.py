#Declaration of libraries and files
from machine import Pin, I2C, ADC,PWM
import utime
from utime import sleep_ms, sleep
from ssd1306 import SSD1306_I2C
from oled import Write
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
from ssd1306font import Display_font
import framebuf
import time
from neopixel import Neopixel

if __name__ == '__main__':
    sleep_ms(1000)
    #Declaration of tones frecuency
    tones = {
        "B0": 31,
        "C1": 33,
        "CS1": 35,
        "D1": 37,
        "DS1": 39,
        "E1": 41,
        "F1": 44,
        "FS1": 46,
        "G1": 49,
        "GS1": 52,
        "A1": 55,
        "AS1": 58,
        "B1": 62,
        "C2": 65,
        "CS2": 69,
        "D2": 73,
        "DS2": 78,
        "E2": 82,
        "F2": 87,
        "FS2": 93,
        "G2": 98,
        "GS2": 104,
        "A2": 110,
        "AS2": 117,
        "B2": 123,
        "C3": 131,
        "CS3": 139,
        "D3": 147,
        "DS3": 156,
        "E3": 165,
        "F3": 175,
        "FS3": 185,
        "G3": 196,
        "GS3": 208,
        "A3": 220,
        "AS3": 233,
        "B3": 247,
        "C4": 262,
        "CS4": 277,
        "D4": 294,
        "DS4": 311,
        "E4": 330,
        "F4": 349,
        "FS4": 370,
        "G4": 392,
        "GS4": 415,
        "A4": 440,
        "AS4": 466,
        "B4": 494,
        "C5": 523,
        "CS5": 554,
        "D5": 587,
        "DS5": 622,
        "E5": 659,
        "F5": 698,
        "FS5": 740,
        "G5": 784,
        "GS5": 831,
        "A5": 880,
        "AS5": 932,
        "B5": 988,
        "C6": 1047,
        "CS6": 1109,
        "D6": 1175,
        "DS6": 1245,
        "E6": 1319,
        "F6": 1397,
        "FS6": 1480,
        "G6": 1568,
        "GS6": 1661,
        "A6": 1760,
        "AS6": 1865,
        "B6": 1976,
        "C7": 2093,
        "CS7": 2217,
        "D7": 2349,
        "DS7": 2489,
        "E7": 2637,
        "F7": 2794,
        "FS7": 2960,
        "G7": 3136,
        "GS7": 3322,
        "A7": 3520,
        "AS7": 3729,
        "B7": 3951,
        "C8": 4186,
        "CS8": 4435,
        "D8": 4699,
        "DS8": 4978,
    }
    #assign input and output pins
    sensor = ADC(4)
    strip = Neopixel(8, 0, 1, "RGB")
    #buz = PWM(Pin(13))
    buz = Pin(2,Pin.OUT)
    pot = ADC(0)
    i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq = 200000)
    btn = Pin(13, Pin.IN)
    
    
        
    
    #Declaration of colors to Neopixels
    red = (255, 0, 0)
    orange = (255, 120, 0)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    violet = (138, 43, 226)
    none = (0,0,0)
    colors_rgb = (red, orange, yellow, green, blue, violet)

    #Set brightness if Neopixels
    strip.brightness(85)
    

    #Set parameters of oled display
    WIDTH = 128
    HEIGHT = 64
    FACTOR = (2.95/ (58584)) * 4.168
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    write15 = Write(oled, ubuntu_mono_15)
    write20 = Write(oled, ubuntu_mono_20)
    
    #Function to show string on oled
    def ssd_text(string, font, char_height,stri,off,offset=1):
        
        oled.fill(0)
        oled.line(0,0,128,0,1)
        oled.line(0,0,0,64,1)
        
        oled.line(0,63,128,63,1)
        oled.line(127,0,127,63,1)
        write20.text(stri,off,2)
        for c in string:
            try:
                fontchar = font[c]   # get char layout
            except KeyError:
                fontchar = font[":"] # default to ":" if not found. 
            
            char_width = len(fontchar)
            for i, line in enumerate(fontchar):
                ssd_x = i + offset
                for j, char_pixel in enumerate(line):
                    ssd_y = (char_height - j) * 1 + 20
                    if char_pixel != " ":
                        oled.pixel(ssd_x, ssd_y, 1)
            offset += char_width + 8
        oled.show()

    #Function to play a specific tone
    def playtone(frecuencia):
        buz.duty_u16(1000)
        buz.freq(frecuencia)
    #Function to mute sound
    def silencio():
        buz.duty_u16(0)
    #Funtion to play a list of tones
    def playsong(song):
        for i in range(len(song)):
            if (song[i] == ""):
                silencio()
            else:
                playtone(tones[song[i]])
            sleep(0.1)
        silencio()
        
    #List of tones
    song = ["A5","A5","A5","","E5","","F5","","G5","G5","G5","","F5","","E5","","D5","D5","D5","","D5","","F5","","A5","A5","A5","","G5","","F5","","E5","E5","E5","E5","","E5","","F5","","G5","G5","G5","","A5","A5","A5","","F5","F5","F5","","D5","D5","D5","","D5","D5","D5","","","","G5","G5","G5","","B5","","D6","","D6","","C6","","B5","","A5","A5","A5","","F5","","A5","","A5","","G5","","F5","","E5","E5","E5","","E5","","F5","","G5","G5","G5","","A5","A5","A5","","F5","F5","F5","","D5","D5","D5","","D5","D5","D5","","","","","",""]
    #logo bitmap
    logo = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xc0\x00\x00\x00\x00\x00\x0f\xff\xf8\x00\x00\x00\x00\x00?\xff\xff\x00\x00\x00\x00\x00\xfe\x00\x1f\xc0\x00\x00\x00\x03\xf0\x1e\x03\xf0\x00\x00\x00\x07\xc3\xff\xf0\xf8\x00\x00\x00\x1f\x1f\xff\xfc<\x00\x00\x00<\x7f\x80\x7f\x1e\x00\x00\x00x\xf8\x00\x0f\xcf\x00\x00\x00\xf3\xe0\x00\x03\xe7\x80\x00\x00\xe7\xc0\x00\x00\xf3\xc0\x00\x01\xcf\x00\x00\x00y\xe0\x00\x03\x8e\x00\x00\x00<\xe0\x00\x03\x8e\x00\x00\x00<\xe0\x00\x03\x9c\x00\x00\x00\x1ep\x00\x078\x00\x00\x00\x0ep\x00\x0fx\x00\x00\x00\x078\x00\x0ep\x00\x00\x00\x07\xb8\x00\x0e\xe0\x00\x00\x00\x03\x9c\x00\x1c\xe0\x00\x00\x00\x01\x9c\x00\x1c\xe0\x00\x00\x00\x01\xcc\x00\x1d\xc0\x00\x00\x00\x01\xce\x00\x19\xc0\x00\x00\x00\x00\xce\x009\xc0\x00\x00\x00\x00\xee\x009\x80\x00\x00\x00\x00\xee\x009\x80\x00\x00\x00\x00\xe6\x00;\x80\x00\x00\x00\x00\xe6\x00;\x80\x00\x00\x00\x00\xe6\x00;\x80\x00\x00\x00\x00\xe6\x009\x80\x00\x00\x00\x00\xe6\x009\x80\x00\x00\x00\x00\xee\x009\xc0\x00\x00\x00\x00\xee\x00\x19\xc0\x00\x00\x00\x00\xce\x00\x1d\xc0\x00\x00\x00\x01\xce\x00\x1c\xc0\x00\x00\x00\x01\xcc\x00\x1c\xe0\x00\x00\x00\x01\xdc\x00\x0e\xe0\x00\x00\x00\x03\x9c\x00\x0ep\x00\x00\x00\x03\x98\x00\x0ex\x00\x00\x00\x078\x00\x078\x00\x00\x00\x0fx\x00\x07\x9c\x00\x00\x00\x00p\x00\x03\x9e\x00\x00\x00\x00 \x00\x01\xcf\x00\x00\x00\x7f\x80\x00\x01\xcf\x00\x00\x00\x7f\x80\x00\x01\xe7\x80\x00\x00\xff\xc0\x00\x00\xf3\xe0\x00\x03\xff\xe0\x00\x00x\xf8\x00\x0f\xc0\xf0\x00\x00<\x7f\x00\x7f\x1ex\x00\x00\x1f\x1f\xff\xfe?<\x00\x00\x0f\x87\xff\xf0\xff\x9e\x00\x00\x03\xe0\x7f\x03\xf3\xcf\x00\x00\x01\xfc\x00\x1f\xc1\xe7\x80\x00\x00\x7f\xff\xff\x00\xf3\xc0\x00\x00\x0f\xff\xfc\x00q\xc0\x00\x00\x01\xff\xc0\x00q\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    
    #Show logo bitmap
    fb = framebuf.FrameBuffer(logo, 60,60, framebuf.MONO_HLSB)
    oled.blit(fb,2,0)
    
    #Set the initial message of display 
    write15.text("QUANTUM", 69,15)
    write15.text("ROBOTICS", 66,35)
    oled.show()
    sleep_ms(4000)
    font = Display_font("font28.txt")
    fontsize = font.font_height
    ssd_font = font.font
    
    def boton_interrupt(pin):
        valor = sensor.read_u16()*3.3/65635
        temp = str(round((27-(valor-0.706)/0.001721),2))
        ssd_text(temp, ssd_font, fontsize,"Temperature",8,8)
    btn.irq(trigger =Pin.IRQ_RISING, handler = boton_interrupt)
 
 
    while True:
        sleep_ms(1000)
        prom = 500
        #read and convert voltage value
        valor = sensor.read_u16()*3.3/65535
        cont = 0
        for i in range(prom):
            val = pot.read_u16()
            cont = cont+val
        valo = cont/prom
            
        temp = str(round((27-(valor-0.706)/0.001721),2))
        volts = valo * FACTOR
        a = str(round(volts,2))
        ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
       
        
        if (volts >12.4 and volts <= 12.8):
            
            valor = sensor.read_u16()*3.3/65535
            cont = 0
            for i in range(prom):
                val = pot.read_u16()
                cont = cont+val
            valo = cont/prom
            volts = valo * FACTOR
            a = str(round(volts,2))
            ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
            oled.show()
            strip.set_pixel(0, red)
            strip.set_pixel(1, red)
            strip.set_pixel(2, red)
            strip.set_pixel(3, red)
            strip.set_pixel(4, red)
            strip.set_pixel(5, red)
            strip.set_pixel(6, red)
            strip.set_pixel(7, red)
            time.sleep(0.01)
            strip.show()
            sleep_ms(3000)
        elif (volts >12.2 and volts <= 12.4):
            
            valor = sensor.read_u16()*3.3/65535
            cont = 0
            for i in range(prom):
                val = pot.read_u16()
                cont = cont+val
            valo = cont/prom
            volts = valo * FACTOR
            a = str(round(volts,2))
            ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
            oled.show()
            strip.set_pixel(0, green)
            strip.set_pixel(1, yellow)
            strip.set_pixel(2, red)
            strip.set_pixel(3, red)
            strip.set_pixel(4, red)
            strip.set_pixel(5, red)
            strip.set_pixel(6, red)
            strip.set_pixel(7, red)
            time.sleep(0.01)
            strip.show()
            sleep_ms(3000)
            
        elif (volts >12.0 and volts <= 12.2):
            valor = sensor.read_u16()*3.3/65535
            cont = 0
            for i in range(prom):
                val = pot.read_u16()
                cont = cont+val
            valo = cont/prom
            volts = valo * FACTOR
            a = str(round(volts,2))
            ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
            oled.show()
            strip.set_pixel(0, green)
            strip.set_pixel(1, green)
            strip.set_pixel(2, yellow)
            strip.set_pixel(3, red)
            strip.set_pixel(4, red)
            strip.set_pixel(5, red)
            strip.set_pixel(6, red)
            strip.set_pixel(7, red)
            time.sleep(0.01)
            strip.show()
            sleep_ms(3000)
        elif (volts >11.8 and volts <= 12.0):
            valor = sensor.read_u16()*3.3/65535
            cont = 0
            for i in range(prom):
                val = pot.read_u16()
                cont = cont+val
            valo = cont/prom
            volts = valo * FACTOR
            a = str(round(volts,2))
            ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
            oled.show()
            strip.set_pixel(0, green)
            strip.set_pixel(1, green)
            strip.set_pixel(2, green)
            strip.set_pixel(3, yellow)
            strip.set_pixel(4, red)
            strip.set_pixel(5, red)
            strip.set_pixel(6, red)
            strip.set_pixel(7, red)
            time.sleep(0.01)
            strip.show()
            sleep_ms(3000)
        elif (volts >11.6 and volts <= 11.8):
            valor = sensor.read_u16()*3.3/65535
            cont = 0
            for i in range(prom):
                val = pot.read_u16()
                cont = cont+val
            valo = cont/prom
            volts = valo * FACTOR
            a = str(round(volts,2))
            ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
            oled.show()
            strip.set_pixel(0, green)
            strip.set_pixel(1, green)
            strip.set_pixel(2, green)
            strip.set_pixel(3, green)
            strip.set_pixel(4, yellow)
            strip.set_pixel(5, red)
            strip.set_pixel(6, red)
            strip.set_pixel(7, red)
            time.sleep(0.01)
            strip.show()
            sleep_ms(3000)
        elif (volts >11.4 and volts <= 12.6):
            valor = sensor.read_u16()*3.3/65535
            cont = 0
            for i in range(prom):
                val = pot.read_u16()
                cont = cont+val
            valo = cont/prom
            volts = valo * FACTOR
            a = str(round(volts,2))
            ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
            oled.show()
            strip.set_pixel(0, green)
            strip.set_pixel(1, green)
            strip.set_pixel(2, green)
            strip.set_pixel(3, green)
            strip.set_pixel(4, green)
            strip.set_pixel(5, yellow)
            strip.set_pixel(6, red)
            strip.set_pixel(7, red)
            time.sleep(0.01)
            strip.show()
            sleep_ms(3000)
        elif (volts >11.2 and volts <= 12.2):
            valor = sensor.read_u16()*3.3/65535
            cont = 0
            for i in range(prom):
                val = pot.read_u16()
                cont = cont+val
            valo = cont/prom
            volts = valo * FACTOR
            a = str(round(volts,2))
            ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
            oled.show()
            strip.set_pixel(0, green)
            strip.set_pixel(1, green)
            strip.set_pixel(2, green)
            strip.set_pixel(3, green)
            strip.set_pixel(4, green)
            strip.set_pixel(5, green)
            strip.set_pixel(6, yellow)
            strip.set_pixel(7, red)
            time.sleep(0.01)
            strip.show()
            sleep_ms(3000)
        elif (volts >11.0 and volts <= 12.2):
            valor = sensor.read_u16()*3.3/65535
            cont = 0
            for i in range(prom):
                val = pot.read_u16()
                cont = cont+val
            valo = cont/prom
            volts = valo * FACTOR
            a = str(round(volts,2))
            ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
            oled.show()
            strip.set_pixel(0, green)
            strip.set_pixel(1, green)
            strip.set_pixel(2, green)
            strip.set_pixel(3, green)
            strip.set_pixel(4, green)
            strip.set_pixel(5, green)
            strip.set_pixel(6, green)
            strip.set_pixel(7, red)
            time.sleep(0.01)
            strip.show()
            sleep_ms(3000)
        
        elif (volts <= 11.0):
            valor = sensor.read_u16()*3.3/65535
            cont = 0
            for i in range(prom):
                val = pot.read_u16()
                cont = cont+val
            valo = cont/prom
            volts = valo * FACTOR
            a = str(round(volts,2))
            ssd_text(a, ssd_font, fontsize,"Voltage",30, 12)
            oled.show()
            strip.set_pixel(0, green)
            strip.set_pixel(1, green)
            strip.set_pixel(2, green)
            strip.set_pixel(3, green)
            strip.set_pixel(4, green)
            strip.set_pixel(5, green)
            strip.set_pixel(6, green)
            strip.set_pixel(7, green)
            time.sleep(0.01)
            strip.show()
            buz.on()
            time.sleep(1)
            buz.off()
            #playsong(song)
            sleep_ms(3000)
        
            