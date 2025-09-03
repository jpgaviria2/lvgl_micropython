# ISOLATE INIT - Test display.init() step by step
print("=== ISOLATE DISPLAY INIT ===")

try:
    print("Step 1: Setup LVGL and hardware...")
    import machine
    import time
    import gc
    import lvgl as lv
    import lcd_bus
    import st7796
    
    lv.init()
    gc.collect()
    print(f"✓ Setup OK, memory: {gc.mem_free()} bytes")
    
    print("Step 2: Hardware reset...")
    rst_pin = machine.Pin(4, machine.Pin.OUT)
    rst_pin.off()
    time.sleep_ms(10)
    rst_pin.on()
    time.sleep_ms(10)
    print("✓ Reset OK")
    
    print("Step 3: Backlight...")
    machine.Pin(6, machine.Pin.OUT).on()
    print("✓ Backlight OK")
    
    print("Step 4: Create buses...")
    spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=2, sck=5)
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)
    print("✓ Buses OK")
    
    print("Step 5: Create display object...")
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
    
    print("Step 6a: Set power...")
    display.set_power(True)
    print("✓ Power set")
    
    print("Step 6b: Initialize display (CRITICAL STEP)...")
    display.init()
    print("✓ Display init completed!")
    
    print("Step 6c: Set backlight...")
    display.set_backlight(100)
    print("✓ Backlight set")
    
    print("Step 7: Test if we can get screen...")
    scr = lv.screen_active()
    print(f"✓ Got screen: {scr}")
    
    print("Step 8: Set background...")
    scr.set_style_bg_color(lv.color_hex(0xFF00FF), 0)  # Magenta
    print("✓ Background set")
    
    print("Step 9: Refresh...")
    lv.refr_now(lv.display_get_default())
    print("✓ Should see MAGENTA background!")
    
    print("SUCCESS: All steps completed!")
    
except Exception as e:
    print(f"CRASH at current step: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Memory after crash: {gc.mem_free()} bytes")
