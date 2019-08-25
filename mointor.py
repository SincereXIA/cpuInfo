import Adafruit_Nokia_LCD.PCD8544 as LCD
import os.path as path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Mointor(object):
    # Raspberry Pi software SPI config:
    _SCLK = 17
    _DIN = 18
    _DC = 27
    _RST = 23
    _CS = 22
    _FONT_SIZE = 10

    # LCD config
    _CONTRAST = 60  #对比度 0-127
    _Y_NOW = 0

    def __init__(self, SCLK = _SCLK, DIN = _DIN, DC = _DC, RST = _RST, CS = _CS,
                 CONTRAST = _CONTRAST, FONT_SIZE = 10):
        self._SCLK = SCLK
        self._DIN = DIN
        self._RST = RST
        self._CS = CS
        self._DC = DC
        self._CONTRAST = CONTRAST
        self._FONT_SIZE = FONT_SIZE
        self.setfont()
        # Software SPI usage (defaults to bit-bang SPI interface):
        self._disp = LCD.PCD8544(self._DC, self._RST, self._SCLK, self._DIN, self._CS)

        # Initialize library.
        self._disp.begin(contrast=127)

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self._image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
        # Clear display.
        self._disp.clear()
        self._disp.display()

        draw = ImageDraw.Draw(self._image)
        # Draw a white filled box to clear the image.
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

    
    def println(self, text, font = None, size = _FONT_SIZE):
        dir = path.dirname(__file__)
        if font:
            self.setfont(font, size)
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(self._image)
        if self._Y_NOW + self._FONT_SIZE - 1 > LCD.LCDHEIGHT:
            self._rollUp_()
            
        lineNum = text.strip().count('\n')
        self._rollUp_(self._FONT_SIZE * lineNum)

        draw.text((0,self._Y_NOW), text=text, font=self._font)
        self._disp.image(self._image)
        self._disp.display()
        self._Y_NOW += self._FONT_SIZE * (lineNum+1)
    
    def setfont(self, font = None, size = _FONT_SIZE):
        dir = path.dirname(__file__)
        if font:
            self._font  = ImageFont.truetype(dir+'/fonts/'+font, size = size)
            self._FONT_SIZE = size
        else:
            self._font = ImageFont.load_default()
    
    def _rollUp_(self, size = _FONT_SIZE):
        if size is 0:
            return
        box = (0, size, LCD.LCDWIDTH, LCD.LCDHEIGHT)
        boxNew = (0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT - size)
        part = self._image.crop(box)
        draw = ImageDraw.Draw(self._image)
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        self._image.paste(part, boxNew)
        self._Y_NOW -= size

        
    
    


        
        