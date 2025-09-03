# ST7796 Comprehensive Test
# Based on the working ESP-IDF example configuration

import time
from machine import Pin, SPI

print("=== ST7796 COMPREHENSIVE TEST ===")

# Pin configuration from working ESP-IDF example
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6

def init_display_comprehensive(spi, dc):
    """Initialize display with comprehensive ST7796 sequence"""
    print("=== COMPREHENSIVE ST7796 INITIALIZATION ===")
    
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
    
    # 4. Memory access control (BGR order, mirror X like ESP-IDF)
    print("4. Setting memory access control...")
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

def test_different_areas(spi, dc):
    """Test different areas of the display"""
    print("\n=== TESTING DIFFERENT DISPLAY AREAS ===")
    
    # Test areas to try
    test_areas = [
        ("Top-left corner", 0, 0, 10, 10),
        ("Center", 155, 235, 10, 10),
        ("Bottom-right", 310, 470, 10, 10),
        ("Top-right", 310, 0, 10, 10),
        ("Bottom-left", 0, 470, 10, 10)
    ]
    
    colors = [
        ("Red", bytearray([0xF8, 0x00] * 50)),      # RGB565 Red
        ("Blue", bytearray([0x00, 0x1F] * 50)),     # RGB565 Blue  
        ("Green", bytearray([0x07, 0xE0] * 50)),    # RGB565 Green
        ("White", bytearray([0xFF, 0xFF] * 50)),    # RGB565 White
        ("Yellow", bytearray([0xFF, 0xE0] * 50))    # RGB565 Yellow
    ]
    
    for area_name, x, y, w, h in test_areas:
        print(f"\n--- Testing {area_name} ({x},{y}) ---")
        
        for color_name, color_data in colors:
            print(f"   Testing {color_name}...")
            
            # Set display area
            dc.off()  # Column address
            spi.write(bytearray([0x2A]))
            dc.on()
            spi.write(bytearray([x >> 8, x & 0xFF, (x + w - 1) >> 8, (x + w - 1) & 0xFF]))
            
            dc.off()  # Row address
            spi.write(bytearray([0x2B]))
            dc.on()
            spi.write(bytearray([y >> 8, y & 0xFF, (y + h - 1) >> 8, (y + h - 1) & 0xFF]))
            
            # Memory write
            dc.off()
            spi.write(bytearray([0x2C]))
            
            # Send color data
            dc.on()
            spi.write(color_data)
            
            time.sleep_ms(500)  # Wait to see the color
            
            print(f"     {color_name} sent to {area_name}")

def test_spi_modes(spi, dc):
    """Test different SPI modes"""
    print("\n=== TESTING DIFFERENT SPI MODES ===")
    
    # Test different SPI configurations
    spi_configs = [
        ("Mode 0 (polarity=0, phase=0)", 0, 0),
        ("Mode 1 (polarity=0, phase=1)", 0, 1),
        ("Mode 2 (polarity=1, phase=0)", 1, 0),
        ("Mode 3 (polarity=1, phase=1)", 1, 1)
    ]
    
    for mode_name, polarity, phase in spi_configs:
        print(f"\n--- Testing {mode_name} ---")
        
        # Reinitialize SPI with new mode
        new_spi = SPI(2, baudrate=80000000, polarity=polarity, phase=phase,
                      sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
        
        # Try to send a simple command
        try:
            dc.off()
            new_spi.write(bytearray([0x00]))  # NOP
            print(f"   NOP command sent successfully")
            
            # Try to set a small area and send red pixels
            dc.off()
            new_spi.write(bytearray([0x2A]))  # Column address
            dc.on()
            new_spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
            
            dc.off()
            new_spi.write(bytearray([0x2B]))  # Row address
            dc.on()
            new_spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
            
            dc.off()
            new_spi.write(bytearray([0x2C]))  # Memory write
            
            dc.on()
            red_pixels = bytearray([0xF8, 0x00] * 50)  # 10x10 red pixels
            new_spi.write(red_pixels)
            
            print(f"   Red pixels sent - look for red square")
            
        except Exception as e:
            print(f"   Error: {e}")
        
        time.sleep_ms(1000)

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
    
    # Comprehensive display initialization
    init_display_comprehensive(spi, dc)
    
    # Test different display areas
    test_different_areas(spi, dc)
    
    # Test different SPI modes
    test_spi_modes(spi, dc)
    
    print("\n=== COMPREHENSIVE TEST COMPLETE ===")
    print("If you saw ANY colored squares, the display is working!")
    print("If you still see nothing, there's a fundamental hardware issue.")
    print("Check:")
    print("1. Display connections (MOSI, SCK, DC, BL)")
    print("2. Power supply to the display")
    print("3. Display controller type (ST7796 vs ST7789)")
    print("4. Hardware reset circuit")

except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Test completed")


