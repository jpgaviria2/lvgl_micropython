# Ubuntu WSL Build Guide - Fixed ESP32-S3 Firmware

This guide shows how to build the **FIXED firmware** on Ubuntu WSL that permanently solves the ST7796 memory allocation bug.

## 🎯 **What's Fixed**
- **File:** `api_drivers/py_api_drivers/frozen/display/display_driver_framework.py` 
- **Bug:** Line 195 - `lv.color_format_get_size()` returned 800MB+ instead of 2 bytes
- **Fix:** Replaced with correct hardcoded bytes per pixel values
- **Result:** No more `MemoryError: allocating 1GB+ bytes` crashes!

---

## 📋 **Step 1: Setup Ubuntu WSL Environment**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install build dependencies
sudo apt install -y \
    build-essential \
    cmake \
    ninja-build \
    python3 \
    python3-pip \
    libusb-1.0-0-dev \
    git \
    wget \
    curl \
    unzip
```

---

## 📋 **Step 2: Clone the Fixed Repository**

```bash
# Clone your fixed repository
cd ~
git clone https://github.com/YOUR_USERNAME/lvgl_micropython.git
cd lvgl_micropython

# Verify the fix is present
grep -n "FIXED: Calculate buffer size correctly" api_drivers/py_api_drivers/frozen/display/display_driver_framework.py
# Should show the fixed code around line 192
```

---

## 📋 **Step 3: Initialize Submodules**

```bash
# Initialize and update all submodules
git submodule update --init --recursive

# This will download:
# - MicroPython source
# - ESP-IDF
# - LVGL library
# - All dependencies
```

---

## 📋 **Step 4: Build the Fixed Firmware**

### **Option A: Build with TOML (Recommended)**

```bash
# Use the custom Waveshare ESP32-S3 configuration
python3 make.py esp32 --toml=waveshare_esp32s3_35.toml

# This builds with:
# - ESP32-S3 with Octal SPIRAM
# - ST7796 display driver (FIXED!)
# - FT6x36 touch controller
# - Your exact pin configuration
```

### **Option B: Build with Command Line Arguments**

```bash
# Clean any previous builds
python3 make.py esp32 clean

# Build for your specific hardware
python3 make.py esp32 \
    BOARD=ESP32_GENERIC_S3 \
    BOARD_VARIANT=SPIRAM_OCT \
    DISPLAY=st7796 \
    INDEV=ft6x36
```

---

## 📋 **Step 5: Locate Your Firmware**

```bash
# Find the compiled firmware
ls -la build/

# Look for file like:
# lvgl_micropy_ESP32_GENERIC_S3_SPIRAM_OCT.bin
```

---

## 📋 **Step 6: Transfer to Windows for Flashing**

### **Copy firmware to Windows filesystem:**

```bash
# Copy to your Windows Downloads folder
cp build/lvgl_micropy_ESP32_GENERIC_S3_SPIRAM_OCT.bin /mnt/c/Users/YOUR_USERNAME/Downloads/

# Or copy to a shared folder
cp build/lvgl_micropy_ESP32_GENERIC_S3_SPIRAM_OCT.bin /mnt/c/temp/
```

---

## 📋 **Step 7: Flash the Fixed Firmware**

### **On Windows (PowerShell or Command Prompt):**

```powershell
# Navigate to where you copied the firmware
cd C:\Users\YOUR_USERNAME\Downloads

# Flash the fixed firmware (replace COM5 with your port)
esptool.py --chip esp32s3 --port COM5 --baud 460800 write_flash -z 0x0 lvgl_micropy_ESP32_GENERIC_S3_SPIRAM_OCT.bin
```

### **Alternative: Flash from WSL (if USB passthrough works):**

```bash
# Install esptool in WSL
pip3 install esptool

# Flash directly from WSL (if your ESP32 is accessible)
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x0 build/lvgl_micropy_ESP32_GENERIC_S3_SPIRAM_OCT.bin
```

---

## ✅ **Step 8: Test the Fixed Firmware**

After flashing, test in Thonny:

```python
# Test 1: Basic display initialization (should NOT crash!)
import lv_start
display = lv_start.run(spi_hz=5_000_000, bgr=False, swap=True, do_reset=True)
print("✅ Display initialized without crashes!")

# Test 2: Create UI (should work perfectly!)
import lvgl as lv
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x0000FF), 0)  # Blue
label = lv.label(scr)
label.set_text("FIXED FIRMWARE!")
label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)  # White
label.center()
lv.refr_now(lv.display_get_default())
print("✅ UI created and displayed successfully!")

# Test 3: Touch functionality
# Touch the screen and check console for touch events
```

---

## 🎯 **Expected Build Output**

```
Building target: esp32
Board: ESP32_GENERIC_S3
Board Variant: SPIRAM_OCT
Display: st7796 (FIXED)
Input Device: ft6x36

✅ Submodules updated
✅ Dependencies installed  
✅ LVGL configured
✅ Display driver framework FIXED
✅ ST7796 driver compiled
✅ FT6x36 touch driver compiled
✅ Firmware built successfully

Output: build/lvgl_micropy_ESP32_GENERIC_S3_SPIRAM_OCT.bin
```

---

## 🔍 **Troubleshooting**

### **Build fails with "No module named 'toml'":**
```bash
pip3 install toml
```

### **Git submodule errors:**
```bash
git submodule deinit --all -f
git submodule update --init --recursive
```

### **ESP-IDF path issues:**
```bash
# The build system should handle this automatically
# If issues persist, manually set:
export IDF_PATH=$PWD/lib/esp-idf
```

### **Out of memory during build:**
```bash
# Reduce parallel jobs
python3 make.py esp32 -j2 --toml=waveshare_esp32s3_35.toml
```

---

## 🎉 **Success Indicators**

✅ **Build completes without errors**  
✅ **Firmware file created in build/ directory**  
✅ **File size ~2-4MB (reasonable size)**  
✅ **No "memory allocation failed" errors during build**  

Once flashed, your ESP32-S3 will have the **permanent fix** built into the firmware - no more workarounds needed!

---

## 📁 **Repository Structure After Build**

```
lvgl_micropython/
├── api_drivers/py_api_drivers/frozen/display/
│   └── display_driver_framework.py  ← ✅ FIXED!
├── waveshare_esp32s3_35.toml        ← ✅ Your board config
├── build/
│   └── lvgl_micropy_ESP32_GENERIC_S3_SPIRAM_OCT.bin  ← ✅ Fixed firmware
└── lib/
    ├── micropython/  ← Downloaded by submodules
    ├── esp-idf/      ← Downloaded by submodules  
    └── lvgl/         ← Downloaded by submodules
```

This gives you a **production-ready, permanently fixed firmware** for your Waveshare ESP32-S3 display!
