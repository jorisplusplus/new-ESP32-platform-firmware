from ubluetooth import BLE
from micropython import const
_IRQ_SCAN_RESULT                     = const(5)
_IRQ_SCAN_COMPLETE                   = const(6)

def bt_irq(event, data):
    if event == _IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, connectable, rssi, adv_data = data
        print(addr_type, addr, adv_data)
    elif event == _IRQ_SCAN_COMPLETE:
        # Scan duration finished or manually stopped.
        print('scan complete')
    else:
        print('Other event type', event, data)

ble = BLE()
ble.active(True)
ble.irq(handler=bt_irq)

# Scan for 10s (at 100% duty cycle)
ble.gap_scan(10000)