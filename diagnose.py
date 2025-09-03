# DIAGNOSE - Check device state
print("=== DEVICE DIAGNOSIS ===")

try:
    print("Step 1: Memory check...")
    import gc
    gc.collect()
    print(f"Free memory: {gc.mem_free()} bytes")
    
    print("Step 2: Check if lv_start exists...")
    try:
        import lv_start
        print("✓ lv_start imports OK")
        
        # Check if functions exist
        print(f"Has run function: {hasattr(lv_start, 'run')}")
        print(f"Has test_touch_callback: {hasattr(lv_start, 'test_touch_callback')}")
        
    except Exception as e:
        print(f"✗ lv_start import failed: {e}")
    
    print("Step 3: Check LVGL...")
    try:
        import lvgl as lv
        print("✓ LVGL imports OK")
        print(f"LVGL version available: {hasattr(lv, 'init')}")
    except Exception as e:
        print(f"✗ LVGL import failed: {e}")
    
    print("Step 4: Check hardware modules...")
    try:
        import machine
        import time
        print("✓ Hardware modules OK")
        
        # Test basic pin
        pin = machine.Pin(6, machine.Pin.OUT)
        pin.on()
        print("✓ Pin control works")
        
    except Exception as e:
        print(f"✗ Hardware test failed: {e}")
    
    print("Step 5: Check display modules...")
    try:
        import lcd_bus
        import st7796
        print("✓ Display modules import OK")
    except Exception as e:
        print(f"✗ Display modules failed: {e}")
    
    print("DIAGNOSIS COMPLETE")
    print("If all steps pass, the issue is in lv_start.run() execution")
    print("If any step fails, we have a deeper module issue")
    
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import sys
    sys.print_exception(e)
