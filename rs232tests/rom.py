from myhdl import *

from rs232sig import *

@block
def rom(rom_dout,rom_addr,CONTENT):
	@always_comb
	def read():
		rom_dout.next=CONTENT[int(rom_addr)]
	return read

def convert_rom(hdl):
	rom0_inst=rom(rom_dout,rom_addr,CONTENT)
	rom0_inst.convert(hdl=hdl)
#convert_rom(hdl='Verilog')
	
