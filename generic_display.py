# GENERIC DISPLAY - Bypass ST7796, use basic LVGL display
print("=== GENERIC DISPLAY TEST ===")

try:
    print("Step 1: Basic setup...")
    import machine
    import time
    import gc
    import lvgl as lv
    print("✓ Basic imports OK")
    
    print("Step 2: Initialize LVGL...")
    lv.init()
    gc.collect()
    print(f"✓ LVGL init, memory: {gc.mem_free()} bytes")
    
    print("Step 3: Hardware pins...")
    # Just control backlight directly
    backlight = machine.Pin(6, machine.Pin.OUT)
    backlight.on()
    print("✓ Backlight on")
    
    print("Step 4: Try basic LVGL without display driver...")
    # Create a basic display buffer in memory
    # This bypasses all hardware drivers
    
    # Get default display (should exist after lv.init())
    disp = lv.display_get_default()
    if disp:
        print(f"✓ Got default display: {disp}")
    else:
        print("! No default display, creating one...")
        # Create a basic display
        disp = lv.display_create(320, 480)
        print(f"✓ Created display: {disp}")
    
    print("Step 5: Test LVGL UI without hardware...")
    scr = lv.screen_active()
    scr.set_style_bg_color(lv.color_hex(0xFF0000), 0)  # Red
    
    label = lv.label(scr)
    label.set_text("GENERIC TEST")
    label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    label.center()
    
    print("Step 6: Refresh...")
    lv.refr_now(disp)
    print("✓ LVGL UI created (no hardware display)")
    
    print("Step 7: Test if system is stable...")
    for i in range(10):
        lv.timer_handler()
        time.sleep_ms(50)
        if i % 3 == 0:
            print(f"Stable test {i}...")
    
    print("SUCCESS: LVGL system is stable without hardware drivers!")
    print("This means the issue is with ST7796 or hardware drivers.")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Memory: {gc.mem_free()} bytes")
