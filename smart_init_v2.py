# SMART INITIALIZATION V2 - With longer delays and LVGL protection
print("=== SMART INITIALIZATION V2 ===")

def safe_step(step_num, description, func, delay_ms=1000):
    """Execute a step safely with logging and longer delay"""
    import time
    import gc
    
    print(f"Step {step_num}: {description}...")
    try:
        result = func()
        print(f"✓ Step {step_num} SUCCESS: {description}")
        if result:
            print(f"  Result: {result}")
        
        # Memory check after each step
        gc.collect()
        print(f"  Memory: {gc.mem_free()} bytes")
        
        # Longer delay before next step
        print(f"  Waiting {delay_ms}ms before next step...")
        time.sleep_ms(delay_ms)
        return True
        
    except Exception as e:
        print(f"✗ Step {step_num} FAILED: {description}")
        print(f"  Error: {e}")
        import sys
        sys.print_exception(e)
        return False

def run_smart_init_v2():
    """Run initialization with longer delays and LVGL protection"""
    
    # Step 1: Imports with extra delay
    def step1():
        global machine, time, gc, lv, lcd_bus, st7796, i2c
        import machine, time, gc
        import lvgl as lv
        import lcd_bus, st7796, i2c
        return "All modules imported"
    
    if not safe_step(1, "Import all modules", step1, 2000):
        return False
    
    # Step 2: Initialize LVGL with protection
    def step2():
        gc.collect()
        print("    Checking if LVGL already initialized...")
        
        # Try to check if LVGL is already initialized
        try:
            # Test if we can get default display (indicates LVGL is initialized)
            test_disp = lv.display_get_default()
            if test_disp:
                print("    LVGL already initialized, skipping lv.init()")
                return f"LVGL already initialized, memory: {gc.mem_free()}"
        except:
            pass
        
        print("    Calling lv.init()...")
        lv.init()
        return f"LVGL initialized, memory: {gc.mem_free()}"
    
    if not safe_step(2, "Initialize LVGL (with protection)", step2, 2000):
        return False
    
    # Step 3: Hardware reset with longer delay
    def step3():
        print("    Setting reset pin low...")
        rst_pin = machine.Pin(4, machine.Pin.OUT)
        rst_pin.off()
        time.sleep_ms(50)  # Longer reset pulse
        print("    Setting reset pin high...")
        rst_pin.on()
        time.sleep_ms(100)  # Longer recovery time
        return "Hardware reset completed"
    
    if not safe_step(3, "Hardware reset", step3, 1500):
        return False
    
    # Step 4: Backlight
    def step4():
        global backlight
        backlight = machine.Pin(6, machine.Pin.OUT)
        backlight.on()
        return "Backlight enabled"
    
    if not safe_step(4, "Enable backlight", step4, 1000):
        return False
    
    # Step 5: SPI bus
    def step5():
        global spi_bus
        spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=2, sck=5)
        return f"SPI bus created: {spi_bus}"
    
    if not safe_step(5, "Create SPI bus", step5, 1000):
        return False
    
    # Step 6: Display bus
    def step6():
        global display_bus
        display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)
        return f"Display bus created: {display_bus}"
    
    if not safe_step(6, "Create display bus", step6, 1000):
        return False
    
    # Step 7: Create display object
    def step7():
        global display
        display = st7796.ST7796(
            data_bus=display_bus,
            display_width=320,
            display_height=480,
            backlight_pin=6,
            color_space=lv.COLOR_FORMAT.RGB565,
            color_byte_order=st7796.BYTE_ORDER_RGB,
            rgb565_byte_swap=True,
        )
        return f"Display object created: {display}"
    
    if not safe_step(7, "Create display object", step7, 1500):
        return False
    
    # Step 8: Initialize display hardware
    def step8():
        print("    Setting display power...")
        display.set_power(True)
        time.sleep_ms(100)
        print("    Initializing display...")
        display.init()
        time.sleep_ms(200)
        print("    Setting backlight...")
        display.set_backlight(100)
        return "Display hardware initialized"
    
    if not safe_step(8, "Initialize display hardware", step8, 2000):
        return False
    
    # Step 9: Get LVGL objects
    def step9():
        global disp, scr
        disp = lv.display_get_default()
        scr = lv.screen_active()
        return f"LVGL objects: disp={disp}, scr={scr}"
    
    if not safe_step(9, "Get LVGL display and screen", step9, 1000):
        return False
    
    # Step 10: Set background (no refresh yet)
    def step10():
        scr.set_style_bg_color(lv.color_hex(0xFF0000), 0)  # Red for visibility
        return "Red background color set (not refreshed yet)"
    
    if not safe_step(10, "Set background color", step10, 1000):
        return False
    
    # Step 11: Create label (no refresh yet)
    def step11():
        global label
        label = lv.label(scr)
        label.set_text('V2 WORKS!')
        label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)  # White
        label.center()
        return "Label created and configured (not refreshed yet)"
    
    if not safe_step(11, "Create and configure label", step11, 1000):
        return False
    
    print("\n🎉 SUCCESS: All steps completed without refresh!")
    print("UI is created but not yet visible (no refresh called)")
    print("Red background and white 'V2 WORKS!' text should appear when refreshed")
    return True

# Run the smart initialization
try:
    success = run_smart_init_v2()
    if success:
        print("\n=== INITIALIZATION COMPLETE ===")
        print("All steps successful! UI created but not refreshed.")
        print("The display refresh step was skipped to avoid crashes.")
        print("\nTo test refresh manually, try:")
        print("lv.refr_now(disp)")
    else:
        print("\n=== INITIALIZATION FAILED ===")
        print("Check which step failed above.")
        
except Exception as e:
    print(f"\nUNEXPECTED ERROR: {e}")
    import sys
    sys.print_exception(e)
