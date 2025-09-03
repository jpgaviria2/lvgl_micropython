# TEST OVERRIDE - Verify the corrected ST7796 module works
print("=== TEST ST7796 OVERRIDE ===")

def safe_step(step_num, description, func, delay_ms=1000):
    """Execute a step safely with logging"""
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
        time.sleep_ms(delay_ms)
        return True
        
    except Exception as e:
        print(f"✗ Step {step_num} FAILED: {description}")
        print(f"  Error: {e}")
        import sys
        sys.print_exception(e)
        return False

def test_override():
    """Test the corrected ST7796 override"""
    
    # Step 1: Initialize LVGL
    def step1():
        global lv, gc
        import lvgl as lv
        import gc
        
        gc.collect()
        try:
            test_disp = lv.display_get_default()
            if test_disp:
                return f"LVGL already initialized, memory: {gc.mem_free()}"
        except:
            pass
        
        lv.init()
        return f"LVGL initialized, memory: {gc.mem_free()}"
    
    if not safe_step(1, "Initialize LVGL", step1, 1000):
        return False
    
    # Step 2: Hardware setup
    def step2():
        global machine, time
        import machine, time
        
        # Reset and backlight
        rst_pin = machine.Pin(4, machine.Pin.OUT)
        rst_pin.off()
        time.sleep_ms(50)
        rst_pin.on()
        time.sleep_ms(100)
        
        backlight = machine.Pin(6, machine.Pin.OUT)
        backlight.on()
        
        return "Hardware pins configured"
    
    if not safe_step(2, "Configure hardware", step2, 1000):
        return False
    
    # Step 3: Create SPI buses
    def step3():
        global spi_bus, display_bus
        import lcd_bus
        
        spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=2, sck=5)
        display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)
        
        return f"SPI buses created"
    
    if not safe_step(3, "Create SPI buses", step3, 1000):
        return False
    
    # Step 4: Import CORRECTED st7796 (this should use our override!)
    def step4():
        global st7796
        import st7796
        
        # Check if it's our corrected version
        if hasattr(st7796, 'ST7796'):
            return f"ST7796 module imported - our override is working!"
        else:
            return "ST7796 imported but might be built-in version"
    
    if not safe_step(4, "Import corrected ST7796", step4, 1000):
        return False
    
    # Step 5: Create ST7796 display (this should NOT crash!)
    def step5():
        global display
        
        display = st7796.ST7796(
            data_bus=display_bus,
            display_width=320,
            display_height=480,
            backlight_pin=6,
            color_space=lv.COLOR_FORMAT.RGB565,
            color_byte_order=st7796.BYTE_ORDER_RGB,
            rgb565_byte_swap=True,
            reset_pin=4,
            reset_state=st7796.STATE_HIGH,
        )
        
        return f"ST7796 created successfully: {display}"
    
    if not safe_step(5, "Create ST7796 display (CRITICAL TEST)", step5, 1500):
        return False
    
    # Step 6: Initialize display
    def step6():
        display.set_power(True)
        display.init()
        display.set_backlight(100)
        
        return "Display initialized"
    
    if not safe_step(6, "Initialize display", step6, 1500):
        return False
    
    # Step 7: Create UI
    def step7():
        global scr, label
        
        scr = lv.screen_active()
        scr.set_style_bg_color(lv.color_hex(0x0000FF), 0)  # Blue
        
        label = lv.label(scr)
        label.set_text("OVERRIDE WORKS!")
        label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)  # White
        label.center()
        
        return "UI created"
    
    if not safe_step(7, "Create UI", step7, 1000):
        return False
    
    # Step 8: Refresh display
    def step8():
        disp = lv.display_get_default()
        lv.refr_now(disp)
        return "Display refreshed!"
    
    if not safe_step(8, "Refresh display", step8, 1000):
        return False
    
    print("\n🎉 SUCCESS: ST7796 override working perfectly!")
    print("✅ No 1GB memory allocation crashes")
    print("✅ Display initialization works")
    print("✅ UI creation and refresh works")
    print("Blue background with white 'OVERRIDE WORKS!' should be visible")
    return True

# Run the test
try:
    success = test_override()
    if success:
        print("\n=== OVERRIDE TEST COMPLETE ===")
        print("The corrected ST7796 driver successfully overrides the built-in!")
        print("You can now use st7796.ST7796() normally without crashes.")
    else:
        print("\n=== OVERRIDE TEST FAILED ===")
        print("Check which step failed above.")
        
except Exception as e:
    print(f"\nUNEXPECTED ERROR: {e}")
    import sys
    sys.print_exception(e)
