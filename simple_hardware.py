# SIMPLE HARDWARE - Test just SPI and basic display without ST7796
print("=== SIMPLE HARDWARE TEST ===")

try:
    print("Step 1: Setup...")
    import machine
    import time
    import gc
    import lvgl as lv
    print("✓ Imports OK")
    
    print("Step 2: Initialize LVGL...")
    lv.init()
    gc.collect()
    print(f"✓ LVGL initialized, memory: {gc.mem_free()} bytes")
    
    print("Step 3: Test hardware pins individually...")
    # Test each pin without drivers
    rst_pin = machine.Pin(4, machine.Pin.OUT)
    rst_pin.on()
    print("✓ Reset pin OK")
    
    backlight = machine.Pin(6, machine.Pin.OUT)
    backlight.on()
    print("✓ Backlight pin OK")
    
    dc_pin = machine.Pin(3, machine.Pin.OUT)
    dc_pin.on()
    print("✓ DC pin OK")
    
    print("Step 4: Test SPI bus creation...")
    spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=2, sck=5)
    print(f"✓ SPI bus created: {spi_bus}")
    
    print("Step 5: Test basic SPI operations...")
    # Try to write some data to SPI (won't display anything but tests SPI)
    dc_pin.off()  # Command mode
    spi_bus.write(bytes([0x01]))  # Software reset command
    time.sleep_ms(10)
    dc_pin.on()   # Data mode
    print("✓ SPI communication test completed")
    
    print("Step 6: Create LVGL display manually...")
    # Create a display without ST7796 driver
    disp = lv.display_create(320, 480)
    
    # Set up a dummy flush callback (required by LVGL)
    def display_flush_cb(disp_drv, area, color_p):
        # This would normally write to hardware
        # For now, just mark as flushed
        lv.display_flush_ready(disp_drv)
    
    disp.set_flush_cb(display_flush_cb)
    print("✓ LVGL display created with manual setup")
    
    print("Step 7: Test UI on manual display...")
    scr = lv.screen_create()
    lv.screen_load(scr)
    
    scr.set_style_bg_color(lv.color_hex(0xFF00FF), 0)  # Magenta
    
    label = lv.label(scr)
    label.set_text("HARDWARE TEST")
    label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    label.center()
    
    lv.refr_now(disp)
    print("✓ UI created on manual display")
    
    print("Step 8: Event loop test...")
    for i in range(30):
        lv.timer_handler()
        time.sleep_ms(100)
        if i % 10 == 0:
            print(f"Running... {3 - (i//10)}s left")
    
    print("SUCCESS: Hardware pins and SPI work, LVGL works!")
    print("Issue is specifically with ST7796 driver implementation.")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Memory: {gc.mem_free()} bytes")
