# CORRECT INIT - Initialize LVGL first!
print("=== CORRECT INITIALIZATION ===")

try:
    print("Step 1: Import modules...")
    import machine
    import time
    import gc
    import lvgl as lv
    import lcd_bus
    import st7796
    print("✓ Imports OK")
    
    print("Step 2: CRITICAL - Initialize LVGL first!")
    lv.init()  # This was missing!
    print("✓ LVGL initialized")
    
    print("Step 3: Garbage collect...")
    gc.collect()
    print(f"Free memory: {gc.mem_free()} bytes")
    
    print("Step 4: Hardware reset...")
    rst_pin = machine.Pin(4, machine.Pin.OUT)
    rst_pin.off()
    time.sleep_ms(10)
    rst_pin.on()
    time.sleep_ms(10)
    print("✓ Reset OK")
    
    print("Step 5: Backlight on early...")
    machine.Pin(6, machine.Pin.OUT).on()
    print("✓ Backlight on")
    
    print("Step 6: Create buses...")
    spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=2, sck=5)
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)
    print("✓ Buses created")
    
    print("Step 7: Create display (with LVGL initialized)...")
    color_order = st7796.BYTE_ORDER_RGB  # bgr=False
    display = st7796.ST7796(
        data_bus=display_bus,
        display_width=320,
        display_height=480,
        backlight_pin=6,
        color_space=lv.COLOR_FORMAT.RGB565,
        color_byte_order=color_order,
        rgb565_byte_swap=True,  # swap=True
    )
    print("✓ Display object created successfully!")
    
    print("Step 8: Configure and initialize display...")
    display.set_power(True)
    display.init()
    display.set_backlight(100)
    print("✓ Display initialized")
    
    print("Step 9: Create UI...")
    scr = lv.screen_active()
    scr.set_style_bg_color(lv.color_hex(0x003366), 0)  # Blue like lv_start
    
    label = lv.label(scr)
    label.set_text("CORRECT INIT!")
    label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    label.center()
    print("✓ UI created")
    
    print("Step 10: Refresh display...")
    lv.refr_now(lv.display_get_default())
    print("✓ Should see blue background with white 'CORRECT INIT!' text!")
    
    print("SUCCESS: Display working with correct initialization!")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Memory: {gc.mem_free()} bytes")
