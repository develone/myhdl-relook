from myhdl import *

@block
def pwruprst(iClk,iRst,pwrup):

    @always(iClk.posedge)
    def logic2():

        if((iRst==1)and(pwrup==40)):
            iRst.next=0

        else:
            if(pwrup<=60):
                pwrup.next = pwrup+1
        if(pwrup==60):
            iRst.next=1

    return logic2

def convert_pwruprst(hdl):
    iClk=Signal(bool(0))
    iRst=Signal(bool(1))
    pwrup=Signal(intbv(0)[6:])
    pwruprst_1 = pwruprst(iClk,iRst,pwrup)

    pwruprst_1.convert(hdl=hdl)

#convert_pwruprst(hdl='Verilog')

