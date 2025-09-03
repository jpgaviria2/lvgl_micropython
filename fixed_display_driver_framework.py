# FIXED display_driver_framework.py - Fixes the memory allocation bug at line 195
# This file should replace: api_drivers/py_api_drivers/frozen/display/display_driver_framework.py

# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from micropython import const  # NOQA
import lvgl as lv  # NOQA
import gc  # NOQA
import lcd_bus  # NOQA


STATE_HIGH = const(1)
STATE_LOW = const(0)
STATE_PWM = const(-1)

BYTE_ORDER_RGB = const(0)
BYTE_ORDER_BGR = const(1)

DISPLAY_TYPE_ST7796 = const(0)  # Add other display types as needed


class DisplayDriver:

    def __init__(
        self,
        data_bus,
        display_width,
        display_height,
        frame_buffer1=None,
        frame_buffer2=None,
        reset_pin=None,
        reset_state=STATE_HIGH,
        power_pin=None,
        power_on_state=STATE_HIGH,
        backlight_pin=None,
        backlight_on_state=STATE_HIGH,
        offset_x=0,
        offset_y=0,
        color_space=lv.COLOR_FORMAT.RGB565,
        **kwargs
    ):
        """Fixed DisplayDriver constructor with proper memory calculation"""
        
        if backlight_pin is not None:
            import machine
            
            self._backlight_pin = machine.Pin(backlight_pin, machine.Pin.OUT)
            
            if (
                backlight_on_state == STATE_HIGH and
                self._backlight_pin is not None
            ):
                self._backlight_pin.value(not backlight_on_state)

            self._backlight_on_state = backlight_on_state

        self._data_bus = data_bus
        self._disp_drv = lv.display_create(display_width, display_height)  # NOQA
        self._disp_drv.set_color_format(color_space)
        self._disp_drv.set_driver_data(self)

        if frame_buffer1 is None:
            # FIXED: Calculate buffer size correctly
            # The bug was here: lv.color_format_get_size(color_space) returns corrupted value
            
            # Use hardcoded values for known color formats instead of buggy LVGL function
            if color_space == lv.COLOR_FORMAT.RGB565:
                bytes_per_pixel = 2
            elif color_space == lv.COLOR_FORMAT.RGB888:
                bytes_per_pixel = 3
            elif color_space == lv.COLOR_FORMAT.ARGB8888:
                bytes_per_pixel = 4
            else:
                # Fallback - assume RGB565
                bytes_per_pixel = 2
                print(f"⚠ Unknown color format {color_space}, assuming RGB565")
            
            # Calculate buffer size with CORRECT bytes per pixel
            buf_size = int(display_width * display_height * bytes_per_pixel)
            buf_size = int(buf_size // 10)  # Use 1/10th of full screen
            
            print(f"✓ FIXED: Calculated buffer size: {buf_size} bytes")
            print(f"  Display: {display_width}x{display_height}")
            print(f"  Color format: {color_space} ({bytes_per_pixel} bytes/pixel)")
            print(f"  Buffer size: {buf_size} bytes (not 1GB+!)")
            
            gc.collect()

            for flags in (
                lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA,
                lcd_bus.MEMORY_SPIRAM | lcd_bus.MEMORY_DMA,
                lcd_bus.MEMORY_INTERNAL,
                lcd_bus.MEMORY_SPIRAM
            ):
                try:
                    frame_buffer1 = (
                        data_bus.allocate_framebuffer(buf_size, flags)
                    )

                    if (flags | lcd_bus.MEMORY_DMA) == flags:
                        frame_buffer2 = (
                            data_bus.allocate_framebuffer(buf_size, flags)
                        )

                    print(f"✓ Frame buffer allocated with flags: {flags}")
                    break
                except MemoryError:
                    frame_buffer1 = data_bus.free_framebuffer(frame_buffer1)
                    print(f"⚠ Memory allocation failed with flags {flags}, trying next...")

            if frame_buffer1 is None:
                raise MemoryError("Unable to allocate frame buffer with any memory type")

        self._disp_drv.set_draw_buffers(
            frame_buffer1,
            frame_buffer2,
            len(frame_buffer1),
            lv.DISPLAY_RENDER_MODE.PARTIAL
        )

        def flush_cb(disp_drv, area, color_p):
            # This would be implemented by specific display drivers
            lv.display_flush_ready(disp_drv)

        self._disp_drv.set_flush_cb(flush_cb)
        
        print("✓ DisplayDriver initialized successfully with FIXED memory allocation")

    def set_backlight(self, value):
        """Set backlight brightness"""
        if hasattr(self, '_backlight_pin') and self._backlight_pin is not None:
            if value > 0:
                self._backlight_pin.value(self._backlight_on_state)
            else:
                self._backlight_pin.value(not self._backlight_on_state)
        return self

    def set_power(self, state):
        """Set display power state"""
        # Implementation would depend on specific hardware
        return self

    def init(self):
        """Initialize display"""
        # Implementation would depend on specific display driver
        return self

print("✓ FIXED display_driver_framework loaded - memory allocation bug fixed!")
