import myhdl
from myhdl import *
from PIL import Image
im = Image.open("red.pgm")
pix = im.load()
w, h = im.size
m = list(im.getdata())
m = [m[i:i+im.size[0]] for i in range(0, len(m), im.size[0])]
#print m


W0 = 9
@block
def ram(dout, din, addr, we, clk, depth=256):
    """  Ram model """
    
    mem = [Signal(intbv(0)[W0:]) for i in range(depth)]
    
    @always(clk.posedge)
    def write():
        if we:
            mem[addr].next = din
                
    @always_comb
    def read():
        dout.next = mem[addr]

    return write, read


dout = Signal(intbv(0)[W0:])
din = Signal(intbv(0)[W0:])
addr = Signal(intbv(0)[8:])
we = Signal(bool(0))
clk = Signal(bool(0))

def convert_ram(hdl):
    ram_1 = ram(dout, din, addr, we, clk, depth=256)

    ram_1.convert(hdl=hdl)

#convert_ram(hdl='Verilog')
