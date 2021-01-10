import myhdl
from myhdl import *

i_sw = Signal(bool(0))
o_led = Signal(bool(0))

@block
def switch(i_sw,o_led):
	@always_comb
	def logic():
		o_led.next  = i_sw
	return logic

def convert_switch(hdl):
	switch_inst = switch(i_sw,o_led)
	switch_inst.convert(hdl=hdl)
	
convert_switch(hdl='Verilog')
