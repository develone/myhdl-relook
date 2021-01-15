from myhdl import *
 

@block
def rs232loopback(clock, iRX, oTX):
	
	@always(clock.posedge)
	def logic():
		iRX.next=oTX
	return logic
	
def convert_rs232loopback(hdl):
	clock=Signal(bool(0))
	iRX=Signal(bool(1))
	oTX=Signal(bool(1))
	
	i_clk=Signal(bool(0))
	i_uart_rx=Signal(bool(0))
	o_uart_tx=Signal(bool(0))
	
	#loopback_1 = rs232loopback(clock=i_clk, iRX=i_uart_rx, oTX=o_uart_tx)
	loopback_1 = rs232loopback(clock, iRX, oTX)
	 
	loopback_1.convert(hdl=hdl)

convert_rs232loopback(hdl='Verilog')
