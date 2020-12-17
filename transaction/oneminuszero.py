import myhdl
from myhdl import *
W0 = 15
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
clk = Signal(bool(0))
update1_i = Signal(bool(0))
update1_o = Signal(bool(0))
sub_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
first_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
snd_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))



@block
def oneminuszero(first_i, snd_i,  update1_i, clk, sub_o, update1_o):
	@always(clk.posedge)
	def rtl1 ():
		if (update1_i == 1):
			update1_o.next =  0
			sub_o.next = (first_i - snd_i)
		else:
			update1_o.next = 1
	
	return rtl1

def convert_oneminuszero(hdl):
	inst_1 = oneminuszero(first_i, snd_i,  update1_i, clk, sub_o, update1_o)
	inst_1.convert(hdl=hdl)
	
#convert_oneminuszero(hdl='Verilog')
