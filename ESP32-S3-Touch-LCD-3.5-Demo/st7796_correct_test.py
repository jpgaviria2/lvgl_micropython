# ST7796 Correct Configuration Test
# Based on the working ESP-IDF example

import time
from machine import Pin, SPI

print("=== ST7796 CORRECT CONFIGURATION TEST ===")

# Pin configuration from working ESP-IDF example
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6

try:
    # Initialize SPI with correct settings from ESP-IDF example
    print("Initializing SPI with ESP-IDF settings...")
    spi = SPI(2, baudrate=80000000, polarity=0, phase=0,  # Mode 0, 80MHz
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    print("SPI initialized at 80MHz, Mode 0")

    # Initialize backlight
    print("Initializing backlight...")
    backlight = Pin(LCD_BL, Pin.OUT)
    backlight.on()
    print("Backlight enabled")

    # Initialize DC pin
    print("Initializing DC pin...")
    dc = Pin(LCD_DC, Pin.OUT)
    print("DC pin initialized")

    # ST7796 specific initialization sequence
    print("\n=== ST7796 INITIALIZATION ===")
    
    # 1. Software reset
    print("1. Software reset...")
    dc.off()  # Command mode
    spi.write(bytearray([0x01]))  # Software reset
    time.sleep_ms(120)
    print("   Software reset sent")

    # 2. Sleep out
    print("2. Sleep out...")
    dc.off()  # Command mode
    spi.write(bytearray([0x11]))  # Sleep out
    time.sleep_ms(120)
    print("   Sleep out sent")

    # 3. Color mode - 16-bit per pixel
    print("3. Setting color mode...")
    dc.off()  # Command mode
    spi.write(bytearray([0x3A]))  # COLMOD
    dc.on()   # Data mode
    spi.write(bytearray([0x55]))  # 16-bit color
    print("   Color mode set to 16-bit")

    # 4. Memory access control (BGR order like ESP-IDF example)
    print("4. Setting memory access control...")
    dc.off()  # Command mode
    spi.write(bytearray([0x36]))  # MADCTL
    dc.on()   # Data mode
    spi.write(bytearray([0x08]))  # BGR color order, normal orientation
    print("   Memory access control set")

    # 5. Column address set (0-319)
    print("5. Setting column address...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2A]))  # CASET
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x01, 0x3F]))  # 0-319
    print("   Column address set to 0-319")

    # 6. Row address set (0-479)
    print("6. Setting row address...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2B]))  # RASET
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x01, 0xDF]))  # 0-479
    print("   Row address set to 0-479")

    # 7. Display on
    print("7. Turning display on...")
    dc.off()  # Command mode
    spi.write(bytearray([0x29]))  # Display on
    print("   Display on command sent")

    # 8. Color inversion (like ESP-IDF example)
    print("8. Enabling color inversion...")
    dc.off()  # Command mode
    spi.write(bytearray([0x21]))  # INVON
    print("   Color inversion enabled")

    print("\n=== ST7796 INITIALIZATION COMPLETE ===")

    # Now test with a small red area
    print("\n=== TESTING DISPLAY ===")
    
    # Set a small area (10x10 pixels)
    print("Setting test area (10x10 pixels)...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2A]))  # Column address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))  # 0-9

    dc.off()  # Command mode
    spi.write(bytearray([0x2B]))  # Row address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))  # 0-9

    # Start memory write
    dc.off()  # Command mode
    spi.write(bytearray([0x2C]))  # Memory write
    print("Memory write started")

    # Send red pixels (BGR565 format: 0xF800)
    print("Sending 100 red pixels...")
    dc.on()   # Data mode
    
    # Create red pixel data (BGR565: 0xF800)
    red_pixel = bytearray([0xF8, 0x00])  # One red pixel
    red_area = red_pixel * 100  # 100 red pixels
    
    spi.write(red_area)
    print("100 red pixels sent - you should see a 10x10 red square in top-left corner")

    print("\n=== TEST COMPLETE ===")
    print("If you see a red square, the ST7796 is working!")
    print("If you still see nothing, there's a hardware issue.")

except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Test completed")


