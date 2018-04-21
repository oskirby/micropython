#RF215 SPI Helpers
import pyb
from pyb import SPI
from pyb import Pin

class rf215:
    def __init__(self, bus):
        self.spi = pyb.SPI(bus, SPI.MASTER, baudrate=8000000, polarity=0, phase=0)
        self.nrst = pyb.Pin('RF_NRST', Pin.OUT_PP)
        self.csel = pyb.Pin('RF_CSEL', Pin.OUT_PP)
        self.csel.high()
        self.nrst.low()
        pyb.delay(10)
        self.nrst.high()
        self.rfcore = rf215.RF09
        self.baseband = rf215.BBC0

    def read(self, address):
        tx = bytearray([address >> 8, address & 0xff, 0])
        self.csel.low()
        rx = self.spi.send_recv(tx)
        self.csel.high()
        return rx[2]

    def bbread(self, address):
        return self.read(address + self.baseband)

    def rfread(self, address):
        return self.read(address + self.rfcore)

    def write(self, address, value):
        if (isinstance(value, bytearray)):
            cmd = bytearray([0x80 | (address >> 8), address & 0xff])
            self.csel.low()
            self.spi.send(cmd)
            self.spi.send(value)
            self.csel.high()
        else:
            tx = bytearray([0x80 | (address >> 8), address & 0xff, value])
            self.csel.low()
            self.spi.send(tx)
            self.csel.high()

    def bbwrite(self, address, value):
        return self.write(address + self.baseband, value)

    def rfwrite(self, address, value):
        return self.write(address + self.rfcore, value)

    def setfreq(self, hz):
        if (hz >= 2366000000):
            nch = int((((hz - 2366000000) << 16) + 13000000) / 26000000)
            self.rfwrite(rf215.RFxx_CCF0H, (nch >> 16) & 0xff)
            self.rfwrite(rf215.RFxx_CCF0L, (nch >> 8) & 0xff)
            self.rfwrite(rf215.RFxx_CNL, nch & 0xff)
            self.rfwrite(rf215.RFxx_CNM, 0xC0)
        elif (hz >= 754000000):
            nch = int((((hz - 754000000) << 16) + 6500000) / 13000000)
            self.rfwrite(rf215.RFxx_CCF0H, (nch >> 16) & 0xff)
            self.rfwrite(rf215.RFxx_CCF0L, (nch >> 8) & 0xff)
            self.rfwrite(rf215.RFxx_CNL, nch & 0xff)
            self.rfwrite(rf215.RFxx_CNM, 0x80)
        else:
            nch = int((((hz - 377000000) << 16) + 3250000) / 6500000)
            self.rfwrite(rf215.RFxx_CCF0H, (nch >> 16) & 0xff)
            self.rfwrite(rf215.RFxx_CCF0L, (nch >> 8) & 0xff)
            self.rfwrite(rf215.RFxx_CNL, nch & 0xff)
            self.rfwrite(rf215.RFxx_CNM, 0x40)

    def setstate(self, state, wait=True):
        rfstate = self.rfread(rf215.RFxx_STATE)
        while True:
            print("Transition from " + hex(rfstate) + " to " + hex(state))
            self.rfwrite(rf215.RFxx_CMD, state)
            if (not wait) or (state == rf215.STATE_NOP) or (state == rf215.STATE_SLEEP):
                break
            rfstate = self.rfread(rf215.RFxx_STATE)
            if (rfstate == state):
                break

    ## Baseband Offsets
    RF09 = 0x100
    RF24 = 0x200
    BBC0 = 0x300
    BBC1 = 0x400

    ## RF215 Registers
    RF09_IRQS = 0x0000
    RF24_IRQS = 0x0001
    BBC0_IRQS = 0x0002
    BBC1_IRQS = 0x0003
    RF_RST = 0x0005
    RF_CFG = 0x0006
    RF_CLKO = 0x0007
    RF_BMVDC = 0x0008
    RF_XOC = 0x0009
    RF_IQIFC0 = 0x000A
    RF_IQIFC1 = 0x000B
    RF_IQIFC2 = 0x000C
    RF_PN = 0x000D
    RF_VN = 0x000E
    ## RF core registers
    RFxx_IRQM = 0x0000
    RFxx_AUXS = 0x0001
    RFxx_STATE = 0x0002
    RFxx_CMD = 0x0003
    RFxx_CS = 0x0004
    RFxx_CCF0L = 0x0005
    RFxx_CCF0H = 0x0006
    RFxx_CNL = 0x0007
    RFxx_CNM = 0x0008
    RFxx_RXBWC = 0x0009
    RFxx_RXDFE = 0x000A
    RFxx_AGCC = 0x000B
    RFxx_AGCS = 0x000C
    RFxx_RSSI = 0x000D
    RFxx_EDC = 0x000E
    RFxx_EDD = 0x000F
    RFxx_EDV = 0x0010
    RFxx_RNDV = 0x0011
    RFxx_TXCUTC = 0x0012
    RFxx_TXDFE = 0x0013
    RFxx_PAC = 0x0014
    RFxx_PADFE = 0x0016
    RFxx_PLL = 0x0021
    RFxx_TXCI = 0x0025
    RFxx_TXCO = 0x0026
    RFxx_TXDACI = 0x0027
    RFxx_TXDACQ = 0x0028
    ## Baseband registers
    BBCx_IRQM = 0x0000
    BBCx_PC = 0x0001
    BBCx_RXFLL = 0x0004
    BBCx_RXFLH = 0x0005
    BBCx_TXFLL = 0x0006
    BBCx_TXFLH = 0x0007
    BBCx_FBLL = 0x0008
    BBCx_FBLH = 0x0009
    BBCx_FBLIL = 0x000A
    BBCx_FBLIH = 0x000B
    BBCx_OFDMPHRTX = 0x000C
    BBCx_OFDMPHRRX = 0x000D
    BBCx_OFDMC = 0x000E
    BBCx_OFDMSW = 0x000F
    BBCx_OQPSKC0 = 0x0010
    BBCx_OQPSKC1 = 0x0011
    BBCx_OQPSKC2 = 0x0012
    BBCx_OQPSKC3 = 0x0013
    BBCx_OQPSKPHRTX = 0x0014
    BBCx_OQPSKPHRRX = 0x0015
    BBCx_AFC0 = 0x0020
    BBCx_AFC1 = 0x0021
    BBCx_AFFTM = 0x0022
    BBCx_AFFVM = 0x0023
    BBCx_AFS = 0x0024
    BBCx_MACEA0 = 0x0025
    BBCx_MACEA1 = 0x0026
    BBCx_MACEA2 = 0x0027
    BBCx_MACEA3 = 0x0028
    BBCx_MACEA4 = 0x0029
    BBCx_MACEA5 = 0x002A
    BBCx_MACEA6 = 0x002B
    BBCx_MACEA7 = 0x002C
    BBCx_MACPID0F0 = 0x002D
    BBCx_MACPID1F0 = 0x002E
    BBCx_MACSHA0F0 = 0x002F
    BBCx_MACSHA1F0 = 0x0030
    BBCx_MACPID0F1 = 0x0031
    BBCx_MACPID1F1 = 0x0032
    BBCx_MACSHA0F1 = 0x0033
    BBCx_MACSHA1F1 = 0x0034
    BBCx_MACPID0F2 = 0x0035
    BBCx_MACPID1F2 = 0x0036
    BBCx_MACSHA0F2 = 0x0037
    BBCx_MACSHA1F2 = 0x0038
    BBCx_MACPID0F3 = 0x0039
    BBCx_MACPID1F3 = 0x003A
    BBCx_MACSHA0F3 = 0x003B
    BBCx_MACSHA1F3 = 0x003C
    BBCx_AMCS = 0x0040
    BBCx_AMEDT = 0x0041
    BBCx_AMAACKPD = 0x0042
    BBCx_AMAACKTL = 0x0043
    BBCx_AMAACKTH = 0x0044
    BBCx_FSKC0 = 0x0060
    BBCx_FSKC1 = 0x0061
    BBCx_FSKC2 = 0x0062
    BBCx_FSKC3 = 0x0063
    BBCx_FSKC4 = 0x0064
    BBCx_FSKPLL = 0x0065
    BBCx_FSKSFD0L = 0x0066
    BBCx_FSKSFD0H = 0x0067
    BBCx_FSKSFD1L = 0x0068
    BBCx_FSKSFD1H = 0x0069
    BBCx_FSKPHRTX = 0x006A
    BBCx_FSKPHRRX = 0x006B
    BBCx_FSKRPC = 0x006C
    BBCx_FSKRPCONT = 0x006D
    BBCx_FSKRPCOFFT = 0x006E
    BBCx_FSKRRXFLL = 0x0070
    BBCx_FSKRRXFLH = 0x0071
    BBCx_FSKDM = 0x0072
    BBCx_FSKPE0 = 0x0073
    BBCx_FSKPE1 = 0x0074
    BBCx_FSKPE2 = 0x0075
    BBCx_PMUC = 0x0080
    BBCx_PMUVAL = 0x0081
    BBCx_PMUQF = 0x0082
    BBCx_PMUI = 0x0083
    BBCx_PMUQ = 0x0084
    BBCx_CNTC = 0x0090
    BBCx_CNT0 = 0x0091
    BBCx_CNT1 = 0x0092
    BBCx_CNT2 = 0x0093
    BBCx_CNT3 = 0x0094

    ## Frame buffer addresses
    BBC0_FBRXS = 0x2000
    BBC0_FBRXE = 0x27FE
    BBC0_FBTXS = 0x2800
    BBC0_FBTXE = 0x2FFE
    BBC1_FBRXS = 0x3000
    BBC1_FBRXE = 0x37FE
    BBC1_FBTXS = 0x3800
    BBC1_FBTXE = 0x38FE

    ## Transceiver States
    STATE_NOP = 0x00
    STATE_SLEEP = 0x01
    STATE_TRXOFF = 0x02
    STATE_TXPREP = 0x03
    STATE_TX = 0x04
    STATE_RX = 0x05
    STATE_TRANSITION = 0x06
    STATE_RESET  =0x07
