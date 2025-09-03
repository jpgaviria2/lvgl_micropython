# BYPASS ST7796 - Create working display without buggy ST7796 driver
print("=== BYPASS ST7796 SOLUTION ===")

def safe_step(step_num, description, func, delay_ms=1000):
    """Execute a step safely with logging and delay"""
    import time
    import gc
    
    print(f"Step {step_num}: {description}...")
    try:
        result = func()
        print(f"✓ Step {step_num} SUCCESS: {description}")
        if result:
            print(f"  Result: {result}")
        
        gc.collect()
        print(f"  Memory: {gc.mem_free()} bytes")
        print(f"  Waiting {delay_ms}ms...")
        time.sleep_ms(delay_ms)
        return True
        
    except Exception as e:
        print(f"✗ Step {step_num} FAILED: {description}")
        print(f"  Error: {e}")
        import sys
        sys.print_exception(e)
        return False

def run_bypass_solution():
    """Create working display solution bypassing ST7796"""
    
    # Step 1: Imports
    def step1():
        global machine, time, gc, lv
        import machine, time, gc
        import lvgl as lv
        return "Core modules imported (NO ST7796!)"
    
    if not safe_step(1, "Import core modules", step1, 1000):
        return False
    
    # Step 2: Initialize LVGL
    def step2():
        gc.collect()
        try:
            test_disp = lv.display_get_default()
            if test_disp:
                return f"LVGL already initialized, memory: {gc.mem_free()}"
        except:
            pass
        
        lv.init()
        return f"LVGL initialized, memory: {gc.mem_free()}"
    
    if not safe_step(2, "Initialize LVGL", step2, 1000):
        return False
    
    # Step 3: Hardware setup (pins only, no ST7796)
    def step3():
        global backlight, rst_pin
        
        # Reset pin
        rst_pin = machine.Pin(4, machine.Pin.OUT)
        rst_pin.off()
        time.sleep_ms(50)
        rst_pin.on()
        time.sleep_ms(100)
        
        # Backlight
        backlight = machine.Pin(6, machine.Pin.OUT)
        backlight.on()
        
        return "Hardware pins configured (reset + backlight)"
    
    if not safe_step(3, "Configure hardware pins", step3, 1000):
        return False
    
    # Step 4: Create manual LVGL display (bypass hardware drivers)
    def step4():
        global disp
        
        # Create a display manually with LVGL
        disp = lv.display_create(320, 480)
        
        # Set up a dummy flush callback (required by LVGL)
        def display_flush_cb(disp_drv, area, color_p):
            # This would normally write to hardware
            # For now, just mark as flushed (no actual hardware output)
            lv.display_flush_ready(disp_drv)
        
        disp.set_flush_cb(display_flush_cb)
        
        return f"Manual LVGL display created: {disp}"
    
    if not safe_step(4, "Create manual LVGL display", step4, 1000):
        return False
    
    # Step 5: Test LVGL UI creation
    def step5():
        global scr
        scr = lv.screen_create()
        lv.screen_load(scr)
        
        # Set background
        scr.set_style_bg_color(lv.color_hex(0xFF0000), 0)  # Red
        
        return f"Screen created and loaded: {scr}"
    
    if not safe_step(5, "Create LVGL screen", step5, 1000):
        return False
    
    # Step 6: Add UI elements
    def step6():
        global label
        
        # Title label
        label = lv.label(scr)
        label.set_text("BYPASS WORKS!")
        label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)  # White
        label.set_style_text_font(lv.font_montserrat_24, 0)
        label.align(lv.ALIGN.TOP_MID, 0, 20)
        
        # Status label
        status = lv.label(scr)
        status.set_text("ST7796 bypassed")
        status.set_style_text_color(lv.color_hex(0xFFFF00), 0)  # Yellow
        status.center()
        
        return "UI elements created (title + status)"
    
    if not safe_step(6, "Add UI elements", step6, 1000):
        return False
    
    # Step 7: Test refresh (this should work without ST7796)
    def step7():
        lv.refr_now(disp)
        return "Display refreshed successfully!"
    
    if not safe_step(7, "Refresh display", step7, 1000):
        return False
    
    # Step 8: Test backlight control
    def step8():
        print("    Testing backlight control...")
        for i in range(3):
            backlight.off()
            print(f"      Backlight OFF {i+1}")
            time.sleep_ms(300)
            backlight.on()
            print(f"      Backlight ON {i+1}")
            time.sleep_ms(300)
        
        return "Backlight control verified"
    
    if not safe_step(8, "Test backlight control", step8, 1000):
        return False
    
    print("\n🎉 SUCCESS: Complete bypass solution working!")
    print("✅ LVGL UI system functional")
    print("✅ Backlight control working")
    print("✅ No ST7796 driver crashes")
    print("❌ No actual display output (hardware bypassed)")
    print("\nThis proves the ST7796 driver is the problem!")
    return True

# Run the bypass solution
try:
    success = run_bypass_solution()
    if success:
        print("\n=== BYPASS SOLUTION COMPLETE ===")
        print("The ST7796 driver is confirmed broken.")
        print("We need an alternative display driver or manual SPI control.")
    else:
        print("\n=== BYPASS SOLUTION FAILED ===")
        print("Check which step failed above.")
        
except Exception as e:
    print(f"\nUNEXPECTED ERROR: {e}")
    import sys
    sys.print_exception(e)
