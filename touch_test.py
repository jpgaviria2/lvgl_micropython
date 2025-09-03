# SAFE TOUCH TEST
print("=== TOUCH TEST ===")

try:
    print("Step 1: Initialize display...")
    import lv_start
    display = lv_start.run(spi_hz=5_000_000, bgr=False, swap=True, do_reset=True)
    print("✓ Display initialized")
    
    print("Step 2: Create simple UI...")
    import lvgl as lv
    import time
    
    # Get screen and clean it
    scr = lv.screen_active()
    scr.clean()
    scr.set_style_bg_color(lv.color_hex(0x001100), 0)  # Dark green
    
    # Create button
    btn = lv.button(scr)
    btn.set_size(120, 80)
    btn.center()
    btn_label = lv.label(btn)
    btn_label.set_text("TOUCH ME")
    btn_label.center()
    
    # Create counter
    counter = 0
    counter_label = lv.label(scr)
    counter_label.set_text("Count: 0")
    counter_label.set_style_text_color(lv.color_hex(0xFFFF00), 0)
    counter_label.align(lv.ALIGN.BOTTOM_MID, 0, -20)
    
    # Button click handler
    def btn_clicked(e):
        global counter
        counter += 1
        counter_label.set_text(f"Count: {counter}")
        btn_label.set_text(f"HIT {counter}!")
        print(f"Button touched! Count: {counter}")
    
    # Add event callback
    btn.add_event_cb(btn_clicked, lv.EVENT.CLICKED, None)
    
    # Refresh display
    lv.refr_now(lv.display_get_default())
    print("✓ Touch interface ready!")
    print("✓ Touch the green button on screen!")
    
    # Run test loop
    print("Running test for 10 seconds...")
    for i in range(100):  # 10 seconds
        lv.timer_handler()
        time.sleep_ms(100)
        if i % 25 == 0 and i > 0:
            print(f"Test running... {10 - (i//10)} seconds left")
    
    print(f"✓ Touch test completed! Final count: {counter}")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
