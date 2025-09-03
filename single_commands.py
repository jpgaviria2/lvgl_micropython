# SINGLE COMMANDS - Run ONE command at a time
print("=== SINGLE COMMAND APPROACH ===")
print("Run ONLY ONE command at a time in Thonny:")
print()

print("# 1. Import everything first:")
print("import machine, time, gc, lvgl as lv, lcd_bus, st7796, i2c")
print()

print("# 2. Initialize LVGL:")
print("gc.collect(); lv.init()")
print()

print("# 3. Hardware reset:")
print("rst_pin = machine.Pin(4, machine.Pin.OUT); rst_pin.off(); time.sleep_ms(10); rst_pin.on(); time.sleep_ms(10)")
print()

print("# 4. Backlight:")
print("backlight = machine.Pin(6, machine.Pin.OUT); backlight.on()")
print()

print("# 5. SPI bus:")
print("spi_bus = machine.SPI.Bus(host=1, mosi=1, miso=2, sck=5)")
print()

print("# 6. Display bus:")
print("display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=5_000_000, dc=3, cs=-1)")
print()

print("# 7. Create display:")
print("display = st7796.ST7796(data_bus=display_bus, display_width=320, display_height=480, backlight_pin=6, color_space=lv.COLOR_FORMAT.RGB565, color_byte_order=st7796.BYTE_ORDER_RGB, rgb565_byte_swap=True)")
print()

print("# 8. Initialize display:")
print("display.set_power(True); display.init(); display.set_backlight(100); print('Display ready!')")
print()

print("# 9. Get display and screen:")
print("disp = lv.display_get_default(); scr = lv.screen_active(); print(f'Screen: {scr}')")
print()

print("# 10. Set background (SINGLE operation):")
print("scr.set_style_bg_color(lv.color_hex(0x00FF00), 0); print('Green background set')")
print()

print("# 11. Refresh display:")
print("lv.refr_now(disp); print('Display refreshed - should see green!')")
print()

print("# 12. Create label (SINGLE operation):")
print("label = lv.label(scr); print('Label created')")
print()

print("# 13. Set label text:")
print("label.set_text('SUCCESS!'); print('Text set')")
print()

print("# 14. Set label color:")
print("label.set_style_text_color(lv.color_hex(0x000000), 0); print('Color set')")
print()

print("# 15. Center label:")
print("label.center(); print('Label centered')")
print()

print("# 16. Final refresh:")
print("lv.refr_now(disp); print('Final refresh - should see text!')")
print()

print("# 17. Test touch I2C:")
print("touch_bus = i2c.I2C.Bus(host=0, scl=7, sda=8, freq=400000, use_locks=False); touch_dev = i2c.I2C.Device(bus=touch_bus, dev_id=0x38, reg_bits=8); print('Touch ready')")
print()

print("# 18. Test touch reading:")
print("try: touch_data = touch_dev.read_mem(0x02, 1)[0]; print(f'Touch status: {touch_data}')\\nexcept Exception as e: print(f'Touch error: {e}')")
print()

print("=== RUN EACH COMMAND SEPARATELY ===")
print("Wait for each command to complete before running the next one.")
