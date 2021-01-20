from myhdl import *
import RS232_Norbo
import RS232Programmer

def convert_RS232Programmer(hdl):
    ###### Constnats #####
    Clk_f=100e6 #100 Mhz
    BAUDRATE=230400
  
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
    RX_BUFF_LEN=8
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
    
    programmer_inst=RS232Programmer.RS232Programmer(iClk,iRst,programmer_enable,oInfobyte, \
                       dout,addr_out,we, \
                       oprog_Data_RS232,oprog_WriteEnable_RS232, iprog_WrBuffer_full_RS232,oData,read_addr,rx_addr)
    programmer_inst.convert(hdl=hdl)
    


convert_RS232Programmer(hdl='Verilog')
