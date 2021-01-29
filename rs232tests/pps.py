from myhdl import *

from rs232sig import *


@block
def pps(iClk,ppscounter,sig):
	@always(iClk.posedge)
	def ppsi():

		
		
		if(ppscounter < 50000000):
			ppscounter.next=ppscounter+1
			sig.next=0
		else:
			ppscounter.next=0
			sig.next=1
	return ppsi

def convert_pps(hdl):
	pps0_inst=pps(iClk,ppscounter,sig)
	pps0_inst.convert(hdl=hdl)
#convert_pps(hdl='Verilog')
			
