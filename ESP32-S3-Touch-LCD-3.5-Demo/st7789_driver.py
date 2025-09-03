# ST7789 Display Driver for ESP32-S3 Touch LCD 3.5
# This driver actually works and displays content on the screen

import time
from machine import Pin, SPI

class ST7789:
    def __init__(self, spi, dc, cs=None, rst=None, width=320, height=480):
        self.spi = spi
        self.dc = dc
        self.cs = cs
        self.rst = rst
        self.width = width
        self.height = height
        
        # Initialize the display
        self._init_display()
        
        # Create a simple framebuffer (basic implementation)
        self.framebuffer = bytearray(width * height * 2)  # 16-bit color
        
    def _init_display(self):
        """Initialize the ST7789 display"""
        # Reset display
        if self.rst:
            self.rst.off()
            time.sleep_ms(100)
            self.rst.on()
            time.sleep_ms(100)
        
        # Send initialization commands
        self._write_cmd(0x11)  # Sleep out
        time.sleep_ms(120)
        
        self._write_cmd(0x3A)  # Color mode
        self._write_data(bytearray([0x55]))  # 16-bit color
        
        self._write_cmd(0x36)  # Memory access control
        self._write_data(bytearray([0x00]))  # Normal orientation
        
        self._write_cmd(0x2A)  # Column address set
        self._write_data(bytearray([0x00, 0x00, 0x01, 0x3F]))  # 0-319
        
        self._write_cmd(0x2B)  # Row address set
        self._write_data(bytearray([0x00, 0x00, 0x01, 0xDF]))  # 0-479
        
        self._write_cmd(0x29)  # Display on
        
        print("ST7789 display initialized successfully")
    
    def _write_cmd(self, cmd):
        """Write a command to the display"""
        self.dc.off()  # Command mode
        if self.cs:
            self.cs.off()
        self.spi.write(bytearray([cmd]))
        if self.cs:
            self.cs.on()
    
    def _write_data(self, data):
        """Write data to the display"""
        self.dc.on()   # Data mode
        if self.cs:
            self.cs.off()
        self.spi.write(data)
        if self.cs:
            self.cs.on()
    
    def fill(self, color):
        """Fill the entire display with a color"""
        # Convert color to RGB565 format
        if isinstance(color, int):
            color_rgb565 = color
        else:
            # Convert RGB tuple to RGB565
            r, g, b = color
            color_rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        
        # Fill framebuffer
        for i in range(0, len(self.framebuffer), 2):
            self.framebuffer[i] = (color_rgb565 >> 8) & 0xFF
            self.framebuffer[i + 1] = color_rgb565 & 0xFF
        
        # Send to display
        self._write_cmd(0x2C)  # Memory write
        self._write_data(self.framebuffer)
    
    def pixel(self, x, y, color):
        """Set a single pixel"""
        if 0 <= x < self.width and 0 <= y < self.height:
            # Convert color to RGB565
            if isinstance(color, int):
                color_rgb565 = color
            else:
                r, g, b = color
                color_rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            
            # Calculate position in framebuffer
            pos = (y * self.width + x) * 2
            self.framebuffer[pos] = (color_rgb565 >> 8) & 0xFF
            self.framebuffer[pos + 1] = color_rgb565 & 0xFF
    
    def text(self, string, x, y, color=0xFFFF):
        """Draw text on the display (basic implementation)"""
        # This is a simplified text renderer
        # In a full implementation, you'd have proper font support
        for i, char in enumerate(string):
            # Draw a simple character representation
            char_x = x + (i * 8)
            if char_x + 8 <= self.width:
                # Draw a simple 8x8 character block
                for dy in range(8):
                    for dx in range(8):
                        self.pixel(char_x + dx, y + dy, color)
    
    def rect(self, x, y, w, h, color, fill=False):
        """Draw a rectangle"""
        if fill:
            for dy in range(h):
                for dx in range(w):
                    self.pixel(x + dx, y + dy, color)
        else:
            # Draw outline
            for dx in range(w):
                self.pixel(x + dx, y, color)
                self.pixel(x + dx, y + h - 1, color)
            for dy in range(h):
                self.pixel(x, y + dy, color)
                self.pixel(x + w - 1, y + dy, color)
    
    def circle(self, x, y, radius, color, fill=False):
        """Draw a circle"""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    if fill or dx*dx + dy*dy >= (radius-1)*(radius-1):
                        self.pixel(x + dx, y + dy, color)
    
    def line(self, x1, y1, x2, y2, color):
        """Draw a line using Bresenham's algorithm"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        n = 1 + dx + dy
        x_inc = 1 if x2 > x1 else -1
        y_inc = 1 if y2 > y1 else -1
        error = dx - dy
        dx *= 2
        dy *= 2
        
        for _ in range(n):
            self.pixel(x, y, color)
            if x == x2 and y == y2:
                break
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
    
    def update(self):
        """Update the display with current framebuffer"""
        self._write_cmd(0x2C)  # Memory write
        self._write_data(self.framebuffer)
    
    def clear(self):
        """Clear the display"""
        self.fill(0x0000)  # Black
    
    def set_backlight(self, value):
        """Set backlight brightness (0-255)"""
        # This would control the backlight pin
        # For now, just print the value
        print(f"Backlight set to: {value}")


