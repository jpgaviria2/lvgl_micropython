# STEP BY STEP - Recreate exact working sequence
print("=== STEP BY STEP RECREATION ===")
print("Run each step separately in Thonny!")
print()

print("# Step 1: Import lv_start")
print("import lv_start")
print()

print("# Step 2: Run with exact same parameters that worked")
print("display = lv_start.run(spi_hz=5_000_000, bgr=False, swap=True, do_reset=True)")
print()

print("# Step 3: Import LVGL")  
print("import lvgl as lv")
print("import time")
print()

print("# Step 4: Create UI exactly like before")
print("scr = lv.screen_active()")
print("scr.clean()")
print("scr.set_style_bg_color(lv.color_hex(0xFF0000), 0)  # Red")
print()

print("# Step 5: Add label")
print("label = lv.label(scr)")
print("label.set_text('SUCCESS!')")
print("label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)")
print("label.center()")
print()

print("# Step 6: Refresh")
print("lv.refr_now(lv.display_get_default())")
print()

print("# Step 7: Test touch (if display works)")
print("lv_start.test_touch_callback()")
print()

print("Copy each command above and run separately in Thonny!")
print("This recreates your successful test sequence.")
