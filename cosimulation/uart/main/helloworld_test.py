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

def helloworld(iClk,iRX,oTX):
    os.system('iverilog -o helloworld main.v tb_main.v')
    return Cosimulation('vvp -m ./myhdl.vpi helloworld',iClk=iClk,iRX=iRX,oTX=oTX)

clk_driver_inst = clk_driver(iClk)
helloworld_inst = helloworld(iClk,iRX,oTX)
checker_inst = checker(iClk,iRX,oTX)

sim = Simulation(clk_driver_inst,helloworld_inst, checker_inst)
sim.run(2000000)
