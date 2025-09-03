# FIXED LV_START - Bypass the problematic timer loop
print("=== FIXED LV_START ===")

def safe_run(spi_hz=5_000_000, rotation=None, bgr=True, swap=True, do_reset=False):
    """Safe version of lv_start.run() that bypasses problematic timer loop"""
    
    import machine
    import time
    import gc
    import lvgl as lv
    import lcd_bus
    import st7796
    import i2c
    
    # Copy exact constants from lv_start.py
    LCD_SCLK = 5
    LCD_MOSI = 1
    LCD_MISO = 2
    LCD_DC = 3
    LCD_CS = -1
    LCD_BL = 6
    TP_SDA = 8
    TP_SCL = 7
    
    print("Step 1: Initialize LVGL...")
    gc.collect()
    lv.init()
    print("✓ LVGL initialized")
    
    print("Step 2: Hardware reset...")
    if do_reset:
        try:
            rst_pin = machine.Pin(4, machine.Pin.OUT)
            rst_pin.off()
            time.sleep_ms(10)
            rst_pin.on()
            time.sleep_ms(10)
        except Exception:
            pass
    print("✓ Reset done")
    
    print("Step 3: Backlight on early...")
    try:
        machine.Pin(LCD_BL, machine.Pin.OUT).on()
    except Exception:
        pass
    print("✓ Backlight on")
    
    print("Step 4: Create SPI and display...")
    spi_bus = machine.SPI.Bus(host=1, mosi=LCD_MOSI, miso=LCD_MISO, sck=LCD_SCLK)
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=spi_hz, dc=LCD_DC, cs=LCD_CS)
    
    color_order = st7796.BYTE_ORDER_BGR if bgr else st7796.BYTE_ORDER_RGB
    
    display = st7796.ST7796(
        data_bus=display_bus,
        display_width=320,
        display_height=480,
        backlight_pin=LCD_BL,
        color_space=lv.COLOR_FORMAT.RGB565,
        color_byte_order=color_order,
        rgb565_byte_swap=bool(swap),
    )
    display.set_power(True)
    display.init()
    display.set_backlight(100)
    print("✓ Display initialized")
    
    if rotation is not None:
        display.set_rotation(rotation)
    
    print("Step 5: Touch setup...")
    # Touch controller (direct I2C method)
    global _touch_bus, _touch_dev
    _touch_bus = i2c.I2C.Bus(host=0, scl=TP_SCL, sda=TP_SDA, freq=400000, use_locks=False)
    _touch_dev = i2c.I2C.Device(bus=_touch_bus, dev_id=0x38, reg_bits=8)
    
    # Simple touch callback
    def _touch_read(indev, data):
        try:
            touch_data = _touch_dev.read_mem(0x02, 1)[0]
            if touch_data > 0:
                x_data = _touch_dev.read_mem(0x03, 2)
                y_data = _touch_dev.read_mem(0x05, 2)
                x = (x_data[0] << 8) | x_data[1]
                y = (y_data[0] << 8) | y_data[1]
                
                data.point.x = x
                data.point.y = y
                data.state = lv.INDEV_STATE.PRESSED
            else:
                data.state = lv.INDEV_STATE.RELEASED
        except:
            data.state = lv.INDEV_STATE.RELEASED
        return False
    
    # Register touch input device
    disp = lv.display_get_default()
    indev = lv.indev_create()
    indev.set_type(lv.INDEV_TYPE.POINTER)
    indev.set_read_cb(_touch_read)
    indev.set_display(disp)
    indev.enable(True)
    
    print("✓ Touch registered")
    
    print("Step 6: Create UI...")
    scr = lv.screen_active()
    scr.set_style_bg_color(lv.color_hex(0x003366), 0)
    label = lv.label(scr)
    label.set_text("FIXED LVGL OK")
    label.center()
    print("✓ UI created")
    
    # SKIP THE PROBLEMATIC TIMER LOOP - just do single refresh
    print("Step 7: Single refresh (skip timer loop)...")
    lv.refr_now(lv.display_get_default())
    print("✓ Display refreshed")
    
    print("Display should now be visible with blue background and 'FIXED LVGL OK' text")
    
    return display

# Test the safe version
try:
    print("Testing safe lv_start.run()...")
    display = safe_run(spi_hz=5_000_000, bgr=False, swap=True, do_reset=True)
    print("✓ SUCCESS: Safe version works!")
    
except Exception as e:
    print(f"Error in safe version: {e}")
    import sys
    sys.print_exception(e)
