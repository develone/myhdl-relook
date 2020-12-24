import myhdl
from myhdl import *
from constsig import *
"""
yosys -l simple.log -p 'synth_ice40 -blif oneminuszero.blif -json oneminuszero.json' oneminuszero.v
=== oneminuszero ===

   Number of wires:                 24
   Number of wire bits:             99
   Number of public wires:          24
   Number of public wire bits:      99
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:                 64
     SB_CARRY                       15
     SB_DFF                          1
     SB_DFFE                        16
     SB_LUT4                        32

""" 

@block
def oneminuszero(first_i, nd_i,  update1_i, clk, sub_o, update1_o):
	@always(clk.posedge)
	def rtl1 ():
		if (update1_i == 1):
			update1_o.next =  0
			sub_o.next = (first_i - nd_i)
		else:
			update1_o.next = 1
	
	return rtl1

def convert_oneminuszero(hdl):
	inst_1 = oneminuszero(first_i, nd_i,  update1_i, clk, sub_o, update1_o)
	inst_1.convert(hdl=hdl)
	
#convert_oneminuszero(hdl='Verilog')
