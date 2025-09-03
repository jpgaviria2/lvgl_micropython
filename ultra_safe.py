# ULTRA SAFE TEST - Test each LVGL operation individually
print("=== ULTRA SAFE TEST ===")

try:
    print("Step 1: Basic imports...")
    import machine
    import time
    import gc
    print("✓ Basic imports OK")
    
    print("Step 2: Import LVGL...")
    import lvgl as lv
    print("✓ LVGL imported OK")
    
    print("Step 3: Import display drivers...")
    import lcd_bus
    import st7796
    print("✓ Display drivers imported OK")
    
    print("Step 4: Memory check...")
    gc.collect()
    print(f"Free memory: {gc.mem_free()} bytes")
    
    print("Step 5: Hardware reset...")
    rst_pin = machine.Pin(4, machine.Pin.OUT)
    rst_pin.off()
    time.sleep_ms(10)
    rst_pin.on()
    time.sleep_ms(10)
    print("✓ Hardware reset OK")
    
    print("Step 6: Create SPI bus...")
    spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=-1, sck=5)
    print("✓ SPI bus created")
    
    print("Step 7: Create display bus...")
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)
    print("✓ Display bus created")
    
    print("Step 8: Create display object...")
    display = st7796.ST7796(
        data_bus=display_bus,
        display_width=320,
        display_height=480,
        backlight_pin=6,
        color_space=lv.COLOR_FORMAT.RGB565,
        color_byte_order=st7796.BYTE_ORDER_BGR,
        reset_pin=4,
        reset_state=st7796.STATE_LOW
    )
    print("✓ Display object created")
    
    print("Step 9: Initialize display...")
    display.init()
    print("✓ Display initialized")
    
    print("Step 10: Get active screen...")
    scr = lv.screen_active()
    print(f"✓ Got screen: {scr}")
    
    print("Step 11: Set background color...")
    scr.set_style_bg_color(lv.color_hex(0xFF0000), 0)  # Red
    print("✓ Background color set")
    
    print("Step 12: Force refresh...")
    lv.refr_now(lv.display_get_default())
    print("✓ Display refreshed - should see RED background!")
    
    print("Step 13: Create label...")
    label = lv.label(scr)
    print("✓ Label created")
    
    print("Step 14: Set label text...")
    label.set_text("SUCCESS!")
    print("✓ Label text set")
    
    print("Step 15: Set label color...")
    label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    print("✓ Label color set")
    
    print("Step 16: Center label...")
    label.center()
    print("✓ Label centered")
    
    print("Step 17: Final refresh...")
    lv.refr_now(lv.display_get_default())
    print("✓ SUCCESS! Should see red background with white 'SUCCESS!' text")
    
    print("Step 18: Memory check after success...")
    gc.collect()
    print(f"Final free memory: {gc.mem_free()} bytes")
    
except Exception as e:
    print(f"CRASH at current step: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Memory after crash: {gc.mem_free()} bytes")
