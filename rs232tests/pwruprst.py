from myhdl import *

@block
def pwruprst(iClk,iRst,pwrup):
	
	@always(iClk.posedge)
	def logic2():
		if((iRst==1)and(pwrup==1)):
			iRst.next=0
			pwrup.next=0
		if(pwrup==0):
			iRst.next=1
		
	return logic2

def convert_pwruprst(hdl):
	iClk=Signal(bool(0))
	iRst=Signal(bool(1))
	pwrup=Signal(bool(1))
	pwruprst_1 = pwruprst(iClk,iRst,pwrup)
	 
	pwruprst_1.convert(hdl=hdl)

#convert_pwruprst(hdl='Verilog')

