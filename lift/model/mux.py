import myhdl
from myhdl import *
W0 = 15
we = Signal(bool(0))
we_in = Signal(bool(0))
addr = Signal(intbv(0)[8:])
addr_in = Signal(intbv(0)[8:])
we_1 = Signal(bool(0))
addr_1 = Signal(intbv(0)[8:])
din = Signal(intbv(0)[W0:])
data_in = Signal(intbv(0)[W0:])
z = Signal(intbv(0)[W0:])
muxsel_i = Signal(bool(0))

muxaddrsel = Signal(intbv(0)[2:])
addr_left = Signal(intbv(0)[8:])
addr_sam = Signal(intbv(0)[8:])
addr_rht = Signal(intbv(0)[8:])
@block
def mux_data(z, din, data_in, we_1, we, we_in,  addr, addr_in, muxsel_i, muxaddrsel, addr_left, addr_sam, addr_rht,zfifo ):
	@always_comb
	def muxLogic():
		'''If  muxsel_i eq 0 ram  writing disabled to pc_read'''
		din.next = z
		we.next = we_1
		if (muxaddrsel == 0):
			addr.next = addr_left
		elif (muxaddrsel == 1):
			addr.next = addr_sam
		else:
			if (muxaddrsel == 2):
				addr.next = addr_rht
		 
		if (muxsel_i == 1):
			din.next = zfifo
			we.next =  we_in
			addr.next = addr_in
			
	return muxLogic	
def convert_mux_data(hdl):
	mux_data_1 = mux_data(z, din, data_in, we_1, we, we_in, addr, addr_in, muxsel_i, muxaddrsel, addr_left, addr_sam, addr_rht,zfifo)

	mux_data_1.convert(hdl=hdl)

#convert_mux_data(hdl='Verilog')
	
 
