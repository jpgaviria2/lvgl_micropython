# Hardware initialization for ESP32-S3-Touch-LCD-3.5
# Works with ESP-IDF v1.26 Generic ESP32-S3 firmware

from machine import Pin, SPI, I2C
import time

# Pin configuration for ESP32-S3-Touch-LCD-3.5
# Based on the existing ESP-IDF examples in this repository

# I2C configuration for touch and other peripherals
I2C_SDA = 8
I2C_SCL = 7
I2C_FREQ = 100000

# SPI configuration for LCD
SPI_SCK = 5
SPI_MOSI = 1
SPI_MISO = 2
SPI_FREQ = 40000000

# LCD pins
LCD_DC = 3
LCD_BL = 6

# Touch configuration
TOUCH_I2C_ADDR = 0x38  # FT6X36 default address

# Display resolution
LCD_WIDTH = 320
LCD_HEIGHT = 480

def init_hardware():
    """Initialize hardware components"""
    try:
        # Initialize I2C for touch and other peripherals
        i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=I2C_FREQ)
        print(f"I2C initialized on SCL={I2C_SCL}, SDA={I2C_SDA}")
        
        # Scan I2C devices
        devices = i2c.scan()
        print(f"I2C devices found: {[hex(addr) for addr in devices]}")
        
        # Initialize SPI for LCD
        spi = SPI(2, baudrate=SPI_FREQ, polarity=0, phase=0, 
                  sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))
        print(f"SPI initialized on SCK={SPI_SCK}, MOSI={SPI_MOSI}, MISO={SPI_MISO}")
        
        # Initialize backlight
        backlight = Pin(LCD_BL, Pin.OUT)
        backlight.on()
        print(f"Backlight initialized on GPIO {LCD_BL}")
        
        # Initialize button
        button = Pin(0, Pin.IN, Pin.PULL_UP)
        print(f"Button initialized on GPIO 0")
        
        return True
        
    except Exception as e:
        print(f"Hardware initialization error: {e}")
        return False

# Initialize hardware
if init_hardware():
    print("Hardware initialization successful")
    print(f"Display: {LCD_WIDTH}x{LCD_HEIGHT}")
    print(f"Touch: FT6X36 on I2C 0x{TOUCH_I2C_ADDR:02X}")
else:
    print("Hardware initialization failed")

print("boot.py finished - ESP32-S3 Touch LCD 3.5 ready")


