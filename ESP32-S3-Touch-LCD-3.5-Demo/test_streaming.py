# Test Streaming Display Driver for ESP32-S3 Touch LCD 3.5
# This will test if the memory-efficient driver works

import time
from machine import Pin, SPI, I2C

print("Starting Streaming Display Test...")

# Pin configuration
I2C_SDA = 8
I2C_SCL = 7
SPI_SCK = 5
SPI_MOSI = 1
SPI_MISO = 2
LCD_DC = 3
LCD_BL = 6

try:
    # Initialize I2C
    print("Initializing I2C...")
    i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)
    devices = i2c.scan()
    print(f"I2C devices found: {[hex(addr) for addr in devices]}")
    
    # Initialize SPI
    print("Initializing SPI...")
    spi = SPI(2, baudrate=40000000, polarity=0, phase=0, 
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))
    print("SPI initialized")
    
    # Initialize backlight
    print("Initializing backlight...")
    backlight = Pin(LCD_BL, Pin.OUT)
    backlight.on()
    print("Backlight enabled")
    
    # Test backlight control
    print("Testing backlight...")
    backlight.off()
    time.sleep(1)
    backlight.on()
    print("Backlight test complete")
    
    # Try to import and test streaming display driver
    print("Testing streaming display driver...")
    try:
        from st7789_streaming import ST7789
        
        # Create display object
        display = ST7789(
            spi=spi,
            dc=Pin(LCD_DC),
            cs=None,
            rst=None,
            width=320,
            height=480
        )
        
        print("Streaming display driver loaded successfully!")
        
        # Test basic display functions
        print("Testing display functions...")
        
        # Clear display
        display.clear()
        print("Display cleared")
        
        # Fill with different colors
        colors = [
            (0x0000, "Black"),
            (0xF800, "Red"),
            (0x07E0, "Green"),
            (0x001F, "Blue"),
            (0xFFFF, "White")
        ]
        
        for color, name in colors:
            print(f"Filling with {name}...")
            display.fill(color)
            time.sleep(1)
        
        # Draw some shapes
        print("Drawing shapes...")
        display.fill(0x0000)  # Black background
        
        # Draw a red rectangle
        display.draw_rect(50, 50, 100, 50, 0xF800, fill=True)
        
        # Draw a green circle
        display.draw_circle(200, 100, 30, 0x07E0, fill=True)
        
        # Draw some text
        display.draw_text("Streaming Test", 100, 250, 0xFFFF)
        display.draw_text("Working!", 120, 280, 0xFFFF)
        
        print("Shapes drawn successfully!")
        
        # Test touch driver
        print("Testing touch driver...")
        try:
            from ft6x36_driver import FT6X36
            
            # Create touch object
            touch = FT6X36(i2c, addr=0x38)
            print("Touch driver loaded successfully!")
            
            # Test touch reading
            print("Touch test - touch the screen or press button to continue...")
            for i in range(50):  # Test for 5 seconds
                touch_data = touch.read_touch()
                if touch_data:
                    print(f"Touch detected at ({touch_data['x']}, {touch_data['y']})")
                    break
                time.sleep_ms(100)
            
            print("Touch test completed")
            
        except Exception as e:
            print(f"Touch driver error: {e}")
        
        print("\n=== STREAMING DISPLAY TEST COMPLETE ===")
        print("If you can see colors and shapes on your LCD screen,")
        print("your MicroPythonOS streaming display is working perfectly!")
        print("Press the button or restart to continue...")
        
        # Wait for button press
        button = Pin(0, Pin.IN, Pin.PULL_UP)
        while button.value() == 1:
            time.sleep_ms(100)
        
    except Exception as e:
        print(f"Streaming display driver error: {e}")
        print("Please ensure st7789_streaming.py is uploaded to the device")
    
except Exception as e:
    print(f"Hardware initialization error: {e}")

print("Test completed")


