from myhdl import *
from rs232sig import *

t_state1 = enum('IDLE','DEL0','DEL1','DEL2','DEL3','DEL4','DEL5')
state1 = Signal(t_state1.IDLE)

from rom import rom

"""
The signal lcl_Rx_addr=Signal(intbv(0,min=0,max=RX_BUFF_LEN))
is used to compare with 
if(oRx_addr==lcl_Rx_addr):
The RX_BUFF_LEN is set to 8 
oRx_addr was added to instianate of updateecho
updateecho(iClk,iRst,iData, WriteEnable,ldData,oWrBuffer_full,obusy,oData,read_addr,oRx_addr)
=== mainecho ===

   Number of wires:                494
   Number of wire bits:           1282
   Number of public wires:         494
   Number of public wire bits:    1282
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:               1064
     SB_CARRY                      218
     SB_DFF                          8
     SB_DFFE                       233
     SB_DFFER                       74
     SB_DFFR                         9
     SB_DFFS                         2
     SB_DFFSR                       32
     SB_DFFSS                        2
     SB_LUT4                       486
when both RX_BUFF_LEN=8 & TX_BUFF_LEN=8
=== mainecho ===

   Number of wires:                294
   Number of wire bits:            733
   Number of public wires:         294
   Number of public wire bits:     733
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:                687
     SB_CARRY                      117
     SB_DFF                          8
     SB_DFFE                       137
     SB_DFFER                       70
     SB_DFFR                         9
     SB_DFFS                         2
     SB_DFFSR                       32
     SB_DFFSS                        2
     SB_LUT4                       310
1 warning, 0 errors
mainecho.asc
// Reading input .asc file..
// Reading 8k chipdb file..
// Creating timing netlist..
// Timing estimate: 7.98 ns (125.26 MHz)
// Checking 10.00 ns (100.00 MHz) clock constraint: PASSED.
main.asc
// Reading input .asc file..
// Reading 8k chipdb file..
// Creating timing netlist..
// Timing estimate: 8.33 ns (119.99 MHz)
// Checking 10.00 ns (100.00 MHz) clock constraint: PASSED.
"""

    
    
@block
def updateecho(iClk,iRst,iData, WriteEnable,ldData,oWrBuffer_full,obusy,oData,read_addr,oRx_addr):
 
    lcl_Rx_addr=Signal(intbv(0,min=0,max=RX_BUFF_LEN))
    @always(iClk.posedge,iRst.negedge)
    def rtl ():
        if(iRst==0):
            iData.next=0
            ldData.next=0
            WriteEnable.next=0
            read_addr.next=0
            obusy.next=0
            lcl_Rx_addr.next=0
            state1.next = t_state1.IDLE
        else:

            state1.next = t_state1.IDLE
            if (state1 == t_state1.IDLE):
                if(oRx_addr==lcl_Rx_addr):
                    state1.next = t_state1.IDLE
                else:
                    if((not WriteEnable) and (not oWrBuffer_full)):
                        ldData.next=oData
                        lcl_Rx_addr.next=oRx_addr
                        obusy.next=1
                        state1.next = t_state1.DEL0
                    else:
                        state1.next = t_state1.IDLE
                    
            elif (state1 == t_state1.DEL0):
                read_addr.next=(read_addr+1)%RX_BUFF_LEN 
                state1.next = t_state1.DEL1
            elif (state1 == t_state1.DEL1):
                iData.next = ldData
                WriteEnable.next=1
                state1.next = t_state1.DEL2
            elif(state1 == t_state1.DEL2):
                WriteEnable.next=0

                state1.next = t_state1.DEL3

            
            elif (state1 == t_state1.DEL3):

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
  
  updateecho0=updateecho(iClk,iRst,iData, WriteEnable,ldData,oWrBuffer_full,obusy,oData,read_addr,oRx_addr)
  rom0=rom(rom_dout) 
  
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

def convert_updateecho(hdl):
    updateecho0=updateecho(iClk,iRst,iData, WriteEnable,ldData,oWrBuffer_full,obusy,oData,read_addr,oRx_addr)
    updateecho0.convert(hdl=hdl)
    
#convert_updateecho(hdl='Verilog')
"""
tb=testbench()
tb.config_sim(trace=True)
tb.run_sim()"""
 
