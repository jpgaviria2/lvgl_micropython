# ST7796 Final Test - Focused on Critical Issues
# Based on working ESP-IDF example

import time
from machine import Pin, SPI

print("=== ST7796 FINAL TEST ===")

# Pin configuration from working ESP-IDF example
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6

try:
    print("Initializing hardware...")
    
    # Initialize SPI with ESP-IDF settings
    print("Initializing SPI at 80MHz, Mode 0...")
    spi = SPI(2, baudrate=80000000, polarity=0, phase=0,
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    
    # Initialize backlight
    print("Initializing backlight...")
    backlight = Pin(LCD_BL, Pin.OUT)
    backlight.on()
    
    # Initialize DC pin
    print("Initializing DC pin...")
    dc = Pin(LCD_DC, Pin.OUT)
    
    print("\n=== ST7796 INITIALIZATION ===")
    
    # 1. Software reset
    print("1. Software reset...")
    dc.off()
    spi.write(bytearray([0x01]))
    time.sleep_ms(120)
    
    # 2. Sleep out
    print("2. Sleep out...")
    dc.off()
    spi.write(bytearray([0x11]))
    time.sleep_ms(120)
    
    # 3. Color mode - 16-bit per pixel
    print("3. Setting color mode...")
    dc.off()
    spi.write(bytearray([0x3A]))
    dc.on()
    spi.write(bytearray([0x55]))  # 16-bit color
    
    # 4. Memory access control - CRITICAL: BGR order + mirror X
    print("4. Setting memory access control (BGR + mirror X)...")
    dc.off()
    spi.write(bytearray([0x36]))
    dc.on()
    spi.write(bytearray([0x08]))  # BGR color order, mirror X
    
    # 5. Column address set (0-319)
    print("5. Setting column address...")
    dc.off()
    spi.write(bytearray([0x2A]))
    dc.on()
    spi.write(bytearray([0x00, 0x00, 0x01, 0x3F]))
    
    # 6. Row address set (0-479)
    print("6. Setting row address...")
    dc.off()
    spi.write(bytearray([0x2B]))
    dc.on()
    spi.write(bytearray([0x00, 0x00, 0x01, 0xDF]))
    
    # 7. Display on
    print("7. Turning display on...")
    dc.off()
    spi.write(bytearray([0x29]))
    
    # 8. Color inversion (like ESP-IDF example)
    print("8. Enabling color inversion...")
    dc.off()
    spi.write(bytearray([0x21]))
    
    print("   Initialization complete!")
    
    # Now test with a simple red square
    print("\n=== TESTING DISPLAY ===")
    
    # Set small area (20x20 pixels)
    print("Setting test area (20x20 pixels)...")
    dc.off()  # Column address
    spi.write(bytearray([0x2A]))
    dc.on()
    spi.write(bytearray([0x00, 0x00, 0x00, 0x13]))  # 0-19
    
    dc.off()  # Row address
    spi.write(bytearray([0x2B]))
    dc.on()
    spi.write(bytearray([0x00, 0x00, 0x00, 0x13]))  # 0-19
    
    # Start memory write
    dc.off()
    spi.write(bytearray([0x2C]))
    print("Memory write started")
    
    # Send red pixels - CRITICAL: Use BGR565 format
    print("Sending red pixels in BGR565 format...")
    dc.on()
    
    # BGR565 Red: 0x00F8 (swapped from RGB565 0xF800)
    red_pixel_bgr = bytearray([0x00, 0xF8])  # BGR565 Red
    red_area = red_pixel_bgr * 400  # 20x20 = 400 pixels
    
    spi.write(red_area)
    print("400 red pixels sent in BGR565 format")
    
    print("\n=== TEST COMPLETE ===")
    print("You should see a 20x20 RED square in the top-left corner.")
    print("If you see ANY red pixels, the ST7796 is working!")
    print("If you see nothing, there's a fundamental hardware issue.")
    
    # Wait a moment, then try blue
    time.sleep_ms(2000)
    print("\nNow testing blue...")
    
    # Set same area
    dc.off()
    spi.write(bytearray([0x2A]))
    dc.on()
    spi.write(bytearray([0x00, 0x00, 0x00, 0x13]))
    
    dc.off()
    spi.write(bytearray([0x2B]))
    dc.on()
    spi.write(bytearray([0x00, 0x00, 0x00, 0x13]))
    
    dc.off()
    spi.write(bytearray([0x2C]))
    
    # BGR565 Blue: 0x1F00 (swapped from RGB565 0x001F)
    blue_pixel_bgr = bytearray([0x1F, 0x00])  # BGR565 Blue
    blue_area = blue_pixel_bgr * 400
    
    dc.on()
    spi.write(blue_area)
    print("400 blue pixels sent in BGR565 format")
    
    print("You should now see a BLUE square instead of red.")

except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Test completed")


