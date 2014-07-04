# Uncomment the next two lines if you want to save the animation
#import matplotlib
#matplotlib.use("Agg")

import numpy
import math
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation


"""\
This module provides the EPOC class for accessing Emotiv EPOC
EEG headsets.
"""

import os

from Crypto.Cipher import AES

import usb.core
import usb.util

import numpy as np

import utils


class EPOCError(Exception):
    """Base class for exceptions in this module."""
    pass


class EPOCTurnedOffError(EPOCError):
    """Exception raised when Emotiv EPOC is not turned on."""
    pass


class EPOCDeviceNodeNotFoundError(EPOCError):
    """Exception raised when /dev/emotiv_epoc is missing."""
    pass


class EPOCUSBError(EPOCError):
    """Exception raised when error occurs during I/O operations."""
    pass


class EPOCNotPluggedError(EPOCError):
    """Exception raised when EPOC dongle cannot be detected."""
    pass


class EPOCPermissionError(EPOCError):
    """Exception raised when EPOC dongle cannot be opened for I/O."""
    pass


class EPOC(object):
    """Class for accessing Emotiv EPOC headset devices."""

    # Device descriptions for USB
    INTERFACE_DESC = "Emotiv RAW DATA"
    MANUFACTURER_DESC = "Emotiv Systems Pty Ltd"

    # Channel names
    channels = ["F3", "FC5", "AF3", "F7", "T7", "P7", "O1",
                "O2", "P8",  "T8",  "F8", "AF4", "FC6", "F4"]

    # Sampling rate: 128Hz (Internal: 2048Hz)
    sampling_rate = 128

    # Vertical resolution interval (0.51uV)
    vres = 0.51

    # Battery levels
    # github.com/openyou/emokit/blob/master/doc/emotiv_protocol.asciidoc
    battery_levels = {247: 99, 246: 97, 245: 93, 244: 89, 243: 85,
                      242: 82, 241: 77, 240: 72, 239: 66, 238: 62,
                      237: 55, 236: 46, 235: 32, 234: 20, 233: 12,
                      232: 6, 231: 4, 230: 3, 229: 2, 228: 1,
                      227: 1, 226: 1,
                      }
    # 100% for bit values between 248-255
    battery_levels.update(dict([(k, 100) for k in range(248, 256)]))
    # 0% for bit values between 128-225
    battery_levels.update(dict([(k, 0) for k in range(128, 226)]))

    # Define a contact quality ordering
    #   github.com/openyou/emokit/blob/master/doc/emotiv_protocol.asciidoc

    # For counter values between 0-15
    cq_order = ["F3", "FC5", "AF3", "F7", "T7",  "P7",  "O1",
                "O2", "P8",  "T8",  "F8", "AF4", "FC6", "F4",
                "F8", "AF4"]

    # 16-63 is currently unknown
    cq_order.extend([None, ] * 48)

    # Now the first 16 values repeat once more and ends with 'FC6'
    cq_order.extend(cq_order[:16])
    cq_order.append("FC6")

    # Finally pattern 77-80 repeats until 127
    cq_order.extend(cq_order[-4:] * 12)

    # emokit-style bit indexes to use with utils.get_level()
    bit_indexes = {
        'F3': [10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
        'FC5': [28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9],
        'AF3': [46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27],
        'F7': [48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45],
        'T7': [66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63],
        'P7': [84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65],
        'O1': [102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83],
        'O2': [140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121],
        'P8': [158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139],
        'T8': [160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157],
        'F8': [178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175],
        'AF4': [196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177],
        'FC6': [214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195],
        'F4': [216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213],
        'QU': [99,100,101,102,103,104,105,106,107,108,109,110,111,112],
    }

    def __init__(self, method="libusb", serial_number=None, enable_gyro=True):
        self.vendor_id = None
        self.product_id = None
        self.decryption = None
        self.decryption_key = None
        self.headset_on = False
        self.enable_gyro = enable_gyro
        self.battery = 0
        self.counter = 0
        self.gyroX = 0
        self.gyroY = 0

        # Access method can be direct/libusb/dummy (Default: libusb)
        # If dummy is given the class behaves as a random signal generator
        self.method = method

        # One may like to specify the dongle with its serial
        self.serial_number = serial_number

        # libusb device and endpoint
        self.device = None
        self.endpoint = None

        # By default acquire from all channels
        self.channel_mask = self.channels

        # Dict for storing contact qualities
        self.quality = {
            "F3": 0, "FC5": 0, "AF3": 0, "F7": 0,
            "T7": 0, "P7": 0, "O1": 0, "O2": 0,
            "P8": 0, "T8": 0, "F8": 0, "AF4": 0,
            "FC6": 0, "F4": 0,
        }

        # Update __dict__ with convenience attributes for channels
        self.__dict__.update(dict((v, k) for k, v in enumerate(self.channels)))

        # Enumerate the bus to find EPOC devices
        self.enumerate()

    def _is_epoc(self, device):
        """Custom match function for libusb."""
        try:
            manu = usb.util.get_string(device, len(self.MANUFACTURER_DESC),
                                       device.iManufacturer)
        except usb.core.USBError, usb_exception:
            # If the udev rule is installed, we shouldn't get an exception
            # for Emotiv device.
            return False
        else:
            if manu == self.MANUFACTURER_DESC:
                # Found a dongle, check for interface class 3
                for interf in device.get_active_configuration():
                    if_str = usb.util.get_string(
                        device, len(self.INTERFACE_DESC),
                        interf.iInterface)
                    if if_str == self.INTERFACE_DESC:
                        return True

    def set_channel_mask(self, channel_mask):
        """Set channels from which to acquire."""
        self.channel_mask = channel_mask

    def enumerate(self):
        """Traverse through USB bus and enumerate EPOC devices."""
        if self.method == "dummy":
            self.endpoint = open("/dev/urandom")
            self.get_sample = self.__get_sample_dummy
            return

        devices = usb.core.find(find_all=True, custom_match=self._is_epoc)

        if not devices:
            raise EPOCNotPluggedError("Emotiv EPOC not found.")

        for dev in devices:
            serial = usb.util.get_string(dev, 32, dev.iSerialNumber)
            if self.serial_number and self.serial_number != serial:
                # If a special S/N is given, look for it.
                continue

            # Record some attributes
            self.serial_number = serial
            self.vendor_id = "%X" % dev.idVendor
            self.product_id = "%X" % dev.idProduct

            if self.method == "libusb":
                # Last interface is the one we need
                for interface in dev.get_active_configuration():
                    if dev.is_kernel_driver_active(interface.bInterfaceNumber):
                        # Detach kernel drivers and claim through libusb
                        dev.detach_kernel_driver(interface.bInterfaceNumber)
                        usb.util.claim_interface(dev, interface.bInterfaceNumber)

                self.device = dev
                self.endpoint = usb.util.find_descriptor(
                    interface, bEndpointAddress=usb.ENDPOINT_IN | 2)
            elif self.method == "direct":
                if os.path.exists("/dev/emotiv_epoc"):
                    self.endpoint = open("/dev/emotiv_epoc")
                else:
                    raise EPOCDeviceNodeNotFoundError(
                        "/dev/emotiv_epoc doesn't exist.")

            # Return the first Emotiv headset by default
            break

        self.setup_encryption()
        # Attempt to see whether the headset is turned on
        try:
            self.endpoint.read(32, 100)
        except usb.USBError as ue:
            if ue.errno == 110:
                self.headset_on = False
                print "Setup is OK but make sure that headset is turned on."
        else:
            self.headset_on = True

    def setup_encryption(self, research=True):
        """Generate the encryption key and setup Crypto module.
        The key is based on the serial number of the device and the
        information whether it is a research or consumer device.
        """
        if research:
            self.decryption_key = ''.join([self.serial_number[15], '\x00',
                                           self.serial_number[14], '\x54',
                                           self.serial_number[13], '\x10',
                                           self.serial_number[12], '\x42',
                                           self.serial_number[15], '\x00',
                                           self.serial_number[14], '\x48',
                                           self.serial_number[13], '\x00',
                                           self.serial_number[12], '\x50'])
        else:
            self.decryption_key = ''.join([self.serial_number[15], '\x00',
                                           self.serial_number[14], '\x48',
                                           self.serial_number[13], '\x00',
                                           self.serial_number[12], '\x54',
                                           self.serial_number[15], '\x10',
                                           self.serial_number[14], '\x42',
                                           self.serial_number[13], '\x00',
                                           self.serial_number[12], '\x50'])

        self._cipher = AES.new(self.decryption_key)

    def set_external_decryption(self):
        """Use another process for concurrent decryption."""
        self.decryption = Process(target=decryptionProcess,
                                  args=[self._cipher,
                                        self.input_queue,
                                        self.output_queue, False])
        self.decryption.daemon = True
        self.decryption.start()

    def __get_sample_dummy(self):
        """Read random dummy samples."""
        raw_data = self.endpoint.read(32)
        return [utils.get_level(raw_data, self.bit_indexes[n]) for n in self.channel_mask]

    def get_sample(self):
        """Returns an array of EEG samples."""
        try:
            raw_data = self._cipher.decrypt(self.endpoint.read(32))
            # Parse counter
            ctr = ord(raw_data[0])
            # Update gyro's if requested
            if self.enable_gyro:
                self.gyroX = ((ord(raw_data[29]) << 4) | (ord(raw_data[31]) >> 4))
                self.gyroY = ((ord(raw_data[30]) << 4) | (ord(raw_data[31]) & 0x0F))
            if ctr < 128:
                self.counter = ctr
                # Contact qualities
                if self.cq_order[ctr]:
                    self.quality[self.cq_order[ctr]] = utils.get_level(raw_data, self.bit_indexes["QU"]) / 540.0
                # Finally EEG data
                return [0.51 * utils.get_level(raw_data, self.bit_indexes[n]) for n in self.channel_mask]
            else:
                # Set a synthetic counter for this special packet: 128
                self.counter = 128
                # Parse battery level
                self.battery = self.battery_levels[ctr]
                return []
        except usb.USBError as usb_exception:
            if usb_exception.errno == 110:
                self.headset_on = False
                raise EPOCTurnedOffError(
                        "Make sure that headset is turned on")
            else:
                raise EPOCUSBError("USB I/O error with errno = %d" %
                        usb_exception.errno)

    def acquire_data(self, duration):
        """Acquire data from the EPOC headset."""

        total_samples = duration * self.sampling_rate
        _buffer = np.ndarray((total_samples, len(self.channel_mask) + 1),
                dtype=np.uint16)
        ctr = 0
        while ctr < total_samples:
            # Fetch new data
            data = self.get_sample()
            if data:
                # Prepend sequence numbers
                _buffer[ctr] = np.insert(np.array(data), 0, self.counter)
                ctr += 1

        return _buffer

    def acquire_data_fast(self, duration, stop_callback=None, stop_callback_param=None):
        """A more optimized method to acquire data from the EPOC headset without calling get_sample()."""

        def get_level(raw_data, bits):
            """Returns signal level from raw_data frame."""
            level = 0
            for i in range(13, -1, -1):
                level <<= 1
                b, o = (bits[i] / 8) + 1, bits[i] % 8
                level |= (ord(raw_data[b]) >> o) & 1
            # Return level in uV (microVolts)
            return level

        bit_indexes = [self.bit_indexes[n] for n in self.channel_mask]
        # Packet idx to keep track of losses
        idx = []
        total_samples = duration * self.sampling_rate

        # Pre-allocated array
        _buffer = np.ndarray((total_samples, len(self.channel_mask)), dtype=np.float64)

        # Acquire in one read, this should be more robust against drops
        raw_data = self._cipher.decrypt(self.endpoint.read(32 * (total_samples + duration + 1), timeout=(duration+1)*1000))

        if stop_callback and stop_callback_param:
            stop_callback(stop_callback_param)

        # Split data back into 32-byte chunks, skipping 1st packet
        split_data = [raw_data[i:i + 32] for i in range(32, len(raw_data), 32)]

        # Loop ctr
        c = 0
        for block in split_data:
            if c == total_samples:
                break
            # Parse counter
            ctr = ord(block[0])
            # Skip battery
            if ctr < 128:
                idx.append(ctr)
                _buffer[c] = [0.51 * get_level(block, bi) for bi in bit_indexes]
                c += 1
                # Update qualities as well
                if self.cq_order[ctr] is not None:
                    self.quality[self.cq_order[ctr]] = utils.get_level(block, self.bit_indexes["QU"]) / 540.0
            else:
                # Parse battery level
                self.battery = self.battery_levels[ctr]

        return idx, _buffer

    def get_quality(self, electrode):
        "Return contact quality for the specified electrode."""
        return self.quality.get(electrode, None)

    def disconnect(self):
        """Release the claimed interface."""
        if self.method == "libusb":
            for interf in self.device.get_active_configuration():
                usb.util.release_interface(
                    self.device, interf.bInterfaceNumber)
        else:
            self.endpoint.close()

"""
def main():

    e = EPOC()

    while 1:
        try:
            data = e.get_sample()
            # data is [] for each battery packet, e.g. ctr > 127
            if data:
                # Clear screen
                print("\x1b[2J\x1b[H")
                header = "Emotiv Data Packet [%3d/128] [Loss: N/A] [Battery: %2d(%%)]" % (
                    e.counter, e.battery)
                print "%s\n%s" % (header, '-'*len(header))

                print "%10s: %5d" % ("Gyro(x)", e.gyroX)
                print "%10s: %5d" % ("Gyro(y)", e.gyroY)

                for i,channel in enumerate(e.channel_mask):
                    print "%10s: %.2f %20s: %.2f" % (channel, data[i], "Quality", e.quality[channel])
        except EPOCTurnedOffError, ete:
            print ete
        except KeyboardInterrupt, ki:
            e.disconnect()
            return 0

"""
# Sent for figure
font = {'size'   : 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0 = figure(num = 0, figsize = (20, 8))#, dpi = 100)
f0.suptitle("EEG Datum", fontsize=12)
ax01 = subplot2grid((1, 1), (0, 0))

#tight_layout()

# Set titles of subplots
ax01.set_title('Applitude vs Time')

# set y-limits
ax01.set_ylim(0,3000)


# sex x-limits
ax01.set_xlim(0,5.0)


# Turn on grids
ax01.grid(True)


# set label names
ax01.set_xlabel("x")
ax01.set_ylabel("py")


# Data Placeholders
f3=zeros(0)
fc5=zeros(0)
af3=zeros(0)
f7=zeros(0)
t7=zeros(0)
p7=zeros(0)
s01=zeros(0)
s02=zeros(0)
p8=zeros(0)
t8=zeros(0)
f8=zeros(0)
af4=zeros(0)
fc6=zeros(0)
f4=zeros(0)
qu=zeros(0)
t=zeros(0)

# set plots

pf3, = ax01.plot(t,f3,'b-', label="P7")
pfc5, = ax01.plot(t,fc5,'g-', label="P8")
paf3, = ax01.plot(t,af3,'r-', label="AF3")
pf7, = ax01.plot(t,f7,'y-', label="F7")
pt7, = ax01.plot(t,f3,'c-', label="T7")
pp7, = ax01.plot(t,f3,'c-', label="P7")
ps01, = ax01.plot(t,fc5,'k-', label="01")
ps02, = ax01.plot(t,af3,'b-', label="02")
pp8, = ax01.plot(t,f7,color = '#FF69B4', label="P8")
pt8, = ax01.plot(t,f3,color = '#FF8C00', label="T8")
pf8, = ax01.plot(t,f8,'m-', label="F8")
paf4, = ax01.plot(t,af4,color = '#7FFF00', label="AF4")
pfc6, = ax01.plot(t,fc6,color = '#8B4513', label="FC6")
pf4, = ax01.plot(t,f4,color = '#DDA0DD', label="F4")
pqu, = ax01.plot(t,f7,color = '#A9A9A9', label="QU")



# set legends
#ax01.legend([p011,p012], [p011.get_label(),p012.get_label()])
#ax01.legend([pf3, pfc5, paf3, pf7, pf8, paf4, pfc6, pf4], ["F3", "FC5", "AF3", "F7", "F8", "AF4", "FC6", "F4"])
ax01.legend([pf3, pfc5, paf3, pf7,pt7,pp7,ps01,ps02,pp8,pt8,pf8,paf4,pfc6,pf4,pqu], ["F3", "FC5", "AF3", "F7", "T7","P7", "01","02","P8","T8","F8","AF4","FC6","F4","QU"])
#ax01.legend([pf8, paf4, pfc6, pf4], ["F8", "AF4", "FC6", "F4"])

# Data Update every x (helps move the window right)
xmin = 0.0
xmax = 5.0
x = 0.0

e = EPOC()

def updateData(self):
	global x

	global f3 #left frontal nodes
	global fc5
	global af3
	global f7
	global t7
	global p7
	global s01
	global s02
	global p8
	global t8
	global f8 #right frontal nodes
	global af4
	global fc6
	global f4
	global qu
	global t
	global e
	
	data = e.get_sample()
	if data:
		#print data[1]*(math.exp(1.5))-11800

		f3=append(f3,data[0]+400)
		#fc5=append(fc5,data[1]*(math.exp(1.5))-6000)
		fc5=append(fc5,data[1]+200)
		af3=append(af3,data[2])
		f7=append(f7,data[3]-200)
		t7=append(t7,data[4]-400)
		p7=append(p7,data[5]-400) #
		s01=append(s01,data[6]-600)
		s02=append(s02,data[7]-800)
		p8=append(p8,data[8]-1000) #
		t8=append(t8,data[9]-1000)
		f8=append(f8,data[10]-1200)
		af4=append(af4,data[11]-1400)
		fc6=append(fc6,data[12]-1600)
		f4=append(f4,data[13]-1800)
		#v qu=append(qu,data[14]-2000)


		t=append(t,x)

		x += 0.05

		pf3.set_data(t,f3)
		pfc5.set_data(t,fc5)
		paf3.set_data(t,af3)
		pf7.set_data(t,f7)
		pt7.set_data(t,t7)
		pp7.set_data(t,p7)
		ps01.set_data(t,s01)
		ps02.set_data(t,s02)
		pp8.set_data(t,p8)
		pt8.set_data(t,t8)
		pf8.set_data(t,f8)
		paf4.set_data(t,af4)
		pfc6.set_data(t,fc6)
		pf4.set_data(t,f4)
		#pqu.set_data(t,qu)


		if x >= xmax-1.00:
			pf3.axes.set_xlim(x-xmax+1.0,x+1.0)
			pfc5.axes.set_xlim(x-xmax+1.0,x+1.0)
			paf3.axes.set_xlim(x-xmax+1.0,x+1.0)
			pf7.axes.set_xlim(x-xmax+1.0,x+1.0)
			pt7.axes.set_xlim(x-xmax+1.0,x+1.0)
			pp7.axes.set_xlim(x-xmax+1.0,x+1.0)
			ps01.axes.set_xlim(x-xmax+1.0,x+1.0)
			ps02.axes.set_xlim(x-xmax+1.0,x+1.0)
			pp8.axes.set_xlim(x-xmax+1.0,x+1.0)
			pt8.axes.set_xlim(x-xmax+1.0,x+1.0)
			pf8.axes.set_xlim(x-xmax+1.0,x+1.0)
			paf4.axes.set_xlim(x-xmax+1.0,x+1.0)
			pfc6.axes.set_xlim(x-xmax+1.0,x+1.0)
			pf4.axes.set_xlim(x-xmax+1.0,x+1.0)
			#pqu.axes.set_xlim(x-xmax+1.0,x+1.0)

		return pf3,pfc5,paf3,pf7,pt7,pp7,ps01,ps02,pp8,pt8,pf8,paf4,pfc6,pf4
	else:
		return 0,0,0,0,0,0,0,0,0,0,0,0,0

		# interval: draw new frame every 'interval' ms
		# frames: number of frames to draw
simulation = animation.FuncAnimation(f0,updateData, blit=False, frames=2000, interval=20, repeat=True)

		# Uncomment the next line if you want to save the animation
		#simulation.save(filename='sim.mp4',fps=30,dpi=300)

plt.show()

