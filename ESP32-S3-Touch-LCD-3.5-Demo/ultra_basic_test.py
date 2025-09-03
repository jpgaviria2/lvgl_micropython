# Ultra-Basic Display Test - Bypass driver completely
# This will test raw SPI communication to the display

import time
from machine import Pin, SPI

print("=== ULTRA-BASIC DISPLAY TEST ===")

# Pin configuration
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6

try:
    # Initialize SPI with lower speed first
    print("Initializing SPI at 1MHz...")
    spi = SPI(2, baudrate=1000000, polarity=0, phase=0, 
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    print("SPI initialized at 1MHz")
    
    # Initialize backlight
    print("Initializing backlight...")
    backlight = Pin(LCD_BL, Pin.OUT)
    backlight.on()
    print("Backlight enabled")
    
    # Initialize DC pin
    print("Initializing DC pin...")
    dc = Pin(LCD_DC, Pin.OUT)
    print("DC pin initialized")
    
    # Test 1: Just send a single command
    print("\nTEST 1: Sending single command...")
    dc.off()  # Command mode
    spi.write(bytearray([0x00]))  # NOP command
    print("NOP command sent")
    
    # Test 2: Send sleep out command
    print("\nTEST 2: Sending SLEEP OUT...")
    dc.off()  # Command mode
    spi.write(bytearray([0x11]))  # Sleep out
    time.sleep_ms(120)
    print("Sleep out sent")
    
    # Test 3: Send display on command
    print("\nTEST 3: Sending DISPLAY ON...")
    dc.off()  # Command mode
    spi.write(bytearray([0x29]))  # Display on
    print("Display on sent")
    
    # Test 4: Try to set a small area and send data
    print("\nTEST 4: Setting small area...")
    
    # Set column address (just 10 pixels)
    dc.off()  # Command mode
    spi.write(bytearray([0x2A]))  # Column address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))  # 0-9
    print("Column address set")
    
    # Set row address (just 10 pixels)
    dc.off()  # Command mode
    spi.write(bytearray([0x2B]))  # Row address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))  # 0-9
    print("Row address set")
    
    # Start memory write
    dc.off()  # Command mode
    spi.write(bytearray([0x2C]))  # Memory write
    print("Memory write started")
    
    # Send just 4 pixels of red (8 bytes total)
    print("Sending 4 red pixels...")
    dc.on()   # Data mode
    
    # Red color in RGB565: 0xF800
    red_pixels = bytearray([0xF8, 0x00, 0xF8, 0x00, 0xF8, 0x00, 0xF8, 0x00])
    spi.write(red_pixels)
    print("4 red pixels sent - you should see 4 red dots in top-left corner")
    
    print("\n=== ULTRA-BASIC TEST COMPLETE ===")
    print("If you saw ANY red dots, the display is responding!")
    print("If you saw nothing, there's a fundamental hardware issue.")
    
except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Test completed")
