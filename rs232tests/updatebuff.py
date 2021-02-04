from myhdl import *
from rs232sig import *

t_state1 = enum('IDLE','DEL0','DEL1','DEL2','DEL3','DEL4','DEL5')
state1 = Signal(t_state1.IDLE)

from rom import rom



    
    
@block
def updatebuff(iClk,iRst,iData,WriteEnable,ldData,oWrBuffer_full,obusy,rom_dout,rom_addr,CONTENT):

    @always(iClk.posedge,iRst.negedge)
    def rtl ():
        if(iRst==0):
            iData.next=0
            ldData.next=0
            WriteEnable.next=0
            read_addr.next=0
            obusy.next=0
            state1.next = t_state1.IDLE
        else:

            state1.next = t_state1.IDLE
            if (state1 == t_state1.IDLE):
                 
                if((not WriteEnable) and (not oWrBuffer_full)):
                   
                    ldData.next=rom_dout
                    obusy.next=1
                        
                    state1.next = t_state1.DEL0
            elif (state1 == t_state1.DEL0):
                 
                state1.next = t_state1.DEL1
            elif (state1 == t_state1.DEL1):
                iData.next = ldData
                WriteEnable.next=1
                state1.next = t_state1.DEL2
            elif(state1 == t_state1.DEL2):
                WriteEnable.next=0
                if(rom_addr < 11):
                
                    rom_addr.next=(rom_addr+1)
                    state1.next = t_state1.DEL3
                else:
                    rom_addr.next=0
                    state1.next = t_state1.IDLE
            
            elif (state1 == t_state1.DEL3):
                WriteEnable.next=0

                state1.next = t_state1.DEL4
            
            elif (state1 == t_state1.DEL4):
                if(not sig):
                     
                    state1.next = t_state1.DEL4
                else:
                     
                    state1.next = t_state1.DEL5
                
                 
            else:
                if(state1 == t_state1.DEL5):
                    

                    obusy.next=0
                    state1.next = t_state1.IDLE
                
 
    return rtl


@block
def testbench():
  
  updatebuff0=updatebuff(iClk,iRst,iData,WriteEnable,ldData,oWrBuffer_full,obusy,rom_dout,rom_addr,CONTENT)
  rom0t=rom(rom_dout,rom_addr,CONTENT) 
  
  @always(delay(10))
  def clkgen():
    iClk.next = not iClk
    
  @instance
  def stimulus():
    iRst.next=1
    yield iClk.posedge
    iRst.next=0
    yield iClk.posedge
    iRst.next=1
    yield iClk.posedge
    
    state1.next = t_state1.IDLE
    yield iClk.posedge
    
    if(rom_addr==9):
        oWrBuffer_full.next = 1
    for i in range(10):
        print obusy
        yield iClk.posedge
    oWrBuffer_full.next = 0

    
    
    yield iClk.posedge
    
    ldData.next = rom_dout
    
    for i in range(4):
        print obusy
        yield iClk.posedge

    
    #rom_addr.next=10
    yield iClk.posedge
    
    ldData.next = rom_dout
    
    for i in range(4):
        print obusy
        yield iClk.posedge

    for i in range(1000):
      yield iClk.posedge
    raise StopSimulation
  return instances()

def convert_updatebuff(hdl):
    updatebuff0 = updatebuff(iClk,iRst,iData,WriteEnable,ldData,oWrBuffer_full,obusy,rom_dout,rom_addr,CONTENT)
    updatebuff0.convert(hdl=hdl)
    
#convert_updatebuff(hdl='Verilog')
"""
tb=testbench()
tb.config_sim(trace=True)
tb.run_sim()"""
 
