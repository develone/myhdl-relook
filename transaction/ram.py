"""
red-256.pgm
ramsize = 65536
AZ = 16
red-32.pgm  SB_LUT4 8751
ramsize = 1024 
AZ = 10
red-16.pgm  SB_LUT4 2231
ramsize = 1024
AZ = 8

yosys -l simple.log -p 'synth_ice40 -blif ram.blif -json ram.json' ram.v

=== ram ===

   Number of wires:                477
   Number of wire bits:            991
   Number of public wires:         477
   Number of public wire bits:     991
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:                968
     SB_DFFE                       512
     SB_LUT4                       456

"""
import myhdl
from myhdl import *
from constsig import *

from PIL import Image
im = Image.open("red-32.pgm")
pix = im.load()
w, h = im.size
m = list(im.getdata())
m = [m[i:i+im.size[0]] for i in range(0, len(m), im.size[0])]
#print m



@block
def ram(dout, din, addr, we, clk, depth=256):
    """  Ram model """
    
    mem = [Signal(intbv(0, min=-(2**(W0)), max=(2**(W0)))) for i in range(depth)]
    
    @always(clk.posedge)
    def write():
        if we:
            mem[addr].next = din
                
    @always_comb
    def read():
        dout.next = mem[addr]

    return write, read

 

def convert_ram(hdl):
    ram_1 = ram(dout, din, addr, we, clk, depth=ramsize)

    ram_1.convert(hdl=hdl)

@block
def testbench(dout, din, addr, we, clk, depth=ramsize):
    ram_1 = ram(dout, din, addr, we, clk, depth=ramsize)
    
    @always(delay(10))
    def clkgen():
        clk.next = not clk
        
    @instance
    def stimulus():
        print m[0][0], m[0][1], m[0][2], m[0][3]
        """
        for i in range(ramsize):
            print m[0][i]
        """
        raise StopSimulation
    
    return instances()


#convert_ram(hdl='Verilog')
#tb = testbench(dout, din, addr, we, clk, depth=ramsize)
#tb.config_sim(trace=True)
#tb.run_sim()
