# BYPASS INIT - Skip problematic display.init() and go straight to UI
print("=== BYPASS DISPLAY INIT ===")

try:
    print("Step 1: Setup like working lv_start...")
    import machine
    import time
    import gc
    import lvgl as lv
    import lcd_bus
    import st7796
    
    lv.init()
    gc.collect()
    print("✓ LVGL initialized")
    
    print("Step 2: Hardware setup...")
    rst_pin = machine.Pin(4, machine.Pin.OUT)
    rst_pin.off()
    time.sleep_ms(10)
    rst_pin.on()
    time.sleep_ms(10)
    machine.Pin(6, machine.Pin.OUT).on()
    print("✓ Hardware ready")
    
    print("Step 3: Create buses and display...")
    spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=2, sck=5)
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)
    
    display = st7796.ST7796(
        data_bus=display_bus,
        display_width=320,
        display_height=480,
        backlight_pin=6,
        color_space=lv.COLOR_FORMAT.RGB565,
        color_byte_order=st7796.BYTE_ORDER_RGB,
        rgb565_byte_swap=True,
    )
    print("✓ Display object created")
    
    print("Step 4: Power on (skip init for now)...")
    display.set_power(True)
    print("✓ Power on")
    
    print("Step 5: Try UI without display.init()...")
    # Skip display.init() and go straight to UI like some working examples
    scr = lv.screen_active()
    scr.set_style_bg_color(lv.color_hex(0x00FFFF), 0)  # Cyan
    
    label = lv.label(scr)
    label.set_text("BYPASS TEST")
    label.set_style_text_color(lv.color_hex(0x000000), 0)
    label.center()
    
    print("Step 6: Refresh...")
    lv.refr_now(lv.display_get_default())
    print("✓ Should see CYAN background with black text!")
    
    print("Step 7: Now try display.init() after UI...")
    display.init()
    display.set_backlight(100)
    print("✓ Display init after UI - SUCCESS!")
    
    print("SUCCESS: Bypass method worked!")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Memory: {gc.mem_free()} bytes")
