# ST7796 Test with TCA9554 Hardware Reset
# Based on working Arduino example

import time
from machine import Pin, SPI, I2C

print("=== ST7796 WITH TCA9554 RESET TEST ===")

# Pin configuration
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6
I2C_SDA = 8
I2C_SCL = 7

# TCA9554 I2C address
TCA9554_ADDR = 0x20

def tca9554_reset():
    """Reset the display using TCA9554 pin 1"""
    print("=== TCA9554 HARDWARE RESET ===")
    
    try:
        # Initialize I2C
        i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)
        print("I2C initialized")
        
        # Scan for devices
        devices = i2c.scan()
        print(f"I2C devices found: {[hex(addr) for addr in devices]}")
        
        if TCA9554_ADDR not in devices:
            print(f"ERROR: TCA9554 not found at {hex(TCA9554_ADDR)}")
            return False
        
        # TCA9554 configuration sequence
        # 1. Set pin 1 as output
        print("1. Setting TCA9554 pin 1 as output...")
        i2c.writeto_mem(TCA9554_ADDR, 0x03, bytearray([0xFE]))  # Port 1 direction (pin 1 = output)
        
        # 2. Set pin 1 HIGH
        print("2. Setting pin 1 HIGH...")
        i2c.writeto_mem(TCA9554_ADDR, 0x01, bytearray([0x02]))  # Port 1 output (pin 1 = HIGH)
        time.sleep_ms(10)
        
        # 3. Set pin 1 LOW (reset)
        print("3. Setting pin 1 LOW (reset)...")
        i2c.writeto_mem(TCA9554_ADDR, 0x01, bytearray([0x00]))  # Port 1 output (pin 1 = LOW)
        time.sleep_ms(10)
        
        # 4. Set pin 1 HIGH
        print("4. Setting pin 1 HIGH...")
        i2c.writeto_mem(TCA9554_ADDR, 0x01, bytearray([0x02]))  # Port 1 output (pin 1 = HIGH)
        time.sleep_ms(200)
        
        print("   Hardware reset complete!")
        return True
        
    except Exception as e:
        print(f"TCA9554 reset error: {e}")
        return False

def init_display_st7796(spi, dc):
    """Initialize ST7796 display"""
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
    
    # 4. Memory access control (BGR order + mirror X)
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
    
    # 8. Color inversion
    print("8. Enabling color inversion...")
    dc.off()
    spi.write(bytearray([0x21]))
    
    print("   ST7796 initialization complete!")

def create_color_data(color_bytes, pixel_count):
    """Create color data for specified number of pixels"""
    data = bytearray()
    for _ in range(pixel_count):
        data.extend(color_bytes)
    return data

def test_display(spi, dc):
    """Test the display with colored squares"""
    print("\n=== TESTING DISPLAY ===")
    
    # Test areas
    test_areas = [
        ("Top-left", 0, 0, 20, 20),
        ("Center", 150, 230, 20, 20),
        ("Bottom-right", 300, 460, 20, 20)
    ]
    
    colors = [
        ("Red", bytearray([0x00, 0xF8])),      # BGR565 Red
        ("Blue", bytearray([0x1F, 0x00])),     # BGR565 Blue
        ("Green", bytearray([0xE0, 0x07]))     # BGR565 Green
    ]
    
    for area_name, x, y, w, h in test_areas:
        print(f"\n--- Testing {area_name} ({x},{y}) ---")
        
        for color_name, color_data in colors:
            print(f"   Testing {color_name}...")
            
            # Set display area
            dc.off()
            spi.write(bytearray([0x2A]))
            dc.on()
            spi.write(bytearray([x >> 8, x & 0xFF, (x + w - 1) >> 8, (x + w - 1) & 0xFF]))
            
            dc.off()
            spi.write(bytearray([0x2B]))
            dc.on()
            spi.write(bytearray([y >> 8, y & 0xFF, (y + h - 1) >> 8, (y + h - 1) & 0xFF]))
            
            # Memory write
            dc.off()
            spi.write(bytearray([0x2C]))
            
            # Send color data
            dc.on()
            pixels = create_color_data(color_data, w * h)
            spi.write(pixels)
            
            print(f"     {color_name} sent to {area_name}")
            time.sleep_ms(1000)  # Wait to see the color

try:
    print("Initializing hardware...")
    
    # 1. Hardware reset via TCA9554
    if not tca9554_reset():
        print("WARNING: Hardware reset failed, continuing anyway...")
    
    # 2. Initialize SPI
    print("\nInitializing SPI at 80MHz, Mode 0...")
    spi = SPI(2, baudrate=80000000, polarity=0, phase=0,
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    
    # 3. Initialize backlight
    print("Initializing backlight...")
    backlight = Pin(LCD_BL, Pin.OUT)
    backlight.on()
    
    # 4. Initialize DC pin
    print("Initializing DC pin...")
    dc = Pin(LCD_DC, Pin.OUT)
    
    # 5. Initialize ST7796 display
    init_display_st7796(spi, dc)
    
    # 6. Test display
    test_display(spi, dc)
    
    print("\n=== TEST COMPLETE ===")
    print("If you saw ANY colored squares, the display is working!")
    print("The TCA9554 hardware reset was the missing piece!")

except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Test completed")
