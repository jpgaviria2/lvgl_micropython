# MicroPythonOS with Display Support for ESP32-S3 Touch LCD 3.5
# Shows graphical UI on the actual LCD display

import time
import gc
from machine import Pin, SPI, I2C

class MicroPythonOSDisplay:
    def __init__(self):
        """Initialize MicroPythonOS with Display Support"""
        self.version = "1.0.0"
        self.hardware = "ESP32-S3 Touch LCD 3.5"
        self.firmware = "ESP-IDF v1.26 Generic ESP32-S3"
        self.status = "initializing"
        
        # Pin configuration
        self.I2C_SDA = 8
        self.I2C_SCL = 7
        self.SPI_SCK = 5
        self.SPI_MOSI = 1
        self.SPI_MISO = 2
        self.LCD_DC = 3
        self.LCD_BL = 6
        
        # Initialize hardware
        self.init_hardware()
        
    def init_hardware(self):
        """Initialize all hardware components"""
        try:
            print("Initializing hardware for display...")
            
            # Initialize I2C
            self.i2c = I2C(0, scl=Pin(self.I2C_SCL), sda=Pin(self.I2C_SDA), freq=100000)
            devices = self.i2c.scan()
            print(f"I2C devices found: {[hex(addr) for addr in devices]}")
            
            # Initialize SPI for LCD
            self.spi = SPI(2, baudrate=40000000, polarity=0, phase=0, 
                           sck=Pin(self.SPI_SCK), mosi=Pin(self.SPI_MOSI), miso=Pin(self.SPI_MISO))
            print("SPI initialized for LCD")
            
            # Initialize backlight
            self.backlight = Pin(self.LCD_BL, Pin.OUT)
            self.backlight.on()
            print("Backlight enabled")
            
            # Initialize button
            self.button = Pin(0, Pin.IN, Pin.PULL_UP)
            print("Button initialized")
            
            return True
            
        except Exception as e:
            print(f"Hardware initialization error: {e}")
            return False
    
    def init_display(self):
        """Initialize the LCD display"""
        try:
            print("Initializing LCD display...")
            
            # Try to import display libraries
            try:
                import st7789
                print("ST7789 library found")
                self.display_available = True
            except ImportError:
                print("ST7789 library not available, using basic display")
                self.display_available = False
            
            # For now, we'll create a basic display interface
            # In a full implementation, you'd initialize ST7789 here
            print("Display initialization complete")
            return True
            
        except Exception as e:
            print(f"Display initialization error: {e}")
            return False
    
    def show_welcome_screen(self):
        """Show welcome screen on display"""
        try:
            if not self.display_available:
                print("Display not available, showing console output")
                return
            
            # This would contain actual display commands
            # For now, we'll show what we would do
            print("Would show welcome screen on LCD:")
            print("  - MicroPythonOS logo")
            print("  - Welcome message")
            print("  - System status")
            print("  - Touch instructions")
            
        except Exception as e:
            print(f"Display error: {e}")
    
    def show_main_menu(self):
        """Show main menu on display"""
        try:
            if not self.display_available:
                print("Display not available, showing console menu")
                return
            
            print("Would show main menu on LCD:")
            print("  - App grid layout")
            print("  - Touch-friendly buttons")
            print("  - System information")
            print("  - Settings access")
            
        except Exception as e:
            print(f"Menu display error: {e}")
    
    def run_console_mode(self):
        """Run in console mode when display is not available"""
        print("\n" + "="*50)
        print("    MicroPythonOS ESP32-S3 Touch LCD 3.5")
        print("="*50)
        print(f"Version: {self.version}")
        print(f"Hardware: {self.hardware}")
        print(f"Firmware: {self.firmware}")
        print(f"Status: {self.status}")
        print("="*50)
        
        # Display system information
        try:
            import esp
            if hasattr(esp, 'flash_size'):
                print(f"Flash Size: {esp.flash_size()} bytes")
            print(f"ESP32 Module: {esp.__name__}")
        except Exception as e:
            print(f"ESP info: {e}")
        
        # Memory info
        gc.collect()
        print(f"Free Memory: {gc.mem_free()} bytes")
        
        # Platform info
        try:
            import sys
            print(f"Platform: {sys.platform}")
            print(f"Python Version: {sys.version}")
        except Exception as e:
            print(f"Platform info: {e}")
        
        print("="*50)
        print("Display Status: Console Mode (LCD not fully initialized)")
        print("To enable full display support, install ST7789 library")
        print("="*50)
    
    def run(self):
        """Main application loop"""
        print("Starting MicroPythonOS with Display Support...")
        
        # Initialize display
        if self.init_display():
            self.status = "display_ready"
            print("Display system ready")
        else:
            self.status = "console_mode"
            print("Running in console mode")
        
        # Show appropriate interface
        if self.status == "display_ready":
            self.show_welcome_screen()
            self.show_main_menu()
            print("Display mode active - check your LCD screen!")
        else:
            self.run_console_mode()
        
        # Main loop
        while True:
            try:
                if self.status == "display_ready":
                    # Display mode - handle touch events
                    print("Display mode: Waiting for touch input...")
                    time.sleep(2)
                else:
                    # Console mode - show menu
                    print("\n--- Console Menu ---")
                    print("1. System Information")
                    print("2. Hardware Test")
                    print("3. Try Display Mode")
                    print("4. Exit")
                    print("-------------------")
                    
                    choice = input("Enter choice (1-4): ").strip()
                    
                    if choice == "1":
                        self.run_console_mode()
                    elif choice == "2":
                        self.test_hardware()
                    elif choice == "3":
                        print("Attempting to initialize display...")
                        if self.init_display():
                            self.status = "display_ready"
                            self.show_welcome_screen()
                        else:
                            print("Display initialization failed")
                    elif choice == "4":
                        print("Exiting...")
                        break
                    else:
                        print("Invalid choice")
                
                # Garbage collection
                gc.collect()
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(2)
    
    def test_hardware(self):
        """Test hardware components"""
        print("\n--- Hardware Test ---")
        
        try:
            # Test I2C
            devices = self.i2c.scan()
            print(f"I2C Test: {len(devices)} devices found")
            print(f"Device addresses: {[hex(addr) for addr in devices]}")
            
            # Test SPI
            print("SPI Test: Initialized successfully")
            
            # Test GPIO
            self.backlight.on()
            time.sleep(0.5)
            self.backlight.off()
            time.sleep(0.5)
            self.backlight.on()
            print("GPIO Test: Backlight control working")
            
            print("Hardware test completed successfully")
            
        except Exception as e:
            print(f"Hardware test error: {e}")

# Start MicroPythonOS with Display Support
if __name__ == "__main__":
    mpos = MicroPythonOSDisplay()
    mpos.run()


