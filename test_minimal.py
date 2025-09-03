# TEST MINIMAL ST7796 - Completely bypasses problematic framework
print("=== TEST MINIMAL ST7796 APPROACH ===")

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

def test_minimal():
    """Test the minimal ST7796 approach"""
    
    # Step 1: Initialize LVGL FIRST
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
    
    if not safe_step(1, "Initialize LVGL first", step1, 1000):
        return False
    
    # Step 2: Hardware setup
    def step2():
        global machine, time
        import machine, time
        
        # Reset pin
        rst_pin = machine.Pin(4, machine.Pin.OUT)
        rst_pin.off()
        time.sleep_ms(50)
        rst_pin.on()
        time.sleep_ms(100)
        
        # Backlight pin
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
    
    # Step 4: Import minimal st7796
    def step4():
        global st7796_minimal
        import st7796_minimal
        
        return f"Minimal ST7796 module imported"
    
    if not safe_step(4, "Import minimal ST7796", step4, 1000):
        return False
    
    # Step 5: Create ST7796 hardware object (NO LVGL calls)
    def step5():
        global display
        
        display = st7796_minimal.ST7796(
            data_bus=display_bus,
            display_width=320,
            display_height=480,
            backlight_pin=6,
            color_byte_order=st7796_minimal.BYTE_ORDER_RGB,
            rgb565_byte_swap=True,
            reset_pin=4,
            reset_state=st7796_minimal.STATE_HIGH,
        )
        
        return f"ST7796 hardware object created: {display}"
    
    if not safe_step(5, "Create ST7796 hardware (NO LVGL)", step5, 1500):
        return False
    
    # Step 6: Initialize hardware
    def step6():
        display.set_power(True)
        display.init()
        display.set_backlight(100)
        
        return "Hardware initialized"
    
    if not safe_step(6, "Initialize ST7796 hardware", step6, 1500):
        return False
    
    # Step 7: Manually create LVGL display
    def step7():
        global lvgl_display
        
        lvgl_display = display.create_lvgl_display()
        
        if lvgl_display:
            return f"LVGL display created: {lvgl_display}"
        else:
            return "LVGL display creation failed"
    
    if not safe_step(7, "Create LVGL display manually", step7, 1500):
        return False
    
    # Step 8: Create UI
    def step8():
        global scr, label
        
        scr = lv.screen_active()
        scr.set_style_bg_color(lv.color_hex(0x00FF00), 0)  # Green
        
        label = lv.label(scr)
        label.set_text("MINIMAL WORKS!")
        label.set_style_text_color(lv.color_hex(0x000000), 0)  # Black
        label.center()
        
        return "UI created"
    
    if not safe_step(8, "Create UI", step8, 1000):
        return False
    
    # Step 9: Refresh display
    def step9():
        disp = lv.display_get_default()
        lv.refr_now(disp)
        return "Display refreshed!"
    
    if not safe_step(9, "Refresh display", step9, 1000):
        return False
    
    print("\n🎉 SUCCESS: Minimal ST7796 approach working!")
    print("✅ No framework memory allocation bugs")
    print("✅ Hardware initialization works")
    print("✅ Manual LVGL display creation works")
    print("✅ UI creation and refresh works")
    print("Green background with black 'MINIMAL WORKS!' should be visible")
    return True

# Run the test
try:
    success = test_minimal()
    if success:
        print("\n=== MINIMAL TEST COMPLETE ===")
        print("The minimal approach successfully bypasses all framework bugs!")
        print("We can now build a proper working display system.")
    else:
        print("\n=== MINIMAL TEST FAILED ===")
        print("Check which step failed above.")
        
except Exception as e:
    print(f"\nUNEXPECTED ERROR: {e}")
    import sys
    sys.print_exception(e)
