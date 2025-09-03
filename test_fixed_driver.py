# TEST FIXED DRIVER - Test the corrected ST7796 implementation
print("=== TEST FIXED ST7796 DRIVER ===")

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

def test_fixed_driver():
    """Test the fixed ST7796 driver"""
    
    # Step 1: Import fixed driver
    def step1():
        exec(open('/fixed_st7796.py').read())
        return "Fixed ST7796 driver loaded"
    
    if not safe_step(1, "Load fixed ST7796 driver", step1, 1000):
        return False
    
    # Step 2: Initialize LVGL
    def step2():
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
    
    if not safe_step(2, "Initialize LVGL", step2, 1000):
        return False
    
    # Step 3: Hardware setup
    def step3():
        global machine, time, backlight, rst_pin
        import machine, time
        
        # Reset pin
        rst_pin = machine.Pin(4, machine.Pin.OUT)
        rst_pin.off()
        time.sleep_ms(50)
        rst_pin.on()
        time.sleep_ms(100)
        
        # Backlight
        backlight = machine.Pin(6, machine.Pin.OUT)
        backlight.on()
        
        return "Hardware pins configured"
    
    if not safe_step(3, "Configure hardware pins", step3, 1000):
        return False
    
    # Step 4: Create SPI bus
    def step4():
        global spi_bus, display_bus
        import lcd_bus
        
        spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=2, sck=5)
        display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)
        
        return f"SPI buses created: {spi_bus}, {display_bus}"
    
    if not safe_step(4, "Create SPI buses", step4, 1000):
        return False
    
    # Step 5: Create FIXED display (this should not crash!)
    def step5():
        global display
        
        # Use the fixed driver instead of the broken st7796
        display = create_fixed_st7796(
            data_bus=display_bus,
            display_width=320,
            display_height=480,
            backlight_pin=6,
            color_space=lv.COLOR_FORMAT.RGB565,
            color_byte_order=BYTE_ORDER_RGB,
            rgb565_byte_swap=True,
            reset_pin=4,
            reset_state=STATE_HIGH,
        )
        
        return f"Fixed ST7796 created: {display}"
    
    if not safe_step(5, "Create FIXED ST7796 display", step5, 1000):
        return False
    
    # Step 6: Initialize display hardware
    def step6():
        display.set_power(True)
        display.init()
        display.set_backlight(100)
        
        return "Display hardware initialized"
    
    if not safe_step(6, "Initialize display hardware", step6, 1500):
        return False
    
    # Step 7: Create UI
    def step7():
        global scr, label
        
        scr = lv.screen_active()
        scr.set_style_bg_color(lv.color_hex(0x00FF00), 0)  # Green
        
        label = lv.label(scr)
        label.set_text("FIXED DRIVER!")
        label.set_style_text_color(lv.color_hex(0x000000), 0)  # Black
        label.center()
        
        return "UI elements created"
    
    if not safe_step(7, "Create UI elements", step7, 1000):
        return False
    
    # Step 8: Test refresh (the critical test!)
    def step8():
        disp = lv.display_get_default()
        lv.refr_now(disp)
        return "Display refreshed successfully!"
    
    if not safe_step(8, "Refresh display (CRITICAL TEST)", step8, 1000):
        return False
    
    print("\n🎉 SUCCESS: Fixed ST7796 driver working!")
    print("✅ No memory allocation crashes")
    print("✅ Display refresh works")
    print("✅ UI elements created")
    print("Green background with black 'FIXED DRIVER!' text should be visible")
    return True

# Run the test
try:
    success = test_fixed_driver()
    if success:
        print("\n=== FIXED DRIVER TEST COMPLETE ===")
        print("The fixed ST7796 driver solves the memory allocation bug!")
    else:
        print("\n=== FIXED DRIVER TEST FAILED ===")
        print("Check which step failed above.")
        
except Exception as e:
    print(f"\nUNEXPECTED ERROR: {e}")
    import sys
    sys.print_exception(e)
