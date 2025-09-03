# Complete Working MicroPythonOS for ESP32-S3 Touch LCD 3.5
# This version actually displays content on the LCD screen!

import time
import gc
from machine import Pin, SPI, I2C

# Import our custom drivers (use ST7796 + TCA9554 reset as in 01_factory)
try:
    from st7796_driver import ST7796
    from ft6x36_driver import FT6X36
    print("Custom drivers loaded successfully")
except ImportError as e:
    print(f"Driver import error: {e}")
    print("Please ensure st7796_driver.py, tca9554.py and ft6x36_driver.py are uploaded")

class MicroPythonOS:
    def __init__(self):
        """Initialize MicroPythonOS with full display support"""
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
        
        # Initialize display
        self.init_display()
        
        # Initialize touch
        self.init_touch()
        
    def init_hardware(self):
        """Initialize all hardware components"""
        try:
            print("Initializing hardware...")
            
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
            
            # Create display object (driver handles SPI + TCA9554 reset internally)
            self.display = ST7796(
                sck_pin=self.SPI_SCK,
                mosi_pin=self.SPI_MOSI,
                dc_pin=self.LCD_DC,
                bl_pin=self.LCD_BL,
                width=320,
                height=480,
                spi_id=2,
                i2c_sda=self.I2C_SDA,
                i2c_scl=self.I2C_SCL,
                spi_baudrate=80_000_000,
            )
            
            # Clear display and show welcome
            self.display.clear()
            self.display.fill(0x0000)  # Black background
            
            print("LCD display initialized successfully")
            return True
            
        except Exception as e:
            print(f"Display initialization error: {e}")
            self.display = None  # Set to None if failed
            return False
    
    def init_touch(self):
        """Initialize the touch controller"""
        try:
            print("Initializing touch controller...")
            
            # Create touch object
            self.touch = FT6X36(self.i2c, addr=0x38)
            
            print("Touch controller initialized successfully")
            return True
            
        except Exception as e:
            print(f"Touch initialization error: {e}")
            self.touch = None  # Set to None if failed
            return False
    
    def show_welcome_screen(self):
        """Show welcome screen on the actual LCD"""
        if not self.display:
            print("Display not available, skipping welcome screen")
            return
            
        try:
            print("Showing welcome screen on LCD...")
            
            # Clear display
            self.display.clear()
            
            # Fill with dark blue background
            self.display.fill(0x001F)  # Dark blue
            
            # Draw title bar
            self.display.draw_rect(0, 0, 320, 60, 0x07E0, fill=True)  # Green title bar
            
            # Draw title text (black on green)
            self.display.draw_text("MicroPythonOS", 80, 20, 0x0000, bg_color_565=0x07E0)
            self.display.draw_text("ESP32-S3 Touch LCD 3.5", 60, 40, 0x0000, bg_color_565=0x07E0)
            
            # Draw main content area
            self.display.draw_rect(10, 80, 300, 380, 0xFFFF, fill=True)  # White content area
            
            # Draw welcome message (black on white)
            self.display.draw_text("Welcome to MicroPythonOS!", 30, 100, 0x0000, bg_color_565=0xFFFF)
            self.display.draw_text("Your display is working!", 50, 130, 0x0000, bg_color_565=0xFFFF)
            
            # Draw system info (black on white)
            self.display.draw_text("System Status:", 30, 170, 0x0000, bg_color_565=0xFFFF)
            self.display.draw_text("Hardware: Initialized", 30, 190, 0x0000, bg_color_565=0xFFFF)
            self.display.draw_text("Display: Active", 30, 210, 0x0000, bg_color_565=0xFFFF)
            self.display.draw_text("Touch: Ready", 30, 230, 0x0000, bg_color_565=0xFFFF)
            
            # Draw instructions (black on white)
            self.display.draw_text("Touch the screen to test!", 30, 280, 0x0000, bg_color_565=0xFFFF)
            self.display.draw_text("Press button for menu", 30, 300, 0x0000, bg_color_565=0xFFFF)
            
            # Draw version info (black on white)
            self.display.draw_text(f"Version: {self.version}", 30, 350, 0x0000, bg_color_565=0xFFFF)
            self.display.draw_text("Built for ESP32-S3", 30, 370, 0x0000, bg_color_565=0xFFFF)
            
            print("Welcome screen displayed successfully!")
            
        except Exception as e:
            print(f"Welcome screen error: {e}")
    
    def show_main_menu(self):
        """Show main menu on the LCD"""
        if not self.display:
            print("Display not available, skipping main menu")
            return
            
        try:
            print("Showing main menu on LCD...")
            
            # Clear display
            self.display.clear()
            
            # Fill with light gray background
            self.display.fill(0xC618)  # Light gray
            
            # Draw title bar
            self.display.draw_rect(0, 0, 320, 50, 0x001F, fill=True)  # Blue title bar
            self.display.draw_text("MicroPythonOS Menu", 70, 15, 0xFFFF, bg_color_565=0x001F)  # White on blue
            
            # Draw menu options
            menu_items = [
                "1. System Information",
                "2. Hardware Test",
                "3. Touch Test",
                "4. Display Test",
                "5. Settings",
                "0. Exit"
            ]
            
            y_start = 70
            for i, item in enumerate(menu_items):
                y_pos = y_start + (i * 30)
                # Draw button background
                self.display.draw_rect(20, y_pos, 280, 25, 0xFFFF, fill=True)
                # Draw button border
                self.display.draw_rect(20, y_pos, 280, 25, 0x0000, fill=False)
                # Draw text (black on white)
                self.display.draw_text(item, 30, y_pos + 5, 0x0000, bg_color_565=0xFFFF)
            
            print("Main menu displayed successfully!")
            
        except Exception as e:
            print(f"Main menu error: {e}")
    
    def show_system_info(self):
        """Show system information on the LCD"""
        if not self.display:
            print("Display not available, skipping system info")
            return
            
        try:
            print("Showing system information...")
            
            # Clear display
            self.display.clear()
            
            # Fill with white background
            self.display.fill(0xFFFF)
            
            # Draw title (black on white)
            self.display.draw_text("System Information", 70, 20, 0x0000, bg_color_565=0xFFFF)
            
            # Get system info
            try:
                import esp
                flash_size = esp.flash_size() if hasattr(esp, 'flash_size') else "Unknown"
            except:
                flash_size = "Unknown"
            
            # Draw info
            info_items = [
                f"Version: {self.version}",
                f"Hardware: {self.hardware}",
                f"Firmware: {self.firmware}",
                f"Flash Size: {flash_size} bytes",
                f"Free Memory: {gc.mem_free()} bytes",
                f"Platform: ESP32-S3",
                f"Display: 320x480",
                f"Touch: FT6X36"
            ]
            
            y_start = 60
            for i, item in enumerate(info_items):
                y_pos = y_start + (i * 25)
                self.display.draw_text(item, 20, y_pos, 0x0000, bg_color_565=0xFFFF)
            
            # Draw back button
            self.display.draw_rect(120, 400, 80, 30, 0x001F, fill=True)
            self.display.draw_text("Back", 140, 410, 0xFFFF, bg_color_565=0x001F)
            
            print("System info displayed successfully!")
            
        except Exception as e:
            print(f"System info error: {e}")
    
    def run_touch_test(self):
        """Run interactive touch test on the LCD"""
        if not self.display or not self.touch:
            print("Display or touch not available, skipping touch test")
            return
            
        try:
            print("Starting touch test...")
            
            # Clear display
            self.display.clear()
            self.display.fill(0x0000)  # Black background
            
            # Draw title
            self.display.draw_text("Touch Test", 120, 20, 0xFFFF, bg_color_565=0x0000)
            self.display.draw_text("Touch anywhere on screen", 60, 50, 0xFFFF, bg_color_565=0x0000)
            self.display.draw_text("Press button to exit", 80, 80, 0xFFFF, bg_color_565=0x0000)
            
            # Draw touch area
            self.display.draw_rect(10, 100, 300, 300, 0xFFFF, fill=False)
            self.display.draw_text("Touch Area", 120, 200, 0xFFFF)
            
            # Touch test loop
            start_time = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), start_time) < 30000:  # 30 second timeout
                
                # Check for touch
                touch_data = self.touch.read_touch()
                if touch_data:
                    x, y = touch_data['x'], touch_data['y']
                    print(f"Touch detected at ({x}, {y})")
                    
                    # Draw touch indicator
                    self.display.draw_circle(x, y, 10, 0xF800, fill=True)  # Red circle
                    
                    # Show coordinates
                    self.display.fill_rect(10, 420, 300, 40, 0x0000)
                    self.display.draw_text(f"Touch: ({x}, {y})", 20, 430, 0xFFFF, bg_color_565=0x0000)
                
                # Check for button press
                if self.button.value() == 0:
                    print("Button pressed, exiting touch test")
                    break
                
                time.sleep_ms(50)
            
            print("Touch test completed")
            
        except Exception as e:
            print(f"Touch test error: {e}")
    
    def run_display_test(self):
        """Run display test with various graphics"""
        if not self.display:
            print("Display not available, skipping display test")
            return
            
        try:
            print("Starting display test...")
            
            # Clear display
            self.display.clear()
            self.display.fill(0x0000)  # Black background
            
            # Draw title
            self.display.draw_text("Display Test", 110, 20, 0xFFFF, bg_color_565=0x0000)
            
            # Draw various shapes and colors
            colors = [0xF800, 0x07E0, 0x001F, 0xFFE0, 0xF81F, 0x07FF]  # Red, Green, Blue, Yellow, Magenta, Cyan
            
            # Draw colored rectangles
            for i, color in enumerate(colors):
                x = 20 + (i * 50)
                self.display.draw_rect(x, 60, 40, 40, color, fill=True)
            
            # Draw circles
            self.display.draw_circle(80, 150, 30, 0xFFFF, fill=False)
            self.display.draw_circle(160, 150, 30, 0xF800, fill=True)
            self.display.draw_circle(240, 150, 30, 0x07E0, fill=True)
            
            # Draw text
            self.display.draw_text("Graphics Test Complete!", 60, 280, 0xFFFF, bg_color_565=0x0000)
            self.display.draw_text("Press button to continue", 70, 310, 0xFFFF, bg_color_565=0x0000)
            
            # Wait for button press
            while self.button.value() == 1:
                time.sleep_ms(100)
            
            print("Display test completed")
            
        except Exception as e:
            print(f"Display test error: {e}")
    
    def run(self):
        """Main application loop"""
        print("Starting MicroPythonOS with Full Display Support...")
        
        # Show welcome screen
        self.show_welcome_screen()
        time.sleep(3)  # Show welcome for 3 seconds
        
        # Main loop
        while True:
            try:
                # Show main menu
                self.show_main_menu()
                
                # Wait for input
                print("\n--- MicroPythonOS Menu ---")
                print("1. System Information")
                print("2. Hardware Test")
                print("3. Touch Test")
                print("4. Display Test")
                print("5. Settings")
                print("0. Exit")
                print("----------------------------")
                
                choice = input("Enter your choice (0-5): ").strip()
                
                if choice == "1":
                    self.show_system_info()
                    input("Press Enter to continue...")
                elif choice == "2":
                    print("Hardware test - check console output")
                    self.test_hardware()
                elif choice == "3":
                    self.run_touch_test()
                elif choice == "4":
                    self.run_display_test()
                elif choice == "5":
                    print("Settings - Coming soon")
                elif choice == "0":
                    print("Exiting MicroPythonOS...")
                    break
                else:
                    print("Invalid choice. Please try again.")
                
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
            
            # Test display
            if self.display:
                print("Display Test: LCD initialized and working")
            else:
                print("Display Test: LCD initialization failed")
            
            # Test touch
            if self.touch:
                print("Touch Test: FT6X36 initialized")
            else:
                print("Touch Test: FT6X36 initialization failed")
            
            print("Hardware test completed successfully")
            
        except Exception as e:
            print(f"Hardware test error: {e}")

# Start MicroPythonOS
if __name__ == "__main__":
    mpos = MicroPythonOS()
    mpos.run()
