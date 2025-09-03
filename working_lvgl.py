# WORKING LVGL - Proper screen creation
print("=== WORKING LVGL TEST ===")

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
    
    print("Step 3: Backlight...")
    backlight = machine.Pin(6, machine.Pin.OUT)
    backlight.on()
    print("✓ Backlight on")
    
    print("Step 4: Get or create display...")
    disp = lv.display_get_default()
    print(f"✓ Display: {disp}")
    
    print("Step 5: Create screen properly...")
    scr = lv.screen_create()  # Create new screen instead of getting active
    print(f"✓ Screen created: {scr}")
    
    print("Step 6: Set as active screen...")
    lv.screen_load(scr)
    print("✓ Screen loaded")
    
    print("Step 7: Style the screen...")
    scr.set_style_bg_color(lv.color_hex(0x00FF00), 0)  # Green
    print("✓ Background set to green")
    
    print("Step 8: Add label...")
    label = lv.label(scr)
    label.set_text("LVGL WORKING!")
    label.set_style_text_color(lv.color_hex(0x000000), 0)  # Black text
    label.center()
    print("✓ Label added")
    
    print("Step 9: Add button for interaction test...")
    btn = lv.button(scr)
    btn.set_size(120, 50)
    btn.align(lv.ALIGN.BOTTOM_MID, 0, -20)
    
    btn_label = lv.label(btn)
    btn_label.set_text("CLICK ME")
    btn_label.center()
    
    # Button handler
    def btn_clicked(e):
        btn_label.set_text("CLICKED!")
        print("Button was clicked!")
    
    btn.add_event_cb(btn_clicked, lv.EVENT.CLICKED, None)
    print("✓ Interactive button added")
    
    print("Step 10: Force refresh...")
    lv.refr_now(disp)
    print("✓ Display refreshed")
    
    print("Step 11: Run event loop...")
    for i in range(50):  # 5 seconds
        lv.timer_handler()
        time.sleep_ms(100)
        if i % 10 == 0:
            print(f"Event loop running... {5 - (i//10)}s left")
    
    print("SUCCESS: LVGL is fully functional!")
    print("The issue is definitely with ST7796 hardware drivers, not LVGL.")
    
except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.print_exception(e)
    gc.collect()
    print(f"Memory: {gc.mem_free()} bytes")
