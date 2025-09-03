# EXACT REPLICA - Copy exact parameters from working lv_start.py
print("=== EXACT REPLICA TEST ===")

try:
    print("Step 1: Setup exactly like lv_start.py...")
    import machine
    import time
    import gc
    import lvgl as lv
    import lcd_bus
    import st7796
    print("✓ Imports OK")
    
    # Exact same constants from lv_start.py
    LCD_SCLK = 5
    LCD_MOSI = 1
    LCD_MISO = 2
    LCD_DC = 3
    LCD_CS = -1
    LCD_BL = 6
    
    print("Step 2: Hardware reset (exact copy)...")
    if True:  # do_reset parameter
        rst_pin = machine.Pin(4, machine.Pin.OUT)
        rst_pin.off()
        time.sleep_ms(10)
        rst_pin.on()
        time.sleep_ms(10)
    print("✓ Reset OK")
    
    print("Step 3: Create buses (exact parameters)...")
    spi_bus = machine.SPI.Bus(host=1, mosi=LCD_MOSI, miso=LCD_MISO, sck=LCD_SCLK)
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=LCD_DC, cs=LCD_CS)
    print("✓ Buses created")
    
    print("Step 4: Create display (EXACT parameters from lv_start.py)...")
    # Exact parameters from working lv_start.py
    bgr = False
    swap = True
    color_order = st7796.BYTE_ORDER_BGR if bgr else st7796.BYTE_ORDER_RGB
    
    display = st7796.ST7796(
        data_bus=display_bus,
        display_width=320,
        display_height=480,
        backlight_pin=LCD_BL,
        color_space=lv.COLOR_FORMAT.RGB565,
        color_byte_order=color_order,
        rgb565_byte_swap=bool(swap),  # This was missing!
    )
    print("✓ Display object created with exact parameters!")
    
    print("Step 5: Initialize...")
    display.init()
    print("✓ Display initialized")
    
    print("Step 6: Test LVGL...")
    scr = lv.screen_active()
    scr.set_style_bg_color(lv.color_hex(0x0000FF), 0)  # Blue
    
    label = lv.label(scr)
    label.set_text("EXACT REPLICA!")
    label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    label.center()
    
    lv.refr_now(lv.display_get_default())
    print("✓ Should see blue background with white text!")
    
    print("SUCCESS: Exact replica working!")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Memory: {gc.mem_free()} bytes")
