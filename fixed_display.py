# FIXED DISPLAY - Correct ST7796 parameters
print("=== FIXED DISPLAY TEST ===")

try:
    print("Step 1: Import and setup...")
    import machine
    import time
    import gc
    import lvgl as lv
    import lcd_bus
    import st7796
    print("✓ Imports OK")
    
    print("Step 2: Memory check...")
    gc.collect()
    print(f"Free memory: {gc.mem_free()} bytes")
    
    print("Step 3: Hardware reset...")
    rst_pin = machine.Pin(4, machine.Pin.OUT)
    rst_pin.off()
    time.sleep_ms(10)
    rst_pin.on()
    time.sleep_ms(10)
    print("✓ Reset OK")
    
    print("Step 4: Create buses...")
    spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=-1, sck=5)
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)
    print("✓ Buses created")
    
    print("Step 5: Create display with CORRECTED parameters...")
    display = st7796.ST7796(
        data_bus=display_bus,
        display_width=320,  # Correct width
        display_height=480, # Correct height  
        backlight_pin=6,
        color_space=lv.COLOR_FORMAT.RGB565,  # 16-bit color
        color_byte_order=st7796.BYTE_ORDER_BGR,
        reset_pin=4,
        reset_state=st7796.STATE_LOW,
        # Add these missing parameters that might be causing issues:
        frame_buffer1=None,  # Let driver allocate
        frame_buffer2=None,  # Let driver allocate
    )
    print("✓ Display object created successfully!")
    
    print("Step 6: Initialize display...")
    display.init()
    print("✓ Display initialized")
    
    print("Step 7: Test LVGL...")
    scr = lv.screen_active()
    scr.set_style_bg_color(lv.color_hex(0x00FF00), 0)  # Green
    lv.refr_now(lv.display_get_default())
    print("✓ Should see GREEN background!")
    
    print("Step 8: Add text...")
    label = lv.label(scr)
    label.set_text("DISPLAY FIXED!")
    label.set_style_text_color(lv.color_hex(0x000000), 0)  # Black text
    label.center()
    lv.refr_now(lv.display_get_default())
    print("✓ Should see black 'DISPLAY FIXED!' text on green!")
    
    print("SUCCESS: Display is working!")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Memory after error: {gc.mem_free()} bytes")
