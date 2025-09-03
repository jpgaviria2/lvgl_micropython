# SPI Debug Test - Check actual hardware communication
# This will help us see if SPI is working at the hardware level

import time
from machine import Pin, SPI

print("=== SPI HARDWARE DEBUG TEST ===")

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
    
    # Initialize DC pin
    print("Initializing DC pin...")
    dc = Pin(LCD_DC, Pin.OUT)
    dc.off()  # Command mode
    print("DC pin initialized")
    
    # Test 1: Send basic ST7789 commands manually
    print("\nTEST 1: Sending basic ST7789 commands...")
    
    # Sleep out command
    print("Sending SLEEP OUT command...")
    dc.off()  # Command mode
    spi.write(bytearray([0x11]))  # Sleep out
    time.sleep_ms(120)
    print("Sleep out sent")
    
    # Color mode command
    print("Sending COLOR MODE command...")
    dc.off()  # Command mode
    spi.write(bytearray([0x3A]))  # Color mode
    dc.on()   # Data mode
    spi.write(bytearray([0x55]))  # 16-bit color
    print("Color mode sent")
    
    # Memory access control
    print("Sending MEMORY ACCESS CONTROL...")
    dc.off()  # Command mode
    spi.write(bytearray([0x36]))  # Memory access control
    dc.on()   # Data mode
    spi.write(bytearray([0x00]))  # Normal orientation
    print("Memory access control sent")
    
    # Column address set
    print("Sending COLUMN ADDRESS SET...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2A]))  # Column address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x01, 0x3F]))  # 0-319
    print("Column address set sent")
    
    # Row address set
    print("Sending ROW ADDRESS SET...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2B]))  # Row address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x01, 0xDF]))  # 0-479
    print("Row address set sent")
    
    # Display on
    print("Sending DISPLAY ON...")
    dc.off()  # Command mode
    spi.write(bytearray([0x29]))  # Display on
    print("Display on sent")
    
    # Test 2: Try to fill a small area with red
    print("\nTEST 2: Filling small area with RED...")
    
    # Set area to small rectangle (10x10 pixels)
    print("Setting display area to 10x10 pixels...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2A]))  # Column address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))  # 0-9
    
    dc.off()  # Command mode
    spi.write(bytearray([0x2B]))  # Row address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))  # 0-9
    
    # Start memory write
    print("Starting memory write...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2C]))  # Memory write
    
    # Send red pixels (10x10 = 100 pixels, each 2 bytes)
    print("Sending red pixels...")
    dc.on()   # Data mode
    
    # Create red color (RGB565: 0xF800)
    red_data = bytearray(200)  # 100 pixels * 2 bytes each
    for i in range(0, 200, 2):
        red_data[i] = 0xF8     # High byte
        red_data[i + 1] = 0x00 # Low byte
    
    spi.write(red_data)
    print("Red pixels sent - you should see a small red square in top-left corner")
    
    # Test 3: Try to fill entire screen with blue
    print("\nTEST 3: Filling entire screen with BLUE...")
    
    # Set area to full screen
    print("Setting display area to full screen...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2A]))  # Column address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x01, 0x3F]))  # 0-319
    
    dc.off()  # Command mode
    spi.write(bytearray([0x2B]))  # Row address set
    dc.on()   # Data mode
    spi.write(bytearray([0x00, 0x00, 0x01, 0xDF]))  # 0-479
    
    # Start memory write
    print("Starting memory write for full screen...")
    dc.off()  # Command mode
    spi.write(bytearray([0x2C]))  # Memory write
    
    # Send blue pixels in small batches
    print("Sending blue pixels in batches...")
    dc.on()   # Data mode
    
    # Blue color (RGB565: 0x001F)
    blue_data = bytearray(1024)  # 512 pixels * 2 bytes each
    for i in range(0, 1024, 2):
        blue_data[i] = 0x00     # High byte
        blue_data[i + 1] = 0x1F # Low byte
    
    # Send in batches to avoid memory issues
    total_pixels = 320 * 480  # 153,600 pixels
    pixels_sent = 0
    
    while pixels_sent < total_pixels:
        remaining = total_pixels - pixels_sent
        batch_size = min(remaining, 512)  # Send 512 pixels at a time
        
        # Adjust batch data size
        batch_data = blue_data[:batch_size * 2]
        spi.write(batch_data)
        
        pixels_sent += batch_size
        print(f"Sent {pixels_sent}/{total_pixels} pixels...")
        
        # Small delay to avoid overwhelming the system
        time.sleep_ms(10)
    
    print("Blue fill completed - you should see BLUE screen")
    
    print("\n=== SPI DEBUG TEST COMPLETE ===")
    print("If you saw ANY colors, SPI communication is working!")
    print("If you saw nothing, there's a hardware issue.")
    
except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Debug test completed")


