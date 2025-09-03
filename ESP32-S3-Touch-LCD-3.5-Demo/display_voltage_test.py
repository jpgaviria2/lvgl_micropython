# Display Voltage and Power Test
# Testing different voltage levels and initialization approaches

import time
from machine import Pin, SPI, I2C

print("=== DISPLAY VOLTAGE AND POWER TEST ===")

# Pin configuration
SPI_SCK = 5
SPI_MOSI = 1
LCD_DC = 3
LCD_BL = 6
I2C_SDA = 8
I2C_SCL = 7

def test_different_spi_speeds():
    """Test different SPI speeds to see if voltage/power is the issue"""
    print("\n=== TESTING DIFFERENT SPI SPEEDS ===")
    
    speeds = [1000000, 5000000, 10000000, 20000000, 40000000, 80000000]
    
    for speed in speeds:
        print(f"\n--- Testing SPI at {speed/1000000:.1f}MHz ---")
        
        try:
            # Initialize SPI at this speed
            spi = SPI(2, baudrate=speed, polarity=0, phase=0,
                      sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
            
            # Initialize DC pin
            dc = Pin(LCD_DC, Pin.OUT)
            
            # Try to send a simple command
            dc.off()
            spi.write(bytearray([0x00]))  # NOP
            print(f"   NOP command sent successfully at {speed/1000000:.1f}MHz")
            
            # Try to send sleep out
            dc.off()
            spi.write(bytearray([0x11]))  # Sleep out
            print(f"   Sleep out sent successfully at {speed/1000000:.1f}MHz")
            
            time.sleep_ms(100)
            
        except Exception as e:
            print(f"   Error at {speed/1000000:.1f}MHz: {e}")
            break

def test_different_spi_modes():
    """Test different SPI modes"""
    print("\n=== TESTING DIFFERENT SPI MODES ===")
    
    modes = [
        ("Mode 0", 0, 0),
        ("Mode 1", 0, 1),
        ("Mode 2", 1, 0),
        ("Mode 3", 1, 1)
    ]
    
    for mode_name, polarity, phase in modes:
        print(f"\n--- Testing {mode_name} ---")
        
        try:
            spi = SPI(2, baudrate=10000000, polarity=polarity, phase=phase,
                      sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
            
            dc = Pin(LCD_DC, Pin.OUT)
            
            # Send NOP
            dc.off()
            spi.write(bytearray([0x00]))
            print(f"   NOP sent successfully")
            
            # Send sleep out
            dc.off()
            spi.write(bytearray([0x11]))
            print(f"   Sleep out sent successfully")
            
            time.sleep_ms(100)
            
        except Exception as e:
            print(f"   Error in {mode_name}: {e}")

def test_minimal_display():
    """Test with absolute minimal display commands"""
    print("\n=== MINIMAL DISPLAY TEST ===")
    
    try:
        # Use very low SPI speed first
        print("1. Initializing SPI at 1MHz...")
        spi = SPI(2, baudrate=1000000, polarity=0, phase=0,
                  sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
        
        # Initialize pins
        print("2. Initializing pins...")
        dc = Pin(LCD_DC, Pin.OUT)
        backlight = Pin(LCD_BL, Pin.OUT)
        backlight.on()
        
        # Send minimal commands
        print("3. Sending minimal commands...")
        
        # Just try to wake up the display
        dc.off()
        spi.write(bytearray([0x11]))  # Sleep out
        time.sleep_ms(120)
        print("   Sleep out sent")
        
        # Turn display on
        dc.off()
        spi.write(bytearray([0x29]))  # Display on
        print("   Display on sent")
        
        # Try to set a tiny area (5x5 pixels)
        print("4. Testing tiny area...")
        
        dc.off()
        spi.write(bytearray([0x2A]))  # Column address
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x04]))
        
        dc.off()
        spi.write(bytearray([0x2B]))  # Row address
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x04]))
        
        dc.off()
        spi.write(bytearray([0x2C]))  # Memory write
        
        # Send just 25 pixels of white
        dc.on()
        white_pixels = bytearray()
        for _ in range(25):  # 5x5 pixels
            white_pixels.extend(bytearray([0xFF, 0xFF]))  # White in BGR565
        
        spi.write(white_pixels)
        print("   25 white pixels sent - look for tiny white square")
        
        return True
        
    except Exception as e:
        print(f"   Minimal display test error: {e}")
        return False

def test_voltage_check():
    """Check if voltage levels might be the issue"""
    print("\n=== VOLTAGE CHECK ===")
    
    print("1. Backlight test...")
    try:
        backlight = Pin(LCD_BL, Pin.OUT)
        backlight.on()
        print("   Backlight turned ON")
        time.sleep_ms(1000)
        
        backlight.off()
        print("   Backlight turned OFF")
        time.sleep_ms(1000)
        
        backlight.on()
        print("   Backlight turned ON again")
        
    except Exception as e:
        print(f"   Backlight error: {e}")
    
    print("\n2. DC pin test...")
    try:
        dc = Pin(LCD_DC, Pin.OUT)
        dc.on()
        print("   DC pin set HIGH")
        time.sleep_ms(100)
        
        dc.off()
        print("   DC pin set LOW")
        time.sleep_ms(100)
        
        dc.on()
        print("   DC pin set HIGH again")
        
    except Exception as e:
        print(f"   DC pin error: {e}")

try:
    print("Starting voltage and power tests...")
    
    # Test 1: Voltage check
    test_voltage_check()
    
    # Test 2: Different SPI speeds
    test_different_spi_speeds()
    
    # Test 3: Different SPI modes
    test_different_spi_modes()
    
    # Test 4: Minimal display test
    test_minimal_display()
    
    print("\n=== VOLTAGE TEST COMPLETE ===")
    print("Check if any of the tests showed different behavior.")
    print("If SPI works at lower speeds but not higher, it's a voltage/power issue.")
    print("If minimal display test works, the issue is in the initialization sequence.")

except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Voltage test completed")


