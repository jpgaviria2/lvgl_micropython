# DISPLAY ONLY - Get display working first, add touch later
print("=== DISPLAY ONLY TEST ===")

def display_only_run(spi_hz=5_000_000, rotation=None, bgr=True, swap=True, do_reset=False):
    """Display-only version - no touch to avoid crashes"""
    
    import machine
    import time
    import gc
    import lvgl as lv
    import lcd_bus
    import st7796
    
    # Copy exact constants from lv_start.py
    LCD_SCLK = 5
    LCD_MOSI = 1
    LCD_MISO = 2
    LCD_DC = 3
    LCD_CS = -1
    LCD_BL = 6
    
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
    print("✓ Display hardware initialized")
    
    if rotation is not None:
        display.set_rotation(rotation)
    
    print("Step 5: Create UI (SKIP TOUCH for now)...")
    scr = lv.screen_active()
    scr.set_style_bg_color(lv.color_hex(0x00FF00), 0)  # Green
    
    label = lv.label(scr)
    label.set_text("DISPLAY WORKS!")
    label.set_style_text_color(lv.color_hex(0x000000), 0)  # Black text
    label.center()
    print("✓ UI created")
    
    print("Step 6: Single refresh...")
    lv.refr_now(lv.display_get_default())
    print("✓ Display refreshed")
    
    print("SUCCESS: Display is working! Green background with black text should be visible.")
    
    return display

# Test display-only version
try:
    print("Testing display-only version...")
    display = display_only_run(spi_hz=5_000_000, bgr=False, swap=True, do_reset=True)
    print("✓ DISPLAY-ONLY SUCCESS!")
    
    # Test if we can create interactive UI without touch
    print("\nTesting interactive UI without touch...")
    import lvgl as lv
    
    scr = lv.screen_active()
    
    # Add a button (won't work with touch, but tests UI creation)
    btn = lv.button(scr)
    btn.set_size(150, 60)
    btn.align(lv.ALIGN.CENTER, 0, 50)
    btn_label = lv.label(btn)
    btn_label.set_text("NO TOUCH YET")
    btn_label.center()
    
    lv.refr_now(lv.display_get_default())
    print("✓ Interactive UI created (button visible but no touch)")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
