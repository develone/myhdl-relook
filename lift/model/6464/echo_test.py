#!/usr/bin/env python3

''' 
Jan Marjanovic, 2015

A extremely simple example of co-simulation of MyHDL and Verilog code.
'''

import os
from myhdl import Cosimulation, Simulation, Signal, delay, always, intbv, now

def clk_driver(i_clk, period=10):
    ''' Clock driver '''
    @always(delay(period//2))
    def driver():
        i_clk.next = not i_clk

    return driver
     
def echo(i_clk,uart_rx,uart_tx):

	
    
    ''' A Cosimulation object, used to simulate Verilog modules '''
    os.system('iverilog -o uu echotest.v echo_top.v')
    return Cosimulation('vvp -m ./myhdl.vpi uu', i_clk=i_clk, uart_rx=i_uart_rx, uart_tx=o_uart_tx)

 
 

clk = Signal(0)
i_clk = Signal(0)
 
uart_rx = Signal(0) 
uart_tx = Signal(0)
i_uart_rx = Signal(0) 
o_uart_tx = Signal(0)

clk_driver_inst = clk_driver(i_clk)
echotest_inst = echo(i_clk,uart_rx,uart_tx)
 
sim = Simulation(clk_driver_inst, echotest_inst)
sim.run(200)
