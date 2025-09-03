# ST7796 MicroPython streaming driver for ESP32-S3 Touch LCD 3.5
# Mirrors the working 01_factory configuration
# - SPI host: SPI2
# - Pins: SCK=5, MOSI=1, DC=3, BL=6 (no CS, no RST)
# - Color: BGR, 16bpp (0x55)
# - Resolution: 320x480 (portrait)
# - Uses TCA9554 I/O expander to toggle LCD reset via Port1.Pin1

from machine import Pin, SPI, I2C
import time
try:
    import framebuf
except Exception:
    framebuf = None
try:
    from tca9554 import reset_lcd_via_tca9554
except Exception:
    # Fallback if helper not present
    reset_lcd_via_tca9554 = None

class ST7796:
    def __init__(
        self,
        sck_pin: int = 5,
        mosi_pin: int = 1,
        dc_pin: int = 3,
        bl_pin: int = 6,
        width: int = 320,
        height: int = 480,
        spi_id: int = 2,
        i2c_sda: int = 8,
        i2c_scl: int = 7,
        spi_baudrate: int = 80_000_000,
    ) -> None:
        self.width = width
        self.height = height
        self.dc = Pin(dc_pin, Pin.OUT)
        self.backlight = Pin(bl_pin, Pin.OUT)
        self.backlight.on()

        self.spi = SPI(spi_id, baudrate=spi_baudrate, polarity=0, phase=0,
                       sck=Pin(sck_pin), mosi=Pin(mosi_pin))

        # Perform reset via TCA9554 (I2C 0x20), if available
        try:
            if reset_lcd_via_tca9554 is not None:
                i2c = I2C(0, scl=Pin(i2c_scl), sda=Pin(i2c_sda), freq=100_000)
                reset_lcd_via_tca9554(i2c)
        except Exception:
            # Continue without hard reset
            pass

        self._init_panel()

    # Low-level helpers
    def _cmd(self, value: int) -> None:
        self.dc.off()
        self.spi.write(bytes([value & 0xFF]))

    def _data(self, buf: bytes) -> None:
        self.dc.on()
        self.spi.write(buf)

    def _init_panel(self) -> None:
        # Software reset
        self._cmd(0x01)
        time.sleep_ms(120)
        # Sleep out
        self._cmd(0x11)
        time.sleep_ms(120)

        # Vendor-specific init (mirrors ESP-IDF vendor_default)
        # Pixel format (vendor uses 0x05)
        self._cmd(0x3A); self._data(b"\x05")
        self._cmd(0xF0); self._data(b"\xC3")
        self._cmd(0xF0); self._data(b"\x96")
        self._cmd(0xB4); self._data(b"\x01")
        self._cmd(0xB7); self._data(b"\xC6")
        self._cmd(0xC0); self._data(b"\x80\x45")
        self._cmd(0xC1); self._data(b"\x13")
        self._cmd(0xC2); self._data(b"\xA7")
        self._cmd(0xC5); self._data(b"\x0A")
        self._cmd(0xE8); self._data(b"\x40\x8A\x00\x00\x29\x19\xA5\x33")
        self._cmd(0xE0); self._data(b"\xD0\x08\x0F\x06\x06\x33\x30\x33\x47\x17\x13\x13\x2B\x31")
        self._cmd(0xE1); self._data(b"\xD0\x0A\x11\x0B\x09\x07\x2F\x33\x47\x38\x15\x16\x2C\x32")
        self._cmd(0xF0); self._data(b"\x3C")
        self._cmd(0xF0); self._data(b"\x69")

        # Orientation: BGR | MX (fix horizontal mirroring; no rotation)
        self._cmd(0x36); self._data(b"\x48")

        # Define full window
        self._cmd(0x2A); self._data(bytes([0x00, 0x00, 0x01, 0x3F]))
        self._cmd(0x2B); self._data(bytes([0x00, 0x00, 0x01, 0xDF]))

        # Inversion ON and Display ON
        self._cmd(0x21)
        self._cmd(0x29)
        time.sleep_ms(20)

    def set_window(self, x: int, y: int, w: int, h: int) -> None:
        x0 = x
        x1 = x + w - 1
        y0 = y
        y1 = y + h - 1
        self._cmd(0x2A)
        self._data(bytes([(x0 >> 8) & 0xFF, x0 & 0xFF, (x1 >> 8) & 0xFF, x1 & 0xFF]))
        self._cmd(0x2B)
        self._data(bytes([(y0 >> 8) & 0xFF, y0 & 0xFF, (y1 >> 8) & 0xFF, y1 & 0xFF]))
        self._cmd(0x2C)

    @staticmethod
    def color565(r: int, g: int, b: int) -> int:
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

    def _stream_solid(self, pixel_color_565: int, pixel_count: int, chunk_bytes: int = 512) -> None:
        # Prepare a chunk buffer (must be even)
        if chunk_bytes % 2:
            chunk_bytes += 1
        hi = (pixel_color_565 >> 8) & 0xFF
        lo = pixel_color_565 & 0xFF
        buf = bytearray(chunk_bytes)
        for i in range(0, chunk_bytes, 2):
            buf[i] = hi
            buf[i + 1] = lo
        remaining = pixel_count
        while remaining > 0:
            pixels = min(remaining, chunk_bytes // 2)
            self._data(memoryview(buf)[: pixels * 2])
            remaining -= pixels

    def fill(self, color_565: int) -> None:
        self.set_window(0, 0, self.width, self.height)
        self._stream_solid(color_565, self.width * self.height)

    def fill_rect(self, x: int, y: int, w: int, h: int, color_565: int) -> None:
        if w <= 0 or h <= 0:
            return
        if x < 0:
            w += x
            x = 0
        if y < 0:
            h += y
            y = 0
        if x >= self.width or y >= self.height:
            return
        if x + w > self.width:
            w = self.width - x
        if y + h > self.height:
            h = self.height - y
        self.set_window(x, y, w, h)
        self._stream_solid(color_565, w * h)

    def clear(self) -> None:
        self.fill(0x0000)

    def draw_rect(self, x: int, y: int, w: int, h: int, color_565: int, fill: bool = False) -> None:
        if fill:
            self.fill_rect(x, y, w, h, color_565)
            return
        # Outline
        self.fill_rect(x, y, w, 1, color_565)
        self.fill_rect(x, y + h - 1, w, 1, color_565)
        self.fill_rect(x, y, 1, h, color_565)
        self.fill_rect(x + w - 1, y, 1, h, color_565)

    # Text rendering using MicroPython framebuf 8x8 font
    def draw_text(self, text: str, x: int, y: int, color_565: int, bg_color_565: int = None) -> None:
        if not text:
            return
        if framebuf is None:
            # Fallback: very simple blocks per char
            cw, ch = 8, 12
            cx = x
            for _ in text:
                if bg_color_565 is not None:
                    self.fill_rect(cx, y, cw, ch, bg_color_565)
                self.fill_rect(cx + 1, y + 2, cw - 2, ch - 4, color_565)
                cx += cw
            return

        # Use 8-pixel tall built-in font with correct MONO_HLSB packing (horizontal, LSB first)
        width_px = 8 * len(text)
        height = 8
        stride_bytes = (width_px + 7) // 8
        mono = bytearray(stride_bytes * height)
        fb = framebuf.FrameBuffer(mono, width_px, height, framebuf.MONO_HLSB)
        fb.fill(0)
        fb.text(text, 0, 0, 1)

        if bg_color_565 is None:
            bg_color_565 = 0x0000

        # Prepare one row buffer in RGB565
        row_buf = bytearray(width_px * 2)
        for row in range(height):
            base = row * stride_bytes
            idx = 0
            for col in range(width_px):
                byte = mono[base + (col >> 3)]
                # Treat leftmost pixel in each byte as MSB to fix mirrored glyphs
                bit = 0x80 >> (col & 7)
                c = color_565 if (byte & bit) else bg_color_565
                row_buf[idx] = (c >> 8) & 0xFF
                row_buf[idx + 1] = c & 0xFF
                idx += 2
            # Stream this row
            self.set_window(x, y + row, width_px, 1)
            self._data(row_buf)

    # Minimal circle rendering using midpoint algorithm (outline or filled)
    def draw_circle(self, cx: int, cy: int, r: int, color_565: int, fill: bool = False) -> None:
        if r <= 0:
            return
        x = r
        y = 0
        err = 1 - x

        def plot(px: int, py: int) -> None:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.fill_rect(px, py, 1, 1, color_565)

        while x >= y:
            if fill:
                # Draw horizontal spans to fill the circle
                self.fill_rect(cx - x, cy + y, 2 * x + 1, 1, color_565)
                self.fill_rect(cx - x, cy - y, 2 * x + 1, 1, color_565)
                self.fill_rect(cx - y, cy + x, 2 * y + 1, 1, color_565)
                self.fill_rect(cx - y, cy - x, 2 * y + 1, 1, color_565)
            else:
                plot(cx + x, cy + y)
                plot(cx - x, cy + y)
                plot(cx + x, cy - y)
                plot(cx - x, cy - y)
                plot(cx + y, cy + x)
                plot(cx - y, cy + x)
                plot(cx + y, cy - x)
                plot(cx - y, cy - x)

            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x + 1)

    def set_backlight(self, on: bool = True) -> None:
        if on:
            self.backlight.on()
        else:
            self.backlight.off()

    def update(self) -> None:
        # No-op for streaming driver
        pass

# Backwards-compatible alias if legacy code expects ST7789
ST7789 = ST7796
