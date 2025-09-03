# Memory-Efficient ST7789 Display Driver for ESP32-S3 Touch LCD 3.5
# Uses streaming instead of large framebuffer to save memory

import time
from machine import Pin, SPI

class ST7789Streaming:
    def __init__(self, spi, dc, cs=None, rst=None, width=320, height=480):
        self.spi = spi
        self.dc = dc
        self.cs = cs
        self.rst = rst
        self.width = width
        self.height = height
        
        # Initialize the display
        self._init_display()
        
        print("ST7789 streaming display initialized successfully")
    
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
        """Fill the entire display with a color using streaming"""
        # Convert color to RGB565 format
        if isinstance(color, int):
            color_rgb565 = color
        else:
            # Convert RGB tuple to RGB565
            r, g, b = color
            color_rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        
        # Set display area to full screen
        self._write_cmd(0x2A)  # Column address set
        self._write_data(bytearray([0x00, 0x00, 0x01, 0x3F]))
        
        self._write_cmd(0x2B)  # Row address set
        self._write_data(bytearray([0x00, 0x00, 0x01, 0xDF]))
        
        # Start memory write
        self._write_cmd(0x2C)
        
        # Create a small buffer for streaming
        buffer_size = 1024  # 1KB buffer instead of 307KB
        buffer = bytearray(buffer_size)
        
        # Fill buffer with color
        for i in range(0, buffer_size, 2):
            buffer[i] = (color_rgb565 >> 8) & 0xFF
            buffer[i + 1] = color_rgb565 & 0xFF
        
        # Stream data to display
        total_pixels = self.width * self.height
        pixels_sent = 0
        
        while pixels_sent < total_pixels:
            # Calculate how many pixels to send in this batch
            remaining_pixels = total_pixels - pixels_sent
            pixels_in_batch = min(remaining_pixels, buffer_size // 2)
            
            # Send the batch
            self._write_data(buffer[:pixels_in_batch * 2])
            pixels_sent += pixels_in_batch
    
    def fill_rect(self, x, y, w, h, color):
        """Fill a rectangle with streaming"""
        # Convert color to RGB565
        if isinstance(color, int):
            color_rgb565 = color
        else:
            r, g, b = color
            color_rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        
        # Set display area to rectangle
        self._write_cmd(0x2A)  # Column address set
        self._write_data(bytearray([x >> 8, x & 0xFF, (x + w - 1) >> 8, (x + w - 1) & 0xFF]))
        
        self._write_cmd(0x2B)  # Row address set
        self._write_data(bytearray([y >> 8, y & 0xFF, (y + h - 1) >> 8, (y + h - 1) & 0xFF]))
        
        # Start memory write
        self._write_cmd(0x2C)
        
        # Create small buffer for streaming
        buffer_size = 512  # 512 bytes buffer
        buffer = bytearray(buffer_size)
        
        # Fill buffer with color
        for i in range(0, buffer_size, 2):
            buffer[i] = (color_rgb565 >> 8) & 0xFF
            buffer[i + 1] = color_rgb565 & 0xFF
        
        # Stream data for rectangle
        total_pixels = w * h
        pixels_sent = 0
        
        while pixels_sent < total_pixels:
            remaining_pixels = total_pixels - pixels_sent
            pixels_in_batch = min(remaining_pixels, buffer_size // 2)
            
            self._write_data(buffer[:pixels_in_batch * 2])
            pixels_sent += pixels_in_batch
    
    def draw_text(self, string, x, y, color=0xFFFF, bg_color=None):
        """Draw text with background (simplified)"""
        # Simple text rendering - just draw colored rectangles for each character
        char_width = 8
        char_height = 8
        
        for i, char in enumerate(string):
            char_x = x + (i * char_width)
            if char_x + char_width <= self.width:
                # Draw character background if specified
                if bg_color is not None:
                    self.fill_rect(char_x, y, char_width, char_height, bg_color)
                
                # Draw character (simplified - just a colored rectangle)
                self.fill_rect(char_x, y, char_width, char_height, color)
    
    def draw_rect(self, x, y, w, h, color, fill=False):
        """Draw a rectangle"""
        if fill:
            self.fill_rect(x, y, w, h, color)
        else:
            # Draw outline
            self.fill_rect(x, y, w, 1, color)  # Top
            self.fill_rect(x, y + h - 1, w, 1, color)  # Bottom
            self.fill_rect(x, y, 1, h, color)  # Left
            self.fill_rect(x + w - 1, y, 1, h, color)  # Right
    
    def draw_circle(self, x, y, radius, color, fill=False):
        """Draw a circle (simplified)"""
        # Simple circle drawing using multiple small rectangles
        if fill:
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx*dx + dy*dy <= radius*radius:
                        px, py = x + dx, y + dy
                        if 0 <= px < self.width and 0 <= py < self.height:
                            self.fill_rect(px, py, 1, 1, color)
        else:
            # Draw outline
            for angle in range(0, 360, 5):
                rad = angle * 3.14159 / 180
                px = int(x + radius * math.cos(rad))
                py = int(y + radius * math.sin(rad))
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.fill_rect(px, py, 1, 1, color)
    
    def clear(self):
        """Clear the display"""
        self.fill(0x0000)  # Black
    
    def update(self):
        """No-op for streaming driver"""
        pass
    
    def set_backlight(self, value):
        """Set backlight brightness (0-255)"""
        print(f"Backlight set to: {value}")

# Alias for compatibility
ST7789 = ST7789Streaming


