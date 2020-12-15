import myhdl 
from myhdl import *
import random
'''unsigned data width signed is W0 + 1'''
W0 = 15

t = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0)))) 
x = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0))))
z = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0))))
clk = Signal(bool(0))
@block
def signed2twoscomplement(clk, x, z):
    
    @always(clk.posedge)
    def unsigned_logic():
        z.next = x

    return unsigned_logic
def convert_signed2twoscomplement(hdl):
    signed2twoscomplement_1 = signed2twoscomplement(clk, x, z)
    signed2twoscomplement_1.convert(hdl=hdl)
@block
def testbench(clk, x, z):
    instance_1 = signed2twoscomplement(clk, x, z)
    @always(delay(10))
    def clkgen():
        clk.next = not clk
    @instance
    def stimulus():
        for i in range(-(2**(W0)),2**(W0),1):
            t.next = random.randrange(-2**(W0-1),2**(W0-1))
            t.next = i
            yield clk.posedge
            x.next = t[W0:]
            yield clk.posedge
            #print ("%d %d %d %d %s %s %s") % (x, z.signed(), z, bin(x,W0), bin(z, W0))
            #print ("%d %d %d %d %s %s %s") % (x, z.signed(), z, hex(x), hex(z))
            #if( z.signed() < 0):
                #print ("%d ") % (((2**W0)+z.signed()) + 1)
        raise StopSimulation
    return instances()
#convert_signed2twoscomplement(hdl='Verilog')
#tb = testbench(clk, x, z)
#tb.config_sim(trace=True)
#tb.run_sim()

