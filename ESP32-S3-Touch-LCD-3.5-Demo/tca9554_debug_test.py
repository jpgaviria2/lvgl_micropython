# TCA9554 Debug Test - Test Hardware Reset Step by Step
# This will help us understand if the hardware reset is working

import time
from machine import Pin, I2C

print("=== TCA9554 HARDWARE RESET DEBUG TEST ===")

# Pin configuration
I2C_SDA = 8
I2C_SCL = 7

# TCA9554 I2C address
TCA9554_ADDR = 0x20

def test_tca9554_basic():
    """Test basic TCA9554 communication"""
    print("\n=== BASIC TCA9554 TEST ===")
    
    try:
        # Initialize I2C
        print("1. Initializing I2C...")
        i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)
        print("   I2C initialized successfully")
        
        # Scan for devices
        print("2. Scanning I2C bus...")
        devices = i2c.scan()
        print(f"   I2C devices found: {[hex(addr) for addr in devices]}")
        
        if TCA9554_ADDR not in devices:
            print(f"   ERROR: TCA9554 not found at {hex(TCA9554_ADDR)}")
            return False
        
        print(f"   TCA9554 found at {hex(TCA9554_ADDR)}")
        
        # Read current port configuration
        print("3. Reading current port configuration...")
        try:
            port0_dir = i2c.readfrom_mem(TCA9554_ADDR, 0x06, 1)  # Port 0 direction
            port1_dir = i2c.readfrom_mem(TCA9554_ADDR, 0x07, 1)  # Port 1 direction
            port0_out = i2c.readfrom_mem(TCA9554_ADDR, 0x02, 1)  # Port 0 output
            port1_out = i2c.readfrom_mem(TCA9554_ADDR, 0x03, 1)  # Port 1 output
            
            print(f"   Port 0 direction: {hex(port0_dir[0])}")
            print(f"   Port 1 direction: {hex(port1_out[0])}")
            print(f"   Port 0 output: {hex(port0_out[0])}")
            print(f"   Port 1 output: {hex(port1_out[0])}")
            
        except Exception as e:
            print(f"   Error reading ports: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   I2C error: {e}")
        return False

def test_tca9554_reset():
    """Test the hardware reset sequence"""
    print("\n=== HARDWARE RESET TEST ===")
    
    try:
        i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)
        
        # Step 1: Set pin 1 as output
        print("1. Setting TCA9554 pin 1 as output...")
        i2c.writeto_mem(TCA9554_ADDR, 0x07, bytearray([0xFE]))  # Port 1 direction (pin 1 = output)
        print("   Pin 1 set as output")
        
        # Step 2: Set pin 1 HIGH
        print("2. Setting pin 1 HIGH...")
        i2c.writeto_mem(TCA9554_ADDR, 0x03, bytearray([0x02]))  # Port 1 output (pin 1 = HIGH)
        print("   Pin 1 set HIGH")
        time.sleep_ms(100)
        
        # Step 3: Set pin 1 LOW (reset)
        print("3. Setting pin 1 LOW (reset)...")
        i2c.writeto_mem(TCA9554_ADDR, 0x03, bytearray([0x00]))  # Port 1 output (pin 1 = LOW)
        print("   Pin 1 set LOW (reset active)")
        time.sleep_ms(100)
        
        # Step 4: Set pin 1 HIGH
        print("4. Setting pin 1 HIGH...")
        i2c.writeto_mem(TCA9554_ADDR, 0x03, bytearray([0x02]))  # Port 1 output (pin 1 = HIGH)
        print("   Pin 1 set HIGH (reset complete)")
        time.sleep_ms(200)
        
        # Verify the reset
        print("5. Verifying reset...")
        port1_out = i2c.readfrom_mem(TCA9554_ADDR, 0x03, 1)
        print(f"   Port 1 output after reset: {hex(port1_out[0])}")
        
        print("   Hardware reset sequence completed!")
        return True
        
    except Exception as e:
        print(f"   Reset error: {e}")
        return False

def test_simple_display():
    """Test display with minimal commands after reset"""
    print("\n=== SIMPLE DISPLAY TEST ===")
    
    try:
        from machine import SPI
        
        # Initialize SPI
        print("1. Initializing SPI...")
        spi = SPI(2, baudrate=80000000, polarity=0, phase=0,
                  sck=Pin(5), mosi=Pin(1))
        
        # Initialize DC pin
        print("2. Initializing DC pin...")
        dc = Pin(3, Pin.OUT)
        
        # Initialize backlight
        print("3. Initializing backlight...")
        backlight = Pin(6, Pin.OUT)
        backlight.on()
        
        # Send basic commands
        print("4. Sending basic commands...")
        
        # Sleep out
        dc.off()
        spi.write(bytearray([0x11]))
        time.sleep_ms(120)
        print("   Sleep out sent")
        
        # Display on
        dc.off()
        spi.write(bytearray([0x29]))
        print("   Display on sent")
        
        # Try to set a small area and send red pixels
        print("5. Testing display output...")
        
        # Set small area (10x10 pixels)
        dc.off()
        spi.write(bytearray([0x2A]))  # Column address
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
        
        dc.off()
        spi.write(bytearray([0x2B]))  # Row address
        dc.on()
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))
        
        # Memory write
        dc.off()
        spi.write(bytearray([0x2C]))
        
        # Send red pixels (BGR565: 0x00F8)
        dc.on()
        red_pixels = bytearray()
        for _ in range(100):  # 10x10 pixels
            red_pixels.extend(bytearray([0x00, 0xF8]))
        
        spi.write(red_pixels)
        print("   100 red pixels sent - look for red square in top-left corner")
        
        return True
        
    except Exception as e:
        print(f"   Display test error: {e}")
        return False

try:
    print("Starting TCA9554 debug test...")
    
    # Test 1: Basic TCA9554 communication
    if not test_tca9554_basic():
        print("ERROR: Basic TCA9554 test failed!")
        print("Check I2C connections and TCA9554 power")
    else:
        print("✓ Basic TCA9554 test passed")
        
        # Test 2: Hardware reset
        if test_tca9554_reset():
            print("✓ Hardware reset test passed")
            
            # Test 3: Simple display test
            if test_simple_display():
                print("✓ Simple display test completed")
            else:
                print("✗ Simple display test failed")
        else:
            print("✗ Hardware reset test failed")
    
    print("\n=== DEBUG TEST COMPLETE ===")
    print("Check the console output above for any errors.")
    print("If TCA9554 is working, you should see successful hardware reset.")
    print("If display test works, you should see a red square.")

except Exception as e:
    print(f"ERROR: {e}")
    import sys
    sys.print_exception(e)

print("Debug test completed")


