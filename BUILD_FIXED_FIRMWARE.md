# Build Custom ESP32-S3 Firmware with Fixed ST7796 Driver

This guide shows how to build a **permanent firmware solution** with the ST7796 memory allocation bug fixed.

## 🎯 **The Problem**
- **File:** `api_drivers/py_api_drivers/frozen/display/display_driver_framework.py`
- **Line:** 195: `lv.color_format_get_size(color_space)` returns ~800MB instead of 2 bytes
- **Result:** `MemoryError: memory allocation failed, allocating 1601335156 bytes`

## 🔧 **The Solution**
Replace the buggy `lv.color_format_get_size()` call with hardcoded correct values.

---

## 📋 **Prerequisites**

### **System Requirements:**
- **Linux/macOS** (Windows not supported for compilation)
- **Python 3.10+**
- **Git**

### **Install Build Tools:**

**Ubuntu/Linux:**
```bash
sudo apt-get install build-essential cmake ninja-build python3 libusb-1.0-0-dev git
```

**macOS:**
```bash
xcode-select --install
brew install cmake ninja python git
```

---

## 🛠️ **Build Process**

### **Step 1: Fix the Display Framework**

Replace the buggy framework file:

```bash
# Backup original
cp api_drivers/py_api_drivers/frozen/display/display_driver_framework.py \
   api_drivers/py_api_drivers/frozen/display/display_driver_framework.py.backup

# Replace with fixed version
cp fixed_display_driver_framework.py \
   api_drivers/py_api_drivers/frozen/display/display_driver_framework.py
```

### **Step 2: Build ESP32-S3 Firmware**

Build custom firmware with ST7796 driver:

```bash
# Clean any previous builds
python3 make.py esp32 clean

# Build for ESP32-S3 with ST7796 and FT6x36 (your hardware)
python3 make.py esp32 \
    BOARD=ESP32_GENERIC_S3 \
    BOARD_VARIANT=SPIRAM_OCT \
    DISPLAY=st7796 \
    INDEV=ft6x36
```

### **Step 3: Flash the Fixed Firmware**

The compiled firmware will be in `build/` directory:

```bash
# Find your firmware file
ls build/lvgl_micropy_ESP32_GENERIC_S3_*.bin

# Flash to ESP32-S3 (replace COM5 with your port)
esptool.py --chip esp32s3 --port COM5 --baud 460800 write_flash -z 0x0 \
    build/lvgl_micropy_ESP32_GENERIC_S3_SPIRAM_OCT.bin
```

---

## 🎯 **Alternative: TOML Configuration**

Create a custom board configuration for your Waveshare ESP32-S3:

### **Create `waveshare_esp32s3_35.toml`:**

```toml
[mcu]
mcu = "esp32s3"

[mcu.esp32s3]
board = "ESP32_GENERIC_S3"
board_variant = "SPIRAM_OCT"

[display]
display_ic = "st7796"

[display.st7796]
width = 320
height = 480
data_bus_type = "spi"
spi_host = 1
spi_mosi = 1
spi_miso = 2  
spi_sclk = 5
dc_pin = 3
cs_pin = -1
reset_pin = 4
backlight_pin = 6
color_order = "RGB"
swap_xy = true
invert_colors = false

[indev]
indev_ic = "ft6x36"

[indev.ft6x36]
i2c_host = 0
i2c_sda = 8
i2c_scl = 7
i2c_freq = 400000
```

### **Build with TOML:**

```bash
python3 make.py esp32 --toml=waveshare_esp32s3_35.toml
```

---

## ✅ **Expected Results**

After flashing the fixed firmware:

1. **✅ No more memory allocation crashes**
2. **✅ ST7796 display works perfectly** 
3. **✅ FT6x36 touch works correctly**
4. **✅ Your original `lv_start.run()` code works**
5. **✅ MicroPythonOS runs without issues**

---

## 🔍 **Verification**

Test the fixed firmware:

```python
import lv_start
display = lv_start.run(spi_hz=5_000_000, bgr=False, swap=True, do_reset=True)
# Should complete without crashes!

# Test UI
import lvgl as lv
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x0000FF), 0)  # Blue
label = lv.label(scr)
label.set_text("FIXED FIRMWARE!")
label.center()
lv.refr_now(lv.display_get_default())
# Should show blue background with text!
```

---

## 📁 **File Structure After Fix**

```
lvgl_micropython/
├── api_drivers/py_api_drivers/frozen/display/
│   └── display_driver_framework.py  ← FIXED VERSION
├── build/
│   └── lvgl_micropy_ESP32_GENERIC_S3_SPIRAM_OCT.bin  ← YOUR FIRMWARE
└── fixed_display_driver_framework.py  ← BACKUP OF FIX
```

---

## 🎉 **Benefits of Custom Firmware**

✅ **Permanent Fix** - No need to upload override files  
✅ **Better Performance** - Compiled into firmware  
✅ **Clean Solution** - No workarounds needed  
✅ **Future Proof** - Works across device resets  
✅ **Professional** - Production-ready solution  

This approach gives you a **rock-solid, permanent solution** for your ESP32-S3 display system!
