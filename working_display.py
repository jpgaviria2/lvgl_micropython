# WORKING DISPLAY - Bypass problematic lv_start.run()
print("=== WORKING DISPLAY INIT ===")

try:
    print("Step 1: Import modules...")
    import machine
    import lvgl as lv
    import lcd_bus
    import st7796
    import time
    import gc
    print("✓ Modules imported")
    
    print("Step 2: Initialize display hardware...")
    # Use exact pins from working lv_start.py
    LCD_MOSI = 1
    LCD_SCLK = 5  
    LCD_DC = 3
    LCD_BL = 6
    
    # Hardware reset
    rst_pin = machine.Pin(4, machine.Pin.OUT)
    rst_pin.off()
    time.sleep_ms(10)
    rst_pin.on()
    time.sleep_ms(10)
    
    # Create SPI and display
    spi_bus = machine.SPI.Bus(host=1, mosi=LCD_MOSI, miso=-1, sck=LCD_SCLK)
    display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=LCD_DC, cs=-1)
    
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
    
    display.init()
    print("✓ Display hardware initialized")
    
    print("Step 3: Create UI (avoiding timer loop)...")
    scr = lv.screen_active()
    scr.set_style_bg_color(lv.color_hex(0x001122), 0)  # Dark blue
    
    # Title
    title = lv.label(scr)
    title.set_text("WORKING DISPLAY!")
    title.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    title.set_style_text_font(lv.font_montserrat_24, 0)
    title.align(lv.ALIGN.TOP_MID, 0, 20)
    
    # Test button
    btn = lv.button(scr)
    btn.set_size(150, 80)
    btn.center()
    btn_label = lv.label(btn)
    btn_label.set_text("TOUCH TEST")
    btn_label.center()
    
    # Counter
    counter = 0
    counter_label = lv.label(scr)
    counter_label.set_text("Touches: 0")
    counter_label.set_style_text_color(lv.color_hex(0x00FF00), 0)
    counter_label.align(lv.ALIGN.BOTTOM_MID, 0, -20)
    
    # Button handler
    def btn_clicked(e):
        global counter
        counter += 1
        counter_label.set_text(f"Touches: {counter}")
        btn_label.set_text(f"HIT {counter}!")
        print(f"Button touched! Count: {counter}")
    
    btn.add_event_cb(btn_clicked, lv.EVENT.CLICKED, None)
    
    print("Step 4: Refresh display (single refresh, no timer loop)...")
    lv.refr_now(lv.display_get_default())
    print("✓ UI created and refreshed!")
    
    print("Step 5: Initialize touch (simplified)...")
    # Import touch controller
    import ft6x36
    
    # Create I2C for touch
    i2c_touch = machine.I2C(0, scl=7, sda=8, freq=400000)
    touch = ft6x36.FT6x36(i2c_touch)
    
    # Simple touch callback
    def touch_read(indev, data):
        touched, x, y = touch.get_positions()
        if touched:
            data.point.x = x
            data.point.y = y  
            data.state = lv.INDEV_STATE.PRESSED
            print(f"Touch: {x}, {y}")
        else:
            data.state = lv.INDEV_STATE.RELEASED
        return False
    
    # Register touch device
    indev = lv.indev_create()
    indev.set_type(lv.INDEV_TYPE.POINTER)
    indev.set_read_cb(touch_read)
    indev.set_display(lv.display_get_default())
    indev.enable(True)
    
    print("✓ Touch initialized!")
    
    print("Step 6: Manual event loop (safe)...")
    print("Touch the button for 10 seconds...")
    for i in range(100):  # 10 seconds
        lv.timer_handler()  # Single call, no sleep
        if i % 25 == 0 and i > 0:
            print(f"{10 - (i//10)}s left")
    
    print(f"✓ Test completed! Final touches: {counter}")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Free memory after error: {gc.mem_free()}")
