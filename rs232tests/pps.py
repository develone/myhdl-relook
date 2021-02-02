from myhdl import *

from rs232sig import *


@block
def pps(iClk,ppscounter,sig):
	sighi=Signal(intbv(0)[8:])
	@always(iClk.posedge)
	def ppsi():

		
		
		if(ppscounter < ppsdel):
			ppscounter.next=ppscounter+1
			if (ppscounter<sighi):
				sig.next=1
			else:
				sig.next=0
				sighi.next=0
		else:
			
			ppscounter.next=0
			sig.next=1
			sighi.next=sighictn
			
	return ppsi
@block
def test_bench():
	interval = delay(10)
	@always(interval)
	def clk_gen():
		iClk.next=not iClk
	pps0_inst=pps(iClk,ppscounter,sig)
	
	@instance
	def stimulus():
		for i in range(ppsdel+200):
			yield iClk.posedge
		raise StopSimulation
	return  clk_gen,pps0_inst,stimulus
		
def convert_pps(hdl):
	pps0_inst=pps(iClk,ppscounter,sig)
	pps0_inst.convert(hdl=hdl)
#convert_pps(hdl='Verilog')
"""
tb = test_bench()
tb.config_sim(trace=True)
tb.run_sim()"""	
