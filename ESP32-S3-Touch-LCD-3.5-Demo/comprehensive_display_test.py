# Comprehensive Display Test - Multiple Approaches
# Testing different methods to get the ST7796 display working

import time
from machine import Pin, SPI, I2C

print("=== COMPREHENSIVE DISPLAY TEST ===")

# Pin configuration
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6
I2C_SDA = 8
I2C_SCL = 7

def approach_1_arduino_style():
    """Approach 1: Arduino-style with TCA9554 reset"""
    print("\n=== APPROACH 1: ARDUINO-STYLE WITH TCA9554 ===")
    
    try:
        # Initialize I2C and TCA9554
        print("1. Initializing TCA9554...")
        i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)
        devices = i2c.scan()
        print(f"   I2C devices: {[hex(addr) for addr in devices]}")
        
        if 0x20 not in devices:
            print("   ERROR: TCA9554 not found!")
            return False
        
        # TCA9554 reset sequence (like Arduino example)
        print("2. Performing TCA9554 reset...")
        i2c.writeto_mem(0x20, 0x07, bytearray([0xFE]))  # Port 1 direction
        i2c.writeto_mem(0x20, 0x03, bytearray([0x02]))  # Pin 1 HIGH
        time.sleep_ms(10)
        i2c.writeto_mem(0x20, 0x03, bytearray([0x00]))  # Pin 1 LOW (reset)
        time.sleep_ms(10)
        i2c.writeto_mem(0x20, 0x03, bytearray([0x02]))  # Pin 1 HIGH
        time.sleep_ms(200)
        print("   TCA9554 reset completed")
        
        # Initialize SPI and display
        print("3. Initializing SPI and display...")
        spi = SPI(2, baudrate=80000000, polarity=0, phase=0,
                  sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
        dc = Pin(LCD_DC, Pin.OUT)
        backlight = Pin(LCD_BL, Pin.OUT)
        backlight.on()
        
        # ST7796 initialization
        print("4. ST7796 initialization...")
        dc.off()
        spi.write(bytearray([0x01]))  # Software reset
        time.sleep_ms(120)
        
        dc.off()
        spi.write(bytearray([0x11]))  # Sleep out
        time.sleep_ms(120)
        
        dc.off()
        spi.write(bytearray([0x3A]))  # Color mode
        dc.on()
        spi.write(bytearray([0x55]))  # 16-bit
        
        dc.off()
        spi.write(bytearray([0x36]))  # Memory access
        dc.on()
        spi.write(bytearray([0x08]))  # BGR + mirror X
        
        dc.off()
        spi.write(bytearray([0x29]))  # Display on
        
        # Test display
        print("5. Testing display...")
        dc.off()
        spi.write(bytearray([0x2A]))  # Column
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
        
        dc.off()
        spi.write(bytearray([0x2B]))  # Row
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
        
        dc.off()
        spi.write(bytearray([0x2C]))  # Memory write
        
        # Send red pixels
        dc.on()
        red_data = bytearray()
        for _ in range(100):  # 10x10
            red_data.extend(bytearray([0x00, 0xF8]))  # BGR565 Red
        
        spi.write(red_data)
        print("   Red pixels sent - look for red square")
        
        return True
        
    except Exception as e:
        print(f"   Approach 1 failed: {e}")
        return False

def approach_2_esp_idf_style():
    """Approach 2: ESP-IDF style with different timing"""
    print("\n=== APPROACH 2: ESP-IDF STYLE ===")
    
    try:
        # Initialize SPI
        print("1. Initializing SPI...")
        spi = SPI(2, baudrate=80000000, polarity=0, phase=0,
                  sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
        dc = Pin(LCD_DC, Pin.OUT)
        backlight = Pin(LCD_BL, Pin.OUT)
        backlight.on()
        
        # ESP-IDF style initialization
        print("2. ESP-IDF style initialization...")
        
        # Software reset
        dc.off()
        spi.write(bytearray([0x01]))
        time.sleep_ms(200)  # Longer delay
        
        # Sleep out
        dc.off()
        spi.write(bytearray([0x11]))
        time.sleep_ms(200)  # Longer delay
        
        # Color mode
        dc.off()
        spi.write(bytearray([0x3A]))
        dc.on()
        spi.write(bytearray([0x55]))
        
        # Memory access control
        dc.off()
        spi.write(bytearray([0x36]))
        dc.on()
        spi.write(bytearray([0x08]))
        
        # Column address
        dc.off()
        spi.write(bytearray([0x2A]))
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x01, 0x3F]))
        
        # Row address
        dc.off()
        spi.write(bytearray([0x2B]))
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x01, 0xDF]))
        
        # Display on
        dc.off()
        spi.write(bytearray([0x29]))
        
        # Color inversion
        dc.off()
        spi.write(bytearray([0x21]))
        
        # Test display
        print("3. Testing display...")
        dc.off()
        spi.write(bytearray([0x2A]))
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
        
        dc.off()
        spi.write(bytearray([0x2B]))
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
        
        dc.off()
        spi.write(bytearray([0x2C]))
        
        # Send blue pixels
        dc.on()
        blue_data = bytearray()
        for _ in range(100):
            blue_data.extend(bytearray([0x1F, 0x00]))  # BGR565 Blue
        
        spi.write(blue_data)
        print("   Blue pixels sent - look for blue square")
        
        return True
        
    except Exception as e:
        print(f"   Approach 2 failed: {e}")
        return False

