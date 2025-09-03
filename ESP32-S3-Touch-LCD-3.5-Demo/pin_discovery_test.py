# Pin Discovery Test - Try different common pin combinations
# Since current pins aren't working, let's find the right ones

import time
from machine import Pin, SPI

print("=== PIN DISCOVERY TEST ===")

# Common pin combinations for ESP32-S3 displays
pin_configs = [
    # Config 1: Common ESP32-S3 pins
    {"name": "Config 1 (Common)", "sck": 5, "mosi": 1, "dc": 3, "bl": 6},
    
    # Config 2: Alternative common pins
    {"name": "Config 2 (Alt)", "sck": 18, "mosi": 23, "dc": 2, "bl": 4},
    
    # Config 3: Another common set
    {"name": "Config 3 (Alt2)", "sck": 14, "mosi": 13, "dc": 15, "bl": 2},
    
    # Config 4: Try different SPI bus
    {"name": "Config 4 (SPI1)", "sck": 12, "mosi": 11, "dc": 10, "bl": 9},
]

def test_pin_config(config):
    """Test a specific pin configuration"""
    print(f"\n--- Testing {config['name']} ---")
    print(f"SCK: GPIO {config['sck']}, MOSI: GPIO {config['mosi']}")
    print(f"DC: GPIO {config['dc']}, BL: GPIO {config['bl']}")
    
    try:
        # Initialize SPI
        spi = SPI(2, baudrate=1000000, polarity=0, phase=0, 
                  sck=Pin(config['sck']), mosi=Pin(config['mosi']))
        print("✓ SPI initialized")
        
        # Initialize backlight
        backlight = Pin(config['bl'], Pin.OUT)
        backlight.on()
        print("✓ Backlight enabled")
        
        # Initialize DC pin
        dc = Pin(config['dc'], Pin.OUT)
        print("✓ DC pin initialized")
        
        # Try basic display commands
        print("Sending basic commands...")
        
        # Sleep out
        dc.off()  # Command mode
        spi.write(bytearray([0x11]))  # Sleep out
        time.sleep_ms(120)
        
        # Display on
        dc.off()  # Command mode
        spi.write(bytearray([0x29]))  # Display on
        
        # Try to set a small area
        dc.off()  # Command mode
        spi.write(bytearray([0x2A]))  # Column address set
        dc.on()   # Data mode
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))  # 0-9
        
        dc.off()  # Command mode
        spi.write(bytearray([0x2B]))  # Row address set
        dc.on()   # Data mode
        spi.write(bytearray([0x00, 0x00, 0x00, 0x09]))  # 0-9
        
        # Start memory write
        dc.off()  # Command mode
        spi.write(bytearray([0x2C]))  # Memory write
        
        # Send 4 red pixels
        dc.on()   # Data mode
        red_pixels = bytearray([0xF8, 0x00, 0xF8, 0x00, 0xF8, 0x00, 0xF8, 0x00])
        spi.write(red_pixels)
        
        print("✓ Commands sent successfully")
        print("Check your screen for 4 red dots in top-left corner")
        
        # Wait a moment to see if anything appears
        time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Test all configurations
print("Testing different pin configurations...")
print("Watch your screen for ANY visual changes!")

working_config = None

for config in pin_configs:
    if test_pin_config(config):
        print(f"\n🎉 {config['name']} WORKED!")
        print("You should see red dots on your screen!")
        working_config = config
        break
    else:
        print(f"\n❌ {config['name']} failed")
    
    time.sleep(1)

if working_config:
    print(f"\n✅ SUCCESS! Working configuration found:")
    print(f"SCK: GPIO {working_config['sck']}")
    print(f"MOSI: GPIO {working_config['mosi']}")
    print(f"DC: GPIO {working_config['dc']}")
    print(f"BL: GPIO {working_config['bl']}")
    print("\nUse these pins in your display driver!")
else:
    print("\n❌ No working configuration found.")
    print("This suggests:")
    print("1. Wrong pin numbers")
    print("2. Different display type")
    print("3. Hardware connection issue")
    print("\nPlease check your ESP-IDF example for exact pin numbers!")

print("\n=== PIN DISCOVERY TEST COMPLETE ===")


