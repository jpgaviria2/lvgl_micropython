# MINIMAL DISPLAY INIT - Bypass lv_start.run()
print("=== MINIMAL DISPLAY INIT ===")

try:
    print("Step 1: Import modules...")
    import machine
    import lvgl as lv
    import lcd_bus
    import st7796
    import time
    print("✓ Modules imported")
    
    print("Step 2: Check memory...")
    import gc
    gc.collect()
    print(f"Free memory: {gc.mem_free()} bytes")
    
    print("Step 3: Create SPI bus...")
    # Use the exact pins from lv_start.py on device
    LCD_MOSI = 1
    LCD_SCLK = 5
    LCD_DC = 3
    LCD_BL = 6
    
    spi_bus = machine.SPI.Bus(host=1, mosi=LCD_MOSI, miso=-1, sck=LCD_SCLK)
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=LCD_DC, cs=-1)
    print("✓ SPI bus created")
    
    print("Step 4: Create display...")
    display = st7796.ST7796(
        data_bus=display_bus,
        display_width=320,
        display_height=480,
        backlight_pin=LCD_BL,
        color_space=lv.COLOR_FORMAT.RGB565,
        color_byte_order=st7796.BYTE_ORDER_BGR,
        reset_pin=4,
        reset_state=st7796.STATE_LOW
    )
    print("✓ Display object created")
    
    print("Step 5: Initialize display...")
    display.init()
    print("✓ Display initialized")
    
    print("Step 6: Test simple UI...")
    scr = lv.screen_active()
    scr.set_style_bg_color(lv.color_hex(0x0000FF), 0)  # Blue
    
    label = lv.label(scr)
    label.set_text("MINIMAL INIT OK")
    label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    label.center()
    
    lv.refr_now(lv.display_get_default())
    print("✓ SUCCESS: Minimal initialization working!")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
