# Minimal Display Test - Just show one color
# This will help us identify if the display is working at all

import time
from machine import Pin, SPI

print("=== MINIMAL DISPLAY TEST ===")

# Pin configuration
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6

try:
    # Initialize SPI
    print("Initializing SPI...")
    spi = SPI(2, baudrate=40000000, polarity=0, phase=0, 
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
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
    
    # Try to import streaming driver
    print("Importing streaming driver...")
    from st7789_streaming import ST7789
    print("Driver imported successfully")
    
    # Create display object
    print("Creating display object...")
    display = ST7789(
        spi=spi,
        dc=Pin(LCD_DC),
        cs=None,
        rst=None,
        width=320,
        height=480
    )
    print("Display object created")
    
    # Test 1: Just fill with red
    print("TEST 1: Filling with RED...")
    display.fill(0xF800)  # Red
    print("Red fill completed - you should see RED screen")
    time.sleep(3)
    
    # Test 2: Fill with green
    print("TEST 2: Filling with GREEN...")
    display.fill(0x07E0)  # Green
    print("Green fill completed - you should see GREEN screen")
    time.sleep(3)
    
    # Test 3: Fill with blue
    print("TEST 3: Filling with BLUE...")
    display.fill(0x001F)  # Blue
    print("Blue fill completed - you should see BLUE screen")
    time.sleep(3)
    
    # Test 4: Fill with white
    print("TEST 4: Filling with WHITE...")
    display.fill(0xFFFF)  # White
    print("White fill completed - you should see WHITE screen")
    time.sleep(3)
    
    # Test 5: Fill with black
    print("TEST 5: Filling with BLACK...")
    display.fill(0x0000)  # Black
    print("Black fill completed - you should see BLACK screen")
    time.sleep(3)
    
    print("\n=== MINIMAL TEST COMPLETE ===")
    print("If you saw ANY colors on your LCD screen, the display is working!")
    print("If you saw nothing, there's a hardware communication issue.")
    
    # Final test - draw a small red rectangle in the center
    print("Drawing a small red rectangle in center...")
    display.fill_rect(140, 220, 40, 40, 0xF800)
    print("Rectangle drawn - you should see a small red square in the center")
    
except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Test completed")


