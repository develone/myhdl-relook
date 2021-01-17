from myhdl import *
 

@block
def rs232loopback(iClk, iRX, oTX):
	
	@always(iClk.posedge)
	def logic():
		iRX.next=oTX
	return logic
	
def convert_rs232loopback(hdl):
	iClk=Signal(bool(0))
	iRX=Signal(bool(1))
	oTX=Signal(bool(1))
	

	
	#loopback_1 = rs232loopback(clock=i_clk, iRX=i_uart_rx, oTX=o_uart_tx)
	loopback_1 = rs232loopback(iClk, iRX, oTX)
	 
	loopback_1.convert(hdl=hdl)

convert_rs232loopback(hdl='Verilog')
