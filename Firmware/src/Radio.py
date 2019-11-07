import os
import RPi.GPIO as GPIO
from RFM69.RFM69 import RFM69
from RFM69.RFM69registers import *
import time

class Radio:
    def __init__(self, selfNode, toNode, net=1, key=None,
                 sleep_interval=0.1, timeout=5, rst_pin=12):
        self.radio = RFM69(RF69_915MHZ, selfNode, net, True, rstPin=rst_pin)
        self.Node = selfNode
        self.ToNode = toNode
        self.key = key or "1234567891011121"
        self.sleep_interval = sleep_interval
        self.timeout = timeout

    @staticmethod
    def CommaSeparate(*args):
        return ",".join(map(str, args))

    def SetUp(self):
        self.radio.readAllRegs()
        self.radio.rcCalibration()
        #self.radio.setHighPower(True)
        # self.radio.encrypt(KEY)
        self.radio.setPowerLevel(0)

        # 300 kbps settings
        self.radio.writeReg( REG_OPMODE, RF_OPMODE_SEQUENCER_ON | RF_OPMODE_LISTEN_OFF | RF_OPMODE_STANDBY )
        self.radio.writeReg( REG_DATAMODUL, RF_DATAMODUL_DATAMODE_PACKET | RF_DATAMODUL_MODULATIONTYPE_FSK | RF_DATAMODUL_MODULATIONSHAPING_00 )# 0x02
        self.radio.writeReg( REG_BITRATELSB, RF_BITRATEMSB_300000 )# 0x03
        self.radio.writeReg( REG_BITRATELSB, RF_BITRATELSB_300000 )# 0x04
        self.radio.writeReg( REG_FDEVMSB, RF_FDEVMSB_300000   )# 0x05
        self.radio.writeReg( REG_FDEVLSB, RF_FDEVLSB_300000 )# 0x06
        self.radio.writeReg( REG_FRFMSB, RF_FRFMSB_915 )# 0x07
        self.radio.writeReg( REG_FRFMID, RF_FRFMID_915 )# 0x08
        self.radio.writeReg( REG_FRFLSB, RF_FRFLSB_915 )#         0x09
        self.radio.writeReg( REG_RXBW, RF_RXBW_DCCFREQ_111 | RF_RXBW_MANT_16 | RF_RXBW_EXP_0 )# 0x19
        self.radio.writeReg( REG_DIOMAPPING1, RF_DIOMAPPING1_DIO0_01 )# 0x25
        self.radio.writeReg( REG_DIOMAPPING2, RF_DIOMAPPING2_CLKOUT_OFF )#0x26
        self.radio.writeReg( REG_IRQFLAGS2, RF_IRQFLAGS2_FIFOOVERRUN )       # 0x28
        self.radio.writeReg( REG_RSSITHRESH, 220 )# 0x29
        self.radio.writeReg( REG_PREAMBLELSB, 6 )# 0x2D
        self.radio.writeReg( REG_SYNCCONFIG, RF_SYNC_ON |    RF_SYNC_FIFOFILL_AUTO | RF_SYNC_SIZE_3 | RF_SYNC_TOL_0 )# 0x2E
        self.radio.writeReg( REG_SYNCVALUE1, 0x88 )# 0x2F
        self.radio.writeReg( REG_SYNCVALUE2, NET )# 0x30
        self.radio.writeReg( REG_SYNCVALUE3, 0x88 )# 0x2F
        self.radio.writeReg( REG_PACKETCONFIG1, RF_PACKET1_FORMAT_VARIABLE | RF_PACKET1_DCFREE_OFF | RF_PACKET1_CRC_OFF | RF_PACKET1_CRCAUTOCLEAR_OFF | RF_PACKET1_ADRSFILTERING_OFF )# 0x37
        self.radio.writeReg( REG_PAYLOADLENGTH, 66 )# 0x38
        self.radio.writeReg( REG_FIFOTHRESH, RF_FIFOTHRESH_TXSTART_FIFONOTEMPTY | RF_FIFOTHRESH_VALUE )# 0x3C
        self.radio.writeReg( REG_PACKETCONFIG2, RF_PACKET2_RXRESTARTDELAY_2BITS | RF_PACKET2_AUTORXRESTART_ON | RF_PACKET2_AES_OFF )# 0x3D
        self.radio.writeReg( REG_TESTDAGC, RF_DAGC_IMPROVED_LOWBETA0 )# 0x6F

    def Transmit(self, *args):
        message =  Radio.CommaSeparate(*args)
        self.radio.send(self.ToNode, message)

    def Receive(self):
        self.radio.receiveBegin()

        timedOut = 0
        while not self.radio.receiveDone():
            timedOut += self.sleep_interval
            time.sleep(self.sleep_interval)
            if timedOut > self.timeout:
                return

        message = "".join([chr(letter) for letter in self.radio.DATA])

        if self.radio.ACKRequested():
            self.radio.sendACK()

        return message
