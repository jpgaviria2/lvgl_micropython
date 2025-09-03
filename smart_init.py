# SMART INITIALIZATION - With delays and detailed logging
print("=== SMART INITIALIZATION SCRIPT ===")

def safe_step(step_num, description, func, delay_ms=500):
    """Execute a step safely with logging and delay"""
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
        
        # Delay before next step
        time.sleep_ms(delay_ms)
        return True
        
    except Exception as e:
        print(f"✗ Step {step_num} FAILED: {description}")
        print(f"  Error: {e}")
        import sys
        sys.print_exception(e)
        return False

def run_smart_init():
    """Run initialization with smart delays and logging"""
    
    # Step 1: Imports
    def step1():
        global machine, time, gc, lv, lcd_bus, st7796, i2c
        import machine, time, gc
        import lvgl as lv
        import lcd_bus, st7796, i2c
        return "All modules imported"
    
    if not safe_step(1, "Import all modules", step1, 200):
        return False
    
    # Step 2: Initialize LVGL
    def step2():
        gc.collect()
        lv.init()
        return f"LVGL initialized, memory: {gc.mem_free()}"
    
    if not safe_step(2, "Initialize LVGL", step2, 500):
        return False
    
    # Step 3: Hardware reset
    def step3():
        rst_pin = machine.Pin(4, machine.Pin.OUT)
        rst_pin.off()
        time.sleep_ms(10)
        rst_pin.on()
        time.sleep_ms(10)
        return "Hardware reset completed"
    
    if not safe_step(3, "Hardware reset", step3, 300):
        return False
    
    # Step 4: Backlight
    def step4():
        global backlight
        backlight = machine.Pin(6, machine.Pin.OUT)
        backlight.on()
        return "Backlight enabled"
    
    if not safe_step(4, "Enable backlight", step4, 200):
        return False
    
    # Step 5: SPI bus
    def step5():
        global spi_bus
        spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=2, sck=5)
        return f"SPI bus created: {spi_bus}"
    
    if not safe_step(5, "Create SPI bus", step5, 300):
        return False
    
    # Step 6: Display bus
    def step6():
        global display_bus
        display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)
        return f"Display bus created: {display_bus}"
    
    if not safe_step(6, "Create display bus", step6, 300):
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
    
    if not safe_step(7, "Create display object", step7, 500):
        return False
    
    # Step 8: Initialize display hardware
    def step8():
        display.set_power(True)
        display.init()
        display.set_backlight(100)
        return "Display hardware initialized"
    
    if not safe_step(8, "Initialize display hardware", step8, 1000):
        return False
    
    # Step 9: Get LVGL objects
    def step9():
        global disp, scr
        disp = lv.display_get_default()
        scr = lv.screen_active()
        return f"LVGL objects: disp={disp}, scr={scr}"
    
    if not safe_step(9, "Get LVGL display and screen", step9, 300):
        return False
    
    # Step 10: Set background (no refresh yet)
    def step10():
        scr.set_style_bg_color(lv.color_hex(0x00FF00), 0)  # Green
        return "Green background color set (not refreshed yet)"
    
    if not safe_step(10, "Set background color", step10, 200):
        return False
    
    # Step 11: Create label (no refresh yet)
    def step11():
        global label
        label = lv.label(scr)
        label.set_text('SMART INIT!')
        label.set_style_text_color(lv.color_hex(0x000000), 0)  # Black
        label.center()
        return "Label created and configured (not refreshed yet)"
    
    if not safe_step(11, "Create and configure label", step11, 300):
        return False
    
    # Step 12: CRITICAL - Refresh display (this is where crashes happen)
    def step12():
        print("  WARNING: About to refresh display - this may crash!")
        time.sleep_ms(1000)  # Extra delay before critical step
        lv.refr_now(disp)
        return "Display refreshed successfully!"
    
    if not safe_step(12, "Refresh display (CRITICAL STEP)", step12, 1000):
        print("CRASH DETECTED at display refresh!")
        return False
    
    print("🎉 SUCCESS: All steps completed!")
    print("You should see green background with black 'SMART INIT!' text")
    return True

# Run the smart initialization
try:
    success = run_smart_init()
    if success:
        print("\n=== INITIALIZATION COMPLETE ===")
        print("Display is working! Ready for touch integration.")
    else:
        print("\n=== INITIALIZATION FAILED ===")
        print("Check which step failed above.")
        
except Exception as e:
    print(f"\nUNEXPECTED ERROR: {e}")
    import sys
    sys.print_exception(e)
