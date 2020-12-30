from myhdl import *
from main import main

"""
yosys -l simple.log -p 'synth_ice40 -blif top.blif -json top.json' top.v
=== top ===

   Number of wires:                 43
   Number of wire bits:            157
   Number of public wires:          43
   Number of public wire bits:     157
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:                 63
     SB_CARRY                       10
     SB_DFF                          2
     SB_DFFE                        18
     SB_DFFSS                        1
     SB_LUT4                        32


"""
from constsig import *

@block
def top(clk,iRX,oTX):
	main_0 = main(clk,iRX,oTX)
	return instances()

def convert_top(hdl):
	
	top_0 = top(clk,iRX,oTX)
	top_0.convert(hdl=hdl)

clk=Signal(bool(0))
iRX=Signal(bool(1))
oTX=Signal(bool(0))
convert_top(hdl='Verilog')
