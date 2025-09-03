# Quick Start Guide - MicroPythonOS on ESP32-S3 Touch LCD 3.5

## 🚀 Get Running in 5 Minutes

### What You Need
- ESP32-S3 Touch LCD 3.5 hardware
- USB-C cable
- Thonny IDE installed
- The `boot.py` and `main.py` files from this project

### Step 1: Flash Base Firmware
1. **Connect your ESP32-S3** to your computer via USB
2. **Open Thonny IDE**
3. **Go to Tools → Options → Interpreter**
4. **Select "MicroPython (ESP32)"**
5. **Select the correct COM port** (usually COM3, COM4, etc.)
6. **Click "Install or update firmware"**
7. **Select "ESP-IDF v1.26 Generic ESP32-S3"**
8. **Click "Install"** and wait for completion

### Step 2: Upload MicroPythonOS Files
1. **In Thonny IDE**, click the "Files" tab
2. **Right-click on the device** (usually shows as "MicroPython device")
3. **Select "Upload to /"**
4. **Upload `boot.py` first**
5. **Then upload `main.py`**

### Step 3: Test the System
1. **Click the "Stop/Restart" button** in Thonny IDE
2. **Check the Shell/REPL** for initialization messages
3. **You should see:**
   ```
   Hardware initialization successful
   Display: 320x480
   Touch: FT6X36 on I2C 0x38
   boot.py finished - ESP32-S3 Touch LCD 3.5 ready
   Starting MicroPythonOS...
   ```

### Step 4: Interact with MicroPythonOS
1. **In the Shell**, you'll see the main menu
2. **Type your choice** (1-5 or 0)
3. **Try option 2** for hardware testing
4. **Use option 1** to see system information

## 🔧 Troubleshooting

### "No module named 'machine'"
- **Solution**: Make sure you selected "MicroPython (ESP32)" not "CircuitPython"
- **Re-flash** the ESP-IDF v1.26 Generic ESP32-S3 firmware

### Hardware not responding
- **Check connections**: Verify all pins are properly connected
- **Power supply**: Ensure stable 5V power supply
- **USB connection**: Try a different USB cable or port

### Touch not working
- **I2C address**: FT6X36 should be at address 0x38
- **Pull-up resistors**: Ensure I2C lines have proper pull-ups
- **Check connections**: Verify SCL=GPIO7, SDA=GPIO8

### Display issues
- **SPI connections**: Verify SCK=GPIO5, MOSI=GPIO1, MISO=GPIO2
- **DC pin**: Ensure LCD_DC=GPIO3 is connected
- **Backlight**: Check LCD_BL=GPIO6 connection

## 📱 What You Get

### MicroPythonOS Features
- **Hardware initialization** for all components
- **Interactive menu system** with hardware testing
- **System information** display
- **Memory management** with garbage collection
- **Error handling** and debugging support

### Hardware Support
- ✅ **ESP32-S3** microcontroller
- ✅ **3.5" TFT LCD** display (ST7796)
- ✅ **Capacitive touch** (FT6X36)
- ✅ **Power management** (AXP2101)
- ✅ **Audio codec** (ES8311)
- ✅ **6-axis IMU** (QMI8658)
- ✅ **Real-time clock** (PCF85063)
- ✅ **SD card** support
- ✅ **Camera** support

## 🎯 Next Steps

### Immediate Improvements
1. **Add graphical UI** with LVGL
2. **Implement touch handling** for interactive interface
3. **Add WiFi configuration**
4. **Create app launcher**

### Advanced Features
1. **Build custom firmware** using the ESP-IDF project
2. **Add more applications**
3. **Implement cloud connectivity**
4. **Add advanced power management**

## 📞 Need Help?

### Check These First
1. **Serial output** in Thonny IDE Shell
2. **Hardware connections** and power supply
3. **Firmware compatibility** (ESP-IDF v1.26 Generic ESP32-S3)

### Common Commands
```python
# Check I2C devices
from machine import I2C, Pin
i2c = I2C(0, scl=Pin(7), sda=Pin(8))
print([hex(addr) for addr in i2c.scan()])

# Check memory
import gc
gc.collect()
print(f"Free: {gc.mem_free()} bytes")

# Check system info
import esp
print(f"Chip: {esp.chip_id()}")
```

## 🎉 Success!

Once you see the MicroPythonOS menu and can interact with it, congratulations! You've successfully:

- ✅ Flashed the correct firmware
- ✅ Initialized all hardware components
- ✅ Launched MicroPythonOS
- ✅ Verified hardware functionality

Your ESP32-S3 Touch LCD 3.5 is now running MicroPythonOS and ready for development!


