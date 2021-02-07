import os
from myhdl import Cosimulation, Simulation, Signal, delay, always, intbv, now

iClk=Signal(0)
iRX=Signal(0)
oTX=Signal(0)

def clk_driver(iClk, period=10):
    ''' Clock driver '''
    @always(delay(period//2))
    def driver():
        iClk.next = not iClk
    return driver

def checker(iClk,iRX,oTX):
    ''' Checker which prints the value of counter at posedge '''
    @always(iClk.posedge)
    def check():
        print('from checker, time=', now(), ' oTX=', oTX)

    return check

def echo(iClk,iRX,oTX):
    os.system('iverilog -o echo mainecho.v tb_mainecho.v')
    return Cosimulation('vvp -m ./myhdl.vpi echo',iClk=iClk,iRX=iRX,oTX=oTX)

clk_driver_inst = clk_driver(iClk)
echo_inst = echo(iClk,iRX,oTX)
checker_inst = checker(iClk,iRX,oTX)

sim = Simulation(clk_driver_inst,echo_inst, checker_inst)
sim.run(200)
