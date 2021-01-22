from myhdl import *

Clk_f=100e6 #100 Mhz
BAUDRATE=230400
RX_BUFF_LEN=8

##### Signal definitions #####
iData=Signal(intbv(0)[8:])
oData=Signal(intbv(0)[8:])
iClk=Signal(bool(0))
iRst=Signal(bool(1))
iRX=Signal(bool(1))
oTX=Signal(bool(0))
WriteEnable=Signal(bool(0))
oWrBuffer_full=Signal(bool(0))
read_addr=Signal(intbv(0,min=0,max=8))
rx_addr=Signal(intbv(0,min=0,max=RX_BUFF_LEN))
pwrup=Signal(intbv(0)[6:])
dout=Signal(intbv(0)[32:])
addr_out=Signal(intbv(0)[32:])
we=Signal(bool(0))
oTX_programmer=Signal(bool(0))
oInfobyte=Signal(intbv(0)[8:])
oprog_Data_RS232=Signal(intbv(0)[8:])
oprog_WriteEnable_RS232=Signal(bool(0))
iprog_WrBuffer_full_RS232=Signal(bool(0))
programmer_enable=Signal(bool(1))

