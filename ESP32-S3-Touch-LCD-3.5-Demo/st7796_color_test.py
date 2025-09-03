# ST7796 Color Format Test
# Testing different color formats and initialization sequences

import time
from machine import Pin, SPI

print("=== ST7796 COLOR FORMAT TEST ===")

# Pin configuration
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6

def init_display(spi, dc):
    """Initialize display with basic commands"""
    # Software reset
    dc.off()
    spi.write(bytearray([0x01]))
    time.sleep_ms(120)
    
    # Sleep out
    dc.off()
    spi.write(bytearray([0x11]))
    time.sleep_ms(120)
    
    # Display on
    dc.off()
    spi.write(bytearray([0x29]))

def test_colors(spi, dc, color_name, color_data):
    """Test a specific color format"""
    print(f"\n--- Testing {color_name} ---")
    
    # Set small area (5x5 pixels)
    dc.off()  # Column address
    spi.write(bytearray([0x2A]))
    dc.on()
    spi.write(bytearray([0x00, 0x00, 0x00, 0x04]))
    
    dc.off()  # Row address
    spi.write(bytearray([0x2B]))
    dc.on()
    spi.write(bytearray([0x00, 0x00, 0x00, 0x04]))
    
    # Memory write
    dc.off()
    spi.write(bytearray([0x2C]))
    
    # Send color data
    dc.on()
    spi.write(color_data)
    print(f"   {color_name} sent - look for 5x5 square")

try:
    # Initialize SPI
    print("Initializing SPI...")
    spi = SPI(2, baudrate=80000000, polarity=0, phase=0,
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    
    # Initialize backlight
    backlight = Pin(LCD_BL, Pin.OUT)
    backlight.on()
    
    # Initialize DC pin
    dc = Pin(LCD_DC, Pin.OUT)
    
    # Initialize display
    print("Initializing display...")
    init_display(spi, dc)
    
    # Test different color formats
    print("\n=== TESTING DIFFERENT COLOR FORMATS ===")
    
    # Test 1: RGB565 Red (0xF800)
    red_rgb = bytearray([0xF8, 0x00] * 25)  # 5x5 = 25 pixels
    test_colors(spi, dc, "RGB565 Red", red_rgb)
    
    time.sleep_ms(1000)
    
    # Test 2: BGR565 Red (0x00F8) - swapped bytes
    red_bgr = bytearray([0x00, 0xF8] * 25)
    test_colors(spi, dc, "BGR565 Red", red_bgr)
    
    time.sleep_ms(1000)
    
    # Test 3: RGB565 Blue (0x001F)
    blue_rgb = bytearray([0x00, 0x1F] * 25)
    test_colors(spi, dc, "RGB565 Blue", blue_rgb)
    
    time.sleep_ms(1000)
    
    # Test 4: BGR565 Blue (0x1F00) - swapped bytes
    blue_bgr = bytearray([0x1F, 0x00] * 25)
    test_colors(spi, dc, "BGR565 Blue", blue_bgr)
    
    time.sleep_ms(1000)
    
    # Test 5: RGB565 Green (0x07E0)
    green_rgb = bytearray([0x07, 0xE0] * 25)
    test_colors(spi, dc, "RGB565 Green", green_rgb)
    
    time.sleep_ms(1000)
    
    # Test 6: BGR565 Green (0xE007) - swapped bytes
    green_bgr = bytearray([0xE0, 0x07] * 25)
    test_colors(spi, dc, "BGR565 Green", green_bgr)
    
    print("\n=== ALL TESTS COMPLETE ===")
    print("Look for colored squares appearing on the display.")
    print("If you see ANY colored squares, the display is working!")
    print("If you see nothing, there's a fundamental hardware issue.")

except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Test completed")


