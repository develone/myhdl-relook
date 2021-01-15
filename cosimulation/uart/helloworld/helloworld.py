import os
from myhdl import Cosimulation, Simulation, Signal, delay, always, intbv, now


def clk_driver(i_clk, period=10):
    ''' Clock driver '''
    @always(delay(period//2))
    def driver():
        i_clk.next = not i_clk

    return driver


def helloworld(i_clk, o_uart_tx):
    ''' A Cosimulation object, used to simulate Verilog modules '''
    os.system('iverilog -o helloworld.vvp helloworld.v helloworld_tb.v')
    return Cosimulation('vvp -m ./myhdl.vpi helloworld.vvp', i_clk=i_clk, o_uart_tx=o_uart_tx)
    
def checker(i_clk, o_uart_tx):
    ''' Checker which prints the value of counter at posedge '''
    @always(i_clk.posedge)
    def check():
        print('from checker, time=', now(), ' o_uart_=', o_uart_tx)

    return check
i_clk = Signal(0)
o_uart_tx = Signal(0)

clk_driver_inst = clk_driver(i_clk)
helloworld_inst = helloworld(i_clk, o_uart_tx)
checker_inst = checker(i_clk, o_uart_tx)

sim = Simulation(clk_driver_inst, helloworld_inst, checker_inst)
sim.run(200000)
