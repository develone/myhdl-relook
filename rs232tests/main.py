from myhdl import *
import RS232_Norbo

from RS232Programmer import RS232Programmer
from pwruprst import pwruprst
t_State = enum('IDLE','READ_INFO_DATA', 'INFO_DATA_HERE','WAIT_ONE_CLK', 'RECEIVE_IT')

"""
yosys -l simple.log -p 'synth_ice40 -blif main.blif -json main.json' main.v


"""

Clk_f=100e6 #100 Mhz
BAUDRATE=230400
RX_BUFF_LEN=8

@block
def main(iClk,iRst,iRX,oTX,iData,WriteEnable,oWrBuffer_full,oData,read_addr,rx_addr, \
    pwrup,Clkfrequenz=Clk_f,Baudrate=BAUDRATE,RX_BUFFER_LENGTH=RX_BUFF_LEN):
	

    pwruprst_inst = pwruprst(iClk,iRst,pwrup)

    rs232_module_inst=RS232_Norbo.RS232_Module(iClk,iRst,iRX,oTX, iData,WriteEnable,  \
         oWrBuffer_full,oData,read_addr,rx_addr,Clkfrequenz=Clk_f,  \
         Baudrate=BAUDRATE,RX_BUFFER_LENGTH=RX_BUFF_LEN)

	
    return instances()

def convert_main(hdl):
    #Clk_f=100e6 #100 Mhz
    #BAUDRATE=230400
    ##### Signal definitions #####
    iData=Signal(intbv(0)[8:])
    oData=Signal(intbv(0)[8:])
    iClk=Signal(bool(0))
    iRst=Signal(bool(1))
    iRX=Signal(bool(1))
    oTX=Signal(bool(0))
    WriteEnable=Signal(bool(0))
    oWrBuffer_full=Signal(bool(0))
    read_addr=Signal(intbv(0,min=0,max=8))
    #RX_BUFF_LEN=8
    rx_addr=Signal(intbv(0,min=0,max=RX_BUFF_LEN))

    dout=Signal(intbv(0)[32:])
    addr_out=Signal(intbv(0)[32:])
    we=Signal(bool(0))
    oTX_programmer=Signal(bool(0))
    oInfobyte=Signal(intbv(0)[8:])
    #programmer_inst=RS232Programmer(iClk,iRst,oInfobyte,dout,addr_out,we, oTX,oTX_programmer, BAUDRATE=BAUDRATE,RX_BUFF_LEN=RX_BUFF_LEN,TX_BUFF_LEN=RX_BUFF_LEN,Clk_f=Clk_f)
    
    
    oprog_Data_RS232=Signal(intbv(0)[8:])
    oprog_WriteEnable_RS232=Signal(bool(0))
    iprog_WrBuffer_full_RS232=Signal(bool(0))
    programmer_enable=Signal(bool(1))
    pwrup=Signal(bool(1))
    main_0 = main(iClk,iRst,iRX,oTX, iData,WriteEnable,  \
		oWrBuffer_full,oData,read_addr,rx_addr,pwrup,Clkfrequenz=Clk_f,  \
		Baudrate=BAUDRATE,RX_BUFFER_LENGTH=RX_BUFF_LEN)
    main_0.convert(hdl=hdl)

