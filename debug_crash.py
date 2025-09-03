# DEBUG CRASH - Step by step
print("=== DEBUG CRASH ANALYSIS ===")

try:
    print("Step 1: Import lv_start...")
    import lv_start
    print("✓ lv_start imported successfully")
    
    print("Step 2: Check memory before initialization...")
    import gc
    gc.collect()
    print(f"Free memory: {gc.mem_free()} bytes")
    
    print("Step 3: Try to call lv_start.run with minimal parameters...")
    print("WARNING: This is where the crash usually happens!")
    
    # Try with absolute minimal parameters first
    display = lv_start.run()
    print("✓ lv_start.run() completed successfully!")
    
except Exception as e:
    print(f"CRASH DETECTED: {e}")
    import sys
    sys.print_exception(e)
    
    print("\nMemory after crash:")
    import gc
    gc.collect()
    print(f"Free memory: {gc.mem_free()} bytes")
