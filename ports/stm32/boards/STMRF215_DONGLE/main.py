# main.py -- put your code here!
import random

## Bring up the RF215
from radio import rf215

rfspi = rf215(2)
rfspi.write(rf215.RF09_IRQS, 0)
rfspi.write(rf215.RF24_IRQS, 0)
rfspi.write(rf215.BBC0_IRQS, 0)
rfspi.write(rf215.BBC1_IRQS, 0)

## ----------------------------------------------
## Program the 2.4GHz RF215 baseband for O-QPSK
## ----------------------------------------------
rfspi.rfcore = rf215.RF24
rfspi.baseband = rf215.BBC1

## Program the transmitter analog front end.
rfspi.rfwrite(rf215.RFxx_TXCUTC, 0xCB) 	#TXCUTC.PARAMP=32us and LPFCUT=80kHz
rfspi.rfwrite(rf215.RFxx_TXDFE, 0x61) 	#TXDFE.SR = 4000kHz and RCUT=3
rfspi.rfwrite(rf215.RFxx_PAC, 0x7C)
rfspi.rfwrite(rf215.RFxx_AUXS, 0x02)

## Program the receiver analog front end.
rfspi.rfwrite(rf215.RFxx_RXBWC, 0x08)	# IF Bandwidth=1000kHz, no IF shift
rfspi.rfwrite(rf215.RFxx_RXDFE, 0x01) 	#RXDFE.SR = 4000kHz and RCUT=0

rfspi.bbwrite(rf215.BBCx_PC, 0x57) 		# Enable FFSK baseband with auto-FCS
rfspi.bbwrite(rf215.BBCx_OQPSKC0, 0x02)	# Rate mode 1000kchip/s
rfspi.bbwrite(rf215.BBCx_OQPSKC1, 0xDB)	# Receive preabmle thresholds
rfspi.bbwrite(rf215.BBCx_OQPSKC2, 0x04)	# Receive preabmle thresholds
rfspi.bbwrite(rf215.BBCx_OQPSKC3, 0x00)	# Receive preabmle thresholds
rfspi.bbwrite(rf215.BBCx_OQPSKPHRTX, 0x01) # Transmit as legacy O-QPSK

# Prepare to transmit on channel zero in the 2.4GHz ISM band.
rfspi.setfreq(2405000000)
rfspi.setstate(rf215.STATE_TXPREP)

## ----------------------------------------------
## Program the 900MHz RF215 baseband for MR-FSK
## ----------------------------------------------
rfspi.rfcore = rf215.RF09
rfspi.baseband = rf215.BBC0

## Program the transmitter analog front end.
rfspi.rfwrite(rf215.RFxx_TXCUTC, 0xC0) 	#TXCUTC.PARAMP=32us and LPFCUT=80kHz
rfspi.rfwrite(rf215.RFxx_TXDFE, 0x9A) 	#TXDFE.SR = 400kHz and RCUT=4
rfspi.rfwrite(rf215.RFxx_PAC, 0x70)
rfspi.rfwrite(rf215.RFxx_AUXS, 0x02)

## Program the receiver analog front end.
rfspi.rfwrite(rf215.RFxx_RXBWC, 0x00)	# IF Bandwidth=160kHz, no IF shift
rfspi.rfwrite(rf215.RFxx_RXDFE, 0x4A) 	#RXDFE.SR = 400kHz and RCUT=1

## Setup the FSK configuration for FFSK-B mode 1 (50kbps FFSK modindex=1.0)
rfspi.bbwrite(rf215.BBCx_PC, 0x55) 		# Enable FFSK baseband with auto-FCS
rfspi.bbwrite(rf215.BBCx_FSKC0, 0xD6)	# Modulation index=1.0
rfspi.bbwrite(rf215.BBCx_FSKC1, 0x00)	# 50kbps
rfspi.bbwrite(rf215.BBCx_FSKC2, 0x41)	# Bunch of RX stuff left as default
rfspi.bbwrite(rf215.BBCx_FSKC3, 0x85)	# SFD/Preabmle thresholds
rfspi.bbwrite(rf215.BBCx_FSKC4, 0x18)
rfspi.bbwrite(rf215.BBCx_FSKPLL, 8)
rfspi.bbwrite(rf215.BBCx_FSKSFD0L, 0x09)
rfspi.bbwrite(rf215.BBCx_FSKSFD0H, 0x72)
rfspi.bbwrite(rf215.BBCx_FSKSFD1L, 0xf6)
rfspi.bbwrite(rf215.BBCx_FSKSFD1H, 0x72)

## Configure FSK direct modulation
rfspi.bbwrite(rf215.BBCx_FSKDM, 0x03)
rfspi.bbwrite(rf215.BBCx_FSKPE0, 0x02)
rfspi.bbwrite(rf215.BBCx_FSKPE1, 0x03)
rfspi.bbwrite(rf215.BBCx_FSKPE2, 0xFC)

# Prepare to transmit on channel zero in the 900MHz ISM band.
rfspi.setfreq(902200000)
rfspi.setstate(rf215.STATE_TXPREP)

## Run the test LED loop and blast some packets.
foo = [pyb.LED(1), pyb.LED(2), pyb.LED(3), pyb.LED(4)]
i = 0
while True:
	i = (i+1) % len(foo)
	foo[i].toggle()

	## Generate a random packet
	packet = bytearray(100)
	for x in range(0, len(packet)):
		packet[x] = random.randint(0, 255)

	## Transmit the packet on the 900MHz interface
	rfspi.rfcore = rf215.RF09
	rfspi.baseband = rf215.BBC0
	rfspi.write(rf215.BBC0_FBTXS, packet)
	rfspi.bbwrite(rf215.BBCx_TXFLH, (len(packet) >> 8) & 0xff)
	rfspi.bbwrite(rf215.BBCx_TXFLL, (len(packet) >> 0) & 0xff)
	rfspi.setstate(rf215.STATE_TX)
	pyb.delay(500)

	## Transmit the packet on the 2.4GHz interface
	rfspi.rfcore = rf215.RF24
	rfspi.baseband = rf215.BBC1
	rfspi.write(rf215.BBC1_FBTXS, packet)
	rfspi.bbwrite(rf215.BBCx_TXFLH, (len(packet) >> 8) & 0xff)
	rfspi.bbwrite(rf215.BBCx_TXFLL, (len(packet) >> 0) & 0xff)
	rfspi.setstate(rf215.STATE_TX)
	pyb.delay(500)

