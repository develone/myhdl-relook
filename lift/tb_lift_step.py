import myhdl 
from myhdl import *
#block, always, instance, Signal, ResetSignal, delay, intbv, StopSimulation
from lift_step import lift_step
from signed2twoscomplement import signed2twoscomplement

W0 = 15
@block
def testbench():

    res_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
    left_i = Signal(intbv(0)[W0:])
    right_i = Signal(intbv(0)[W0:])
    sam_i = Signal(intbv(0)[W0:])
    flgs_i = Signal(intbv(0)[4:])
    clk = Signal(bool(0))
    update_i = Signal(bool(0))
    update_o = Signal(bool(0))

    lift_step_1 = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():

        update_i.next = 1
        left_i.next = 120
        right_i.next = 121
        sam_i.next =122
        flgs_i.next = 7
        yield clk.posedge
        update_i.next = 0
        yield clk.posedge
        for i in range(3):
            yield clk.posedge
            
        update_i.next = 1
        left_i.next = 120
        right_i.next = 121
        sam_i.next = 122
        flgs_i.next = 5
        yield clk.posedge
        update_i.next = 0
        yield clk.posedge
        for i in range(3):
            yield clk.posedge


        update_i.next = 1
        left_i.next = 10
        right_i.next = 11
        sam_i.next = 12
        flgs_i.next = 6
        yield clk.posedge
        update_i.next = 0
        yield clk.posedge
        for i in range(3):
            yield clk.posedge
            
        update_i.next = 1
        left_i.next = 10
        right_i.next = 11
        sam_i.next = 12
        flgs_i.next = 4
        yield clk.posedge
        update_i.next = 0
        yield clk.posedge
        for i in range(3):
            yield clk.posedge

        update_i.next = 1
        left_i.next = 10
        right_i.next = 11
        sam_i.next = 2
        flgs_i.next = 7
        yield clk.posedge
        update_i.next = 0
        yield clk.posedge
        for i in range(3):
            yield clk.posedge
            
        update_i.next = 1
        left_i.next = 10
        right_i.next = 11
        sam_i.next = 22
        flgs_i.next = 5
        yield clk.posedge
        update_i.next = 0
        yield clk.posedge
        for i in range(3):
            yield clk.posedge


        update_i.next = 1
        left_i.next = 10
        right_i.next = 11
        sam_i.next = 17
        flgs_i.next = 6
        yield clk.posedge
        update_i.next = 0
        yield clk.posedge
        for i in range(3):
            yield clk.posedge
            
        update_i.next = 1
        left_i.next = 10
        right_i.next = 11
        sam_i.next = 7
        flgs_i.next = 4
        yield clk.posedge
        update_i.next = 0
        yield clk.posedge
        for i in range(3):
            yield clk.posedge

        
         
        raise StopSimulation()

    return lift_step_1, clkgen, stimulus

tb = testbench()
tb.config_sim(trace=True)
tb.run_sim()
