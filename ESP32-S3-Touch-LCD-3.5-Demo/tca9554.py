# TCA9554 I/O Expander helper (MicroPython)
# Supports basic pin direction/output on port 1 and LCD reset sequence used in 01_factory

from machine import I2C
import time

# Default address for TCA9554
TCA9554_DEFAULT_ADDR = 0x20

# TCA9554 register map (single 8-bit port)
INPUT_PORT    = 0x00
OUTPUT_PORT   = 0x01
POLARITY_INV  = 0x02
CONFIG        = 0x03  # 1=input, 0=output

class TCA9554:
    def __init__(self, i2c: I2C, addr: int = TCA9554_DEFAULT_ADDR) -> None:
        self.i2c = i2c
        self.addr = addr
        # Detect if device behaves like TCA9555 (dual-port) or TCA9554 (single-port)
        self.is_dual_port = False
        try:
            # Try reading CONFIG of port 1 (0x07). If succeeds, treat as dual-port
            _ = self.i2c.readfrom_mem(self.addr, 0x07, 1)
            self.is_dual_port = True
        except Exception:
            self.is_dual_port = False

    def begin(self) -> bool:
        try:
            return self.addr in self.i2c.scan()
        except Exception:
            return False

    def read_u8(self, reg: int) -> int:
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def write_u8(self, reg: int, value: int) -> None:
        self.i2c.writeto_mem(self.addr, reg, bytes([value & 0xFF]))

    def pinMode1(self, pin_index: int, is_output: bool) -> None:
        # Keep API name for compatibility with Arduino example semantics
        if self.is_dual_port:
            # TCA9555: use CONFIG port 1 at 0x07
            cfg = self.i2c.readfrom_mem(self.addr, 0x07, 1)[0]
            if is_output:
                cfg &= ~(1 << pin_index)
            else:
                cfg |= (1 << pin_index)
            self.i2c.writeto_mem(self.addr, 0x07, bytes([cfg]))
        else:
            # TCA9554: single CONFIG at 0x03
            cfg = self.read_u8(CONFIG)
            if is_output:
                cfg &= ~(1 << pin_index)
            else:
                cfg |= (1 << pin_index)
            self.write_u8(CONFIG, cfg)

    def write1(self, pin_index: int, level: int) -> None:
        if self.is_dual_port:
            # TCA9555: output port 1 at 0x03
            outv = self.i2c.readfrom_mem(self.addr, 0x03, 1)[0]
            if level:
                outv |= (1 << pin_index)
            else:
                outv &= ~(1 << pin_index)
            self.i2c.writeto_mem(self.addr, 0x03, bytes([outv]))
        else:
            outv = self.read_u8(OUTPUT_PORT)
            if level:
                outv |= (1 << pin_index)
            else:
                outv &= ~(1 << pin_index)
            self.write_u8(OUTPUT_PORT, outv)

    # Convenience: perform LCD reset on Port1.Pin1 as in 01_factory Arduino example
    def lcd_reset_pin1(self) -> None:
        # Ensure pin1 is output
        self.pinMode1(1, True)
        # Sequence: HIGH -> 10ms -> LOW -> 10ms -> HIGH -> 200ms
        self.write1(1, 1)
        time.sleep_ms(10)
        self.write1(1, 0)
        time.sleep_ms(10)
        self.write1(1, 1)
        time.sleep_ms(200)

# One-shot helper
def reset_lcd_via_tca9554(i2c: I2C, addr: int = TCA9554_DEFAULT_ADDR) -> bool:
    try:
        tca = TCA9554(i2c, addr)
        if not tca.begin():
            return False
        tca.lcd_reset_pin1()
        return True
    except Exception:
        return False
