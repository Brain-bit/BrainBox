#Importing libraries needed for implementation
import os
import sys
import time
import logging
import dbus
from bluetooth import *

# A class that is responsible for sending data through a bluetooth connection
class Hid:
    # Define the Bluetooth HID PSMs
    PSM_CTRL = 0x11
    PSM_INTR = 0x13

    # define the keyboard service record
    SERVICE_RECORD = """<?xml version="1.0" encoding="UTF-8" ?><record><attribute id="0x0001"><sequence><uuid value="0x1124" /></sequence></attribute>
<attribute id="0x0004"><sequence><sequence><uuid value="0x0100" /><uint16 value="0x0011" /></sequence><sequence><uuid value="0x0011" /></sequence></sequence></attribute>
<attribute id="0x0005"><sequence><uuid value="0x1002" /></sequence></attribute>
<attribute id="0x0006"><sequence><uint16 value="0x656e" /><uint16 value="0x006a" /><uint16 value="0x0100" /></sequence></attribute>
<attribute id="0x0009"><sequence><sequence><uuid value="0x1124" /><uint16 value="0x0100" /></sequence></sequence></attribute>
<attribute id="0x000d"><sequence><sequence><sequence><uuid value="0x0100" /><uint16 value="0x0013" /></sequence><sequence><uuid value="0x0011" /></sequence></sequence></sequence></attribute>
<attribute id="0x0100"><text value="Raspberry Pi Virtual Keyboard" /></attribute><attribute id="0x0101"><text value="USB > BT Keyboard" /></attribute>
<attribute id="0x0102"><text value="PiBoard" /></attribute><attribute id="0x0200"><uint16 value="0x0100" /></attribute>
<attribute id="0x0201"><uint16 value="0x0111" /></attribute><attribute id="0x0202"><uint8 value="0x40" /></attribute>
<attribute id="0x0203"><uint8 value="0x00" /></attribute><attribute id="0x0204"><boolean value="true" /></attribute>
<attribute id="0x0205"><boolean value="true" /></attribute><attribute id="0x0206"><sequence><sequence><uint8 value="0x22" />
<text encoding="hex" value="05010906a101850175019508050719e029e715002501810295017508810395057501050819012905910295017503910395067508150026ff000507190029ff8100c0050c0901a1018503150025017501950b0a23020a21020ab10109b809b609cd09b509e209ea09e9093081029501750d8103c0" />
</sequence></sequence></attribute><attribute id="0x0207"><sequence><sequence><uint16 value="0x0409" /><uint16 value="0x0100" /></sequence></sequence></attribute>
<attribute id="0x020b"><uint16 value="0x0100" /></attribute><attribute id="0x020c"><uint16 value="0x0c80" /></attribute>
<attribute id="0x020d"><boolean value="false" /></attribute><attribute id="0x020e"><boolean value="true" /></attribute>
<attribute id="0x020f"><uint16 value="0x0640" /></attribute><attribute id="0x0210"><uint16 value="0x0320" /></attribute></record>"""

    # Define some HID key codes
    KEY_UP = 82
    KEY_LEFT = 80
    KEY_RIGHT = 79
    KEY_DOWN = 81
    KEY_ENTER = 40
    KEY_ESC = 41
    # Defining some data for the keyboard servive record
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = "/dev/stdout"
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"


    def __init__(self):
        # Requirements for connecting Raspberry Pi to connect as a keyboard to mobile phone
        self.sock_control = None
        self.conn_control = None
        self.conn_interrupt = None
        self.sock_intetrrupt = None
        self.input_report = bytearray([
                0xA1, # Input report
                0x01, # Usage: keyboard
                0x00, # Reserved
                0x00, # Modifier bits
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00 # Keys
        ])
        logging.basicConfig(filename=Hid.LOG_FILE, format=Hid.LOG_FORMAT, level=Hid.LOG_LEVEL)
    # A method binding the bluetooth socket between the Raspberry Pi and mobile
    def connect(self):
        # Create the control and interrupt sockets, and bind and listen
        self.sock_control = BluetoothSocket(L2CAP)
        self.sock_control.bind(("", Hid.PSM_CTRL))
        self.sock_control.listen(1)
        self.sock_interrupt = BluetoothSocket(L2CAP)
        self.sock_interrupt.bind(("", Hid.PSM_INTR))
        self.sock_interrupt.listen(1)
        logging.info("Waiting for a connection...")

        # Accept connections from the host, first the control socket and then the interrupt
        self.conn_control, conn_info = self.sock_control.accept()
        self.conn_interrupt, conn_info = self.sock_interrupt.accept()
        logging.info("PiBoard is connected to %s" % (conn_info[0]))

    # Closing the bluetooth connection 
    def close(self):
        
        self.sock_interrupt.close()
        self.sock_control.close()
        
    # Adding keyboard service record to the Dbus
    def addService(self):
        
        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez", "/"), "org.bluez.Manager")
        adapter_path = manager.DefaultAdapter()
        service = dbus.Interface(bus.get_object("org.bluez", adapter_path), "org.bluez.Service")
        logging.debug("Adding keyboard service record")
        service.AddRecord(Hid.SERVICE_RECORD)

    # A method that sends a key press and release
    def sendKey(self, key, modifiers=None):
        
        # press the key
        self.pressKey(key, modifiers=modifiers)
        # Give the host some time to process; keyboards aren't expected to be fast
        time.sleep(0.01)
        # release the key
        self.releaseKey()
        
    # A method that handles key pressing 
    def pressKey(self, key, modifiers=None):
        
        if (modifiers != None):
            self.input_report[2] = modifiers
        self.input_report[4] = key
        self.conn_interrupt.send(str(self.input_report))
        
    # A method that handles key releasing
    def releaseKey(self):
        
        self.input_report[4] = 0x00
        self.conn_interrupt.send(str(self.input_report))
