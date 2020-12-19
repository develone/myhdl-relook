import myhdl
from myhdl import *
from PIL import Image
im = Image.open("red-32.pgm")
pix = im.load()
w, h = im.size
m = list(im.getdata())
m = [m[i:i+im.size[0]] for i in range(0, len(m), im.size[0])]

W0 = 15
AZ = 5 
"""
yosys -l simple.log -p 'synth_ice40 -blif addrbump.blif -json addrbump.json' addrbump.v
=== addrbump ===

   Number of wires:                  8
   Number of wire bits:             24
   Number of public wires:           8
   Number of public wire bits:      24
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:                 15
     SB_CARRY                        3
     SB_DFF                          1
     SB_DFFE                         5
     SB_LUT4                         6

"""
clk = Signal(bool(0))
addrtoinc = Signal(intbv(0)[AZ:])
incaddr = Signal(intbv(0)[AZ:])
update2_i = Signal(bool(0))
update2_o = Signal(bool(0))

@block
def addrbump(addrtoinc, update2_i, clk, incaddr, update2_o):
    @always(clk.posedge)
    def rtl4 ():
	if (update2_i == 1):
	    update2_o.next =  0
	    incaddr.next = addrtoinc + 1
	else:
	    update2_o.next = 1
	
    return rtl4

@block
def testbench(addrtoinc, update2_i, clk, incaddr, update2_o):
    
    addrbump_1 = addrbump(addrtoinc, update2_i, clk, incaddr, update2_o)
    
    @always(delay(10))
    def clkgen():
        clk.next = not clk
	
    @instance
    def stimulus():
        print m[0][0], m[0][1], m[0][2], m[0][3]
        

	for i in range(0,15):
	    #print addrtoinc
	     
	    addrtoinc.next = i
	    yield clk.posedge
			
	    update2_i.next = 1
	    yield clk.posedge
				
	    update2_i.next = 0
	    yield clk.posedge
	    
	    print addrtoinc, incaddr
	    
	raise StopSimulation

    return instances()
    
def convert_addrbump(hdl):
	addrbump_1 = addrbump(addrtoinc, update2_i, clk, incaddr, update2_o)
	addrbump_1.convert(hdl=hdl)
	
#convert_addrbump(hdl='Verilog')
#tb = testbench(addrtoinc, update2_i, clk, incaddr, update2_o)
#tb.config_sim(trace=True)
#tb.run_sim()

