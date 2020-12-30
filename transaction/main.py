from myhdl import *
from RS232_Norbo import RS232_Module
from RS232Programmer import RS232Programmer
from rs232loopback import rs232loopback
"""
yosys -l simple.log -p 'synth_ice40 -blif main.blif -json main.json' main.v
=== top ===

   Number of wires:                 42
   Number of wire bits:            156
   Number of public wires:          42
   Number of public wire bits:     156
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:                 61
     SB_CARRY                       10
     SB_DFF                          2
     SB_DFFE                        18
     SB_DFFSS                        1
     SB_LUT4                        30

"""
from constsig import *

@block
def main(clk,iRX,oTX):
	rs232loopback_1 = rs232loopback(oTX, iRX)
	rs232_instance=RS232_Module(clk,iRst,iRX,oTX, iData,WriteEnable,  \
		oWrBuffer_full,oData,read_addr,rx_addr,Clkfrequenz=Clk_f,  \
		Baudrate=BAUDRATE,RX_BUFFER_LENGTH=RX_BUFF_LEN)
	programmer_inst=RS232Programmer(clk,iRst,programmer_enable,oInfobyte, \
		dout,addr_out,we, \
		oprog_Data_RS232,oprog_WriteEnable_RS232, iprog_WrBuffer_full_RS232,oData,read_addr,rx_addr)
	return instances()

def convert_main(hdl):
	
	main_0 = main(clk,iRX,oTX)
	main_0.convert(hdl=hdl)

clk=Signal(bool(0))
iRX=Signal(bool(1))
oTX=Signal(bool(0))
#convert_main(hdl='Verilog')
