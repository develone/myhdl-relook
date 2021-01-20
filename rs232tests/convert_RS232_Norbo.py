from myhdl import *
import RS232_Norbo
#from updatebuff import updatebuff
#from rs232loopback import rs232loopback

def convert_RS232_Module(hdl):
  rs232_inst=RS232_Norbo.RS232_Module(iClk,iRst,iRX,oTX, iData,WriteEnable,  \
    oWrBuffer_full,oData,read_addr,rx_addr,Clkfrequenz=Clk_f,  \
    Baudrate=BAUDRATE,RX_BUFFER_LENGTH=RX_BUFF_LEN)
  #updatebuff_1 = updatebuff(iClk, iData, WriteEnable,ldData)
  #loopback_1 = rs232loopback(iClk, iRX, oTX)
  
    
  rs232_inst.convert(hdl=hdl)

Clk_f=100e6 #100 Mhz
BAUDRATE=230400
iClk = Signal(bool(0))
iRst = Signal(bool(0))
iRX = Signal(bool(0))
oTX = Signal(bool(0))
iData=Signal(intbv(0)[8:])
WriteEnable=Signal(bool(0))
oWrBuffer_full=Signal(bool(0))
oData=Signal(intbv(0)[8:])
read_addr=Signal(intbv(0,min=0,max=8))
RX_BUFF_LEN=8
rx_addr=Signal(intbv(0,min=0,max=RX_BUFF_LEN))
ldData=Signal(intbv(0)[8:])

convert_RS232_Module(hdl='Verilog')