@block    
def test_bench():
    ###### Constnats #####
    #Clk_f=100e6 #100 Mhz
    #BAUDRATE=230400
  
    ##### Signal definitions #####
    iData=Signal(intbv(0)[8:])
    oData=Signal(intbv(0)[8:])
    iClk=Signal(bool(0))
    iRst=Signal(bool(1))
    iRX=Signal(bool(1))
    oTX=Signal(bool(0))
    WriteEnable=Signal(bool(0))
    oWrBuffer_full=Signal(bool(0))
    read_addr=Signal(intbv(0,min=0,max=8))
    #RX_BUFF_LEN=8
    rx_addr=Signal(intbv(0,min=0,max=RX_BUFF_LEN))

    ##### Instanziate RS232 Module #####
    rs232_instance=RS232_Norbo.RS232_Module(iClk,iRst,iRX,oTX, iData,WriteEnable,  \
         oWrBuffer_full,oData,read_addr,rx_addr,Clkfrequenz=Clk_f,  \
         Baudrate=BAUDRATE,RX_BUFFER_LENGTH=RX_BUFF_LEN,TX_BUFFER_LENGTH=RX_BUFF_LEN)
    
    
    dout=Signal(intbv(0)[32:])
    addr_out=Signal(intbv(0)[32:])
    we=Signal(bool(0))
    oTX_programmer=Signal(bool(0))
    oInfobyte=Signal(intbv(0)[8:])
    #programmer_inst=RS232Programmer(iClk,iRst,oInfobyte,dout,addr_out,we, oTX,oTX_programmer, BAUDRATE=BAUDRATE,RX_BUFF_LEN=RX_BUFF_LEN,TX_BUFF_LEN=RX_BUFF_LEN,Clk_f=Clk_f)
    
    
    oprog_Data_RS232=Signal(intbv(0)[8:])
    oprog_WriteEnable_RS232=Signal(bool(0))
    iprog_WrBuffer_full_RS232=Signal(bool(0))
    programmer_enable=Signal(bool(1))
    
    programmer_inst=RS232Programmer(iClk,iRst,programmer_enable,oInfobyte, \
                       dout,addr_out,we, \
                       oprog_Data_RS232,oprog_WriteEnable_RS232, iprog_WrBuffer_full_RS232,oData,read_addr,rx_addr)
    
    
    #toVHDL(RS232Programmer,iClk,iRst,oInfobyte,dout,addr_out,we, oTX,oTX_programmer, BAUDRATE=BAUDRATE,RX_BUFF_LEN=RX_BUFF_LEN,TX_BUFF_LEN=RX_BUFF_LEN,Clk_f=Clk_f)
    
    ##### Convert to VHDL ######
    #toVHDL(RS232_Module,iClk,iRst,iRX,oTX, iData,WriteEnable, \
    #       oWrBuffer_full,oData,read_addr,rx_addr,Clkfrequenz=Clk_f,  \
    #       Baudrate=BAUDRATE,RX_BUFFER_LENGTH=RX_BUFF_LEN)
    
    interval = delay(10)
    @always(interval)
    def clk_gen():
      iClk.next=not iClk
    
    @always_comb
    def rs232loopback():
        iRX.next=oTX

    @instance
    def Monitor():
        #print "\t\tPortC:",PORTC_OUT,"Binary:" ,bin(PORTC_OUT,WORD_SZ) ##TODO bin is not supported in simulation
        while 1:
            yield we
            if we:
	      yield delay(0)
	      print "Data:\t",bin(dout),dout,"Addr:\t",addr_out
   
    @instance
    def Monitor2():
      #### wait until data is received #####
      count=0
      currentPos=0
      while 1:
        yield iClk.posedge
        yield delay(0)
        count=count+1
        if rx_addr!=read_addr:
          count=0
          #print "RXData:", oData, "\t\tBuffer Address:",read_addr
          #assert oData==currentPos
          if currentPos==255:
	    currentPos=0
	  else:
	    currentPos=currentPos+1
          #read_addr.next=(read_addr+1)%RX_BUFF_LEN

        #if Nothing is received for six possible complete RS232 transmissions
        # (8+2) means 8 Bits + 1 Startbit + 1 Stopbit
        if count>((Clk_f*1.0/BAUDRATE)*(8+2)*10):  
          break

    def Write_to_rs232_send_buffer(value):
      yield iClk.posedge
      while oWrBuffer_full:
	yield iClk.posedge
      iData.next=value
      if oWrBuffer_full:
        print "Value:",value,"\tNot written, RS232 Transmittbuffer has indiciated to be allready full. (by oWrBuffer_full)"
      
      WriteEnable.next=1
      yield iClk.posedge
      WriteEnable.next=0
    
    def TestTransmitReceive(testARRAY):
      #### Write some Bytes to the Sendbuffer #####
      for data in testARRAY:
        yield Write_to_rs232_send_buffer(data)
      
      for i in range(int(Clk_f/BAUDRATE)*10*(RX_BUFF_LEN+3)):
	yield iClk.posedge
    @instance
    def stimulus():
      #### Reseting #####
      iRst.next=1
      yield delay(50)
      iRst.next=0
      yield delay(50)
      iRst.next=1
      yield delay(50)
      
      #### Some Test Data ####
      testARRAY=[0x09]+range(256)+range(256)+[0x12]+range(256)+range(256)+range(256)+range(256) 
      print
      print "Running Test Array:",testARRAY
      print "#"*50
      yield TestTransmitReceive(testARRAY)
      

      
      #### Reseting #####
      print "Assert the reset"
      iRst.next=1
      yield delay(50)
      iRst.next=0
      yield delay(50)
      iRst.next=1
      yield delay(50)
      
      ### artificial reset of read_addr ####
      read_addr.next=0
      
      #### Some Test Data ####
      testARRAY=[0x09]+range(256)+range(256)+[0x09]+range(256)+range(256)
      print
      print "Running Test Array:",testARRAY
      print "#"*50
      yield TestTransmitReceive(testARRAY)
      
      print
      print "End of Simulation, simulation done!"
      raise StopSimulation

    return  clk_gen,Monitor,stimulus,rs232_instance,programmer_inst,rs232loopback,Monitor2#,Monitor_oTX    


#convert_main(hdl='Verilog')
tb = test_bench()

tb.config_sim(trace=True)
tb.run_sim()
