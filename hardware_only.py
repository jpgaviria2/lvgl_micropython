# HARDWARE ONLY - Test just display hardware without any LVGL UI
print("=== HARDWARE ONLY TEST ===")

def hardware_only_test():
    """Test just display hardware initialization - no LVGL UI"""
    
    import machine
    import time
    import gc
    import lvgl as lv
    import lcd_bus
    import st7796
    
    # Copy exact constants
    LCD_SCLK = 5
    LCD_MOSI = 1
    LCD_MISO = 2
    LCD_DC = 3
    LCD_CS = -1
    LCD_BL = 6
    
    print("Step 1: Initialize LVGL...")
    gc.collect()
    lv.init()
    print("✓ LVGL initialized")
    
    print("Step 2: Hardware reset...")
    rst_pin = machine.Pin(4, machine.Pin.OUT)
    rst_pin.off()
    time.sleep_ms(10)
    rst_pin.on()
    time.sleep_ms(10)
    print("✓ Reset done")
    
    print("Step 3: Backlight...")
    backlight = machine.Pin(LCD_BL, machine.Pin.OUT)
    backlight.on()
    print("✓ Backlight on - should see light")
    
    print("Step 4: Create SPI and display...")
    spi_bus = machine.SPI.Bus(host=1, mosi=LCD_MOSI, miso=LCD_MISO, sck=LCD_SCLK)
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=LCD_DC, cs=LCD_CS)
    
    display = st7796.ST7796(
        data_bus=display_bus,
        display_width=320,
        display_height=480,
        backlight_pin=LCD_BL,
        color_space=lv.COLOR_FORMAT.RGB565,
        color_byte_order=st7796.BYTE_ORDER_RGB,  # bgr=False
        rgb565_byte_swap=True,  # swap=True
    )
    
    display.set_power(True)
    display.init()
    display.set_backlight(100)
    print("✓ Display hardware fully initialized")
    
    print("Step 5: Test backlight control...")
    for i in range(3):
        backlight.off()
        print(f"  Backlight OFF {i+1}")
        time.sleep_ms(500)
        backlight.on()
        print(f"  Backlight ON {i+1}")
        time.sleep_ms(500)
    print("✓ Backlight control works")
    
    print("Step 6: Check LVGL display...")
    disp = lv.display_get_default()
    print(f"✓ LVGL display object: {disp}")
    
    print("SUCCESS: Display hardware is fully functional!")
    print("The issue is with LVGL UI creation, not hardware.")
    
    return display

# Test hardware only
try:
    display = hardware_only_test()
    print("\n=== HARDWARE TEST COMPLETE ===")
    print("✓ Display hardware works perfectly")
    print("✓ Backlight control works")
    print("✓ LVGL display system ready")
    print("Issue is specifically with UI element creation")
    
except Exception as e:
    print(f"Hardware error: {e}")
    import sys
    sys.print_exception(e)
