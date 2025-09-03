# Display Controller Test - Try different display types
# Since SPI is working but no output, let's try different controllers

import time
from machine import Pin, SPI

print("=== DISPLAY CONTROLLER TEST ===")

# Pin configuration
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6

try:
    # Initialize SPI
    print("Initializing SPI...")
    spi = SPI(2, baudrate=1000000, polarity=0, phase=0, 
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    print("SPI initialized")
    
    # Initialize backlight
    print("Initializing backlight...")
    backlight = Pin(LCD_BL, Pin.OUT)
    backlight.on()
    print("Backlight enabled")
    
    # Initialize DC pin
    print("Initializing DC pin...")
    dc = Pin(LCD_DC, Pin.OUT)
    print("DC pin initialized")
    
    # Test 1: Try ST7789 commands (what we were using)
    print("\nTEST 1: ST7789 Commands...")
    dc.off()  # Command mode
    spi.write(bytearray([0x11]))  # Sleep out
    time.sleep_ms(120)
    dc.off()  # Command mode
    spi.write(bytearray([0x29]))  # Display on
    print("ST7789 commands sent")
    
    # Test 2: Try ILI9488 commands (different controller)
    print("\nTEST 2: ILI9488 Commands...")
    dc.off()  # Command mode
    spi.write(bytearray([0x11]))  # Sleep out
    time.sleep_ms(120)
    dc.off()  # Command mode
    spi.write(bytearray([0x29]))  # Display on
    print("ILI9488 commands sent")
    
    # Test 3: Try ST7735 commands (another common controller)
    print("\nTEST 3: ST7735 Commands...")
    dc.off()  # Command mode
    spi.write(bytearray([0x11]))  # Sleep out
    time.sleep_ms(120)
    dc.off()  # Command mode
    spi.write(bytearray([0x29]))  # Display on
    print("ST7735 commands sent")
    
    # Test 4: Try different resolution settings
    print("\nTEST 4: Different Resolutions...")
    
    # Try 240x320 (common for smaller displays)
    print("Trying 240x320 resolution...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2A]))  # Column address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x00, 0xEF]))  # 0-239
    
    dc.off()  # Command mode
    spi.write(bytearray([0x2B]))  # Row address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x01, 0x3F]))  # 0-319
    
    # Try to draw a small red area
    dc.off()  # Command mode
    spi.write(bytearray([0x2C]))  # Memory write
    dc.on()   # Data mode
    
    # Send 10x10 red pixels
    red_data = bytearray(200)  # 10x10 * 2 bytes per pixel
    for i in range(0, 200, 2):
        red_data[i] = 0xF8     # High byte
        red_data[i + 1] = 0x00 # Low byte
    
    spi.write(red_data)
    print("10x10 red area sent for 240x320")
    
    # Test 5: Try 480x320 (landscape orientation)
    print("\nTEST 5: Trying 480x320 resolution...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2A]))  # Column address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x01, 0xDF]))  # 0-479
    
    dc.off()  # Command mode
    spi.write(bytearray([0x2B]))  # Row address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x01, 0x3F]))  # 0-319
    
    # Try to draw a small blue area
    dc.off()  # Command mode
    spi.write(bytearray([0x2C]))  # Memory write
    dc.on()   # Data mode
    
    # Send 10x10 blue pixels
    blue_data = bytearray(200)  # 10x10 * 2 bytes per pixel
    for i in range(0, 200, 2):
        blue_data[i] = 0x00     # High byte
        blue_data[i + 1] = 0x1F # Low byte
    
    spi.write(blue_data)
    print("10x10 blue area sent for 480x320")
    
    print("\n=== DISPLAY CONTROLLER TEST COMPLETE ===")
    print("Check your screen for:")
    print("- Red dots in top-left (240x320 test)")
    print("- Blue dots somewhere (480x320 test)")
    print("If you see ANYTHING, we know the display type!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Test completed")


