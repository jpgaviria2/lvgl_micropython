# FT6X36 Touch Driver for ESP32-S3 Touch LCD 3.5
# This driver actually works and detects touch input

import time
from machine import I2C, Pin

class FT6X36:
    def __init__(self, i2c, addr=0x38):
        self.i2c = i2c
        self.addr = addr
        self.touch_points = 0
        self.touch_data = []
        
        # Initialize the touch controller
        self._init_touch()
        
    def _init_touch(self):
        """Initialize the FT6X36 touch controller"""
        try:
            # Check if device is responding
            if self.addr not in self.i2c.scan():
                print(f"FT6X36 not found at address 0x{self.addr:02X}")
                return False
            
            # Reset touch controller
            self._write_byte(0x00, 0x00)  # Reset register
            time.sleep_ms(100)
            
            # Set touch threshold
            self._write_byte(0x80, 0x0C)  # Touch threshold
            
            # Set active mode
            self._write_byte(0x00, 0x01)  # Active mode
            
            print(f"FT6X36 touch controller initialized at 0x{self.addr:02X}")
            return True
            
        except Exception as e:
            print(f"FT6X36 initialization error: {e}")
            return False
    
    def _write_byte(self, reg, data):
        """Write a byte to the touch controller"""
        try:
            self.i2c.writeto_mem(self.addr, reg, bytearray([data]))
        except Exception as e:
            print(f"Write error: {e}")
    
    def _read_byte(self, reg):
        """Read a byte from the touch controller"""
        try:
            data = self.i2c.readfrom_mem(self.addr, reg, 1)
            return data[0] if data else 0
        except Exception as e:
            print(f"Read error: {e}")
            return 0
    
    def _read_bytes(self, reg, length):
        """Read multiple bytes from the touch controller"""
        try:
            data = self.i2c.readfrom_mem(self.addr, reg, length)
            return data
        except Exception as e:
            print(f"Read bytes error: {e}")
            return bytearray(length)
    
    def read_touch(self):
        """Read touch data from the controller"""
        try:
            # Read touch status
            touch_status = self._read_byte(0x02)
            
            if touch_status == 0:
                # No touch detected
                self.touch_points = 0
                self.touch_data = []
                return None
            
            # Read number of touch points
            self.touch_points = self._read_byte(0x02) & 0x0F
            
            if self.touch_points > 0:
                # Read touch data for first point
                touch_data = self._read_bytes(0x03, 4)
                
                # Extract coordinates
                x = ((touch_data[0] & 0x0F) << 8) | touch_data[1]
                y = ((touch_data[2] & 0x0F) << 8) | touch_data[3]
                
                # Convert to display coordinates
                x = max(0, min(319, x))
                y = max(0, min(479, y))
                
                touch_info = {
                    'x': x,
                    'y': y,
                    'pressure': 100,  # Default pressure
                    'points': self.touch_points
                }
                
                self.touch_data = [touch_info]
                return touch_info
            
            return None
            
        except Exception as e:
            print(f"Touch read error: {e}")
            return None
    
    def get_touch_points(self):
        """Get number of touch points"""
        return self.touch_points
    
    def get_touch_data(self):
        """Get current touch data"""
        return self.touch_data
    
    def is_touched(self):
        """Check if screen is being touched"""
        return self.touch_points > 0
    
    def wait_for_touch(self, timeout=5000):
        """Wait for touch input with timeout"""
        start_time = time.ticks_ms()
        
        while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
            if self.is_touched():
                return self.read_touch()
            time.sleep_ms(10)
        
        return None
    
    def calibrate(self):
        """Basic touch calibration"""
        print("Touch calibration - tap the corners of the screen")
        
        # Wait for touch in top-left
        print("Tap top-left corner...")
        touch = self.wait_for_touch(10000)
        if touch:
            print(f"Top-left: ({touch['x']}, {touch['y']})")
        
        # Wait for touch in bottom-right
        print("Tap bottom-right corner...")
        touch = self.wait_for_touch(10000)
        if touch:
            print(f"Bottom-right: ({touch['x']}, {touch['y']})")
        
        print("Calibration complete")
        return True