def approach_3_ultra_simple():
    """Approach 3: Ultra-simple, just basic commands"""
    print("\n=== APPROACH 3: ULTRA-SIMPLE ===")
    
    try:
        # Initialize with very low speed
        print("1. Initializing SPI at 1MHz...")
        spi = SPI(2, baudrate=1000000, polarity=0, phase=0,
                  sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
        dc = Pin(LCD_DC, Pin.OUT)
        backlight = Pin(LCD_BL, Pin.OUT)
        backlight.on()
        
        # Just try to wake up and turn on
        print("2. Sending basic commands...")
        dc.off()
        spi.write(bytearray([0x11]))  # Sleep out
        time.sleep_ms(200)
        
        dc.off()
        spi.write(bytearray([0x29]))  # Display on
        time.sleep_ms(100)
        
        # Try to set a tiny area
        print("3. Testing tiny area...")
        dc.off()
        spi.write(bytearray([0x2A]))
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x04]))
        
        dc.off()
        spi.write(bytearray([0x2B]))
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x04]))
        
        dc.off()
        spi.write(bytearray([0x2C]))
        
        # Send white pixels
        dc.on()
        white_data = bytearray()
        for _ in range(25):  # 5x5
            white_data.extend(bytearray([0xFF, 0xFF]))
        
        spi.write(white_data)
        print("   White pixels sent - look for tiny white square")
        
        return True
        
    except Exception as e:
        print(f"   Approach 3 failed: {e}")
        return False

def approach_4_different_controller():
    """Approach 4: Try different display controller commands"""
    print("\n=== APPROACH 4: DIFFERENT CONTROLLER ===")
    
    try:
        # Initialize SPI
        print("1. Initializing SPI...")
        spi = SPI(2, baudrate=10000000, polarity=0, phase=0,
                  sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
        dc = Pin(LCD_DC, Pin.OUT)
        backlight = Pin(LCD_BL, Pin.OUT)
        backlight.on()
        
        # Try ST7789 commands instead
        print("2. Trying ST7789 commands...")
        dc.off()
        spi.write(bytearray([0x11]))  # Sleep out
        time.sleep_ms(120)
        
        dc.off()
        spi.write(bytearray([0x3A]))  # Color mode
        dc.on()
        spi.write(bytearray([0x05]))  # 16-bit color
        
        dc.off()
        spi.write(bytearray([0x36]))  # Memory access
        dc.on()
        spi.write(bytearray([0x00]))  # Normal orientation
        
        dc.off()
        spi.write(bytearray([0x29]))  # Display on
        
        # Test display
        print("3. Testing display...")
        dc.off()
        spi.write(bytearray([0x2A]))
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
        
        dc.off()
        spi.write(bytearray([0x2B]))
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
        
        dc.off()
        spi.write(bytearray([0x2C]))
        
        # Send green pixels
        dc.on()
        green_data = bytearray()
        for _ in range(100):
            green_data.extend(bytearray([0x07, 0xE0]))  # RGB565 Green
        
        spi.write(green_data)
        print("   Green pixels sent - look for green square")
        
        return True
        
    except Exception as e:
        print(f"   Approach 4 failed: {e}")
        return False

try:
    print("Starting comprehensive display test...")
    
    # Test all approaches
    approaches = [
        ("Arduino-style with TCA9554", approach_1_arduino_style),
        ("ESP-IDF style", approach_2_esp_idf_style),
        ("Ultra-simple", approach_3_ultra_simple),
        ("Different controller", approach_4_different_controller)
    ]
    
    for approach_name, approach_func in approaches:
        print(f"\n{'='*60}")
        print(f"TESTING: {approach_name}")
        print(f"{'='*60}")
        
        if approach_func():
            print(f"✓ {approach_name} completed successfully")
            print("   Look for colored squares on the display!")
            time.sleep_ms(3000)  # Wait to see the result
        else:
            print(f"✗ {approach_name} failed")
        
        time.sleep_ms(1000)
    
    print("\n=== COMPREHENSIVE TEST COMPLETE ===")
    print("If any approach worked, you should have seen colored squares.")
    print("If none worked, there's a fundamental hardware issue.")
    print("Check:")
    print("1. Display power supply")
    print("2. SPI connections (MOSI, SCK, DC)")
    print("3. Display controller type")
    print("4. Hardware reset circuit")

except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Comprehensive test completed")


