from myhdl import *
from constsig import *

@block
def rs232loopback(oTX, iRX):
	
	@always_comb
	def logic():
		iRX.next=oTX
	return logic
	
def convert_rs232loopback(hdl):
	loopback_1 = rs232loopback(oTX, iRX)
	loopback_1.convert(hdl=hdl)

#convert_rs232loopback(hdl='Verilog')
