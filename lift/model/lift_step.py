import myhdl
from myhdl import *
W0 = 9
res_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
left_i = Signal(intbv(0)[W0:])
right_i = Signal(intbv(0)[W0:])
sam_i = Signal(intbv(0)[W0:])
flgs_i = Signal(intbv(0)[4:])
clk = Signal(bool(0))
update_i = Signal(bool(0))
update_o = Signal(bool(0))

@block
def lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o):
    
    @always(clk.posedge)
    def rtl ():
        if (update_i == 1):
            update_o.next = 0
            if (flgs_i == 7):
                res_o.next = sam_i.signed() - ( (left_i.signed() >> 1) + (right_i.signed() >> 1) )
            elif (flgs_i == 5):
                res_o.next = sam_i.signed() + ( (left_i.signed() >> 1) + (right_i.signed() >> 1) )
            elif (flgs_i == 6):
                res_o.next = sam_i.signed() + ( (left_i.signed() + right_i.signed() + 2) >> 2 )
            elif (flgs_i == 4):
                res_o.next = sam_i.signed() - ( (left_i.signed() + right_i.signed() + 2) >> 2 )
        else:
                update_o.next = 1
    return rtl    
    
def convert_lift_step(hdl):
    lift_step_1 = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)
    lift_step_1.convert(hdl=hdl)

convert_lift_step(hdl='Verilog')
