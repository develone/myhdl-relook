from myhdl import *
W0 = 15
ramsize = 32
AZ = 5

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

res_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
left_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
right_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
sam_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
flgs_i = Signal(intbv(0)[4:])
clk = Signal(bool(0))
update_i = Signal(bool(0))
update_o = Signal(bool(0))
x = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0-1))))
z = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0-1))))

dout_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
din_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
addr_i = Signal(intbv(0)[AZ:])
we_i = Signal(bool(0))

dout_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
din_o = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0-1))))
addr_o = Signal(intbv(0)[AZ:])
we_o = Signal(bool(0))

dout = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
din = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0-1))))
addr = Signal(intbv(0)[AZ:])
we = Signal(bool(0))

update1_i = Signal(bool(0))
update1_o = Signal(bool(0))
sub_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
first_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))
nd_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0-1))))

addrtoinc = Signal(intbv(0)[AZ:])
incaddr = Signal(intbv(0)[AZ:])
update2_i = Signal(bool(0))
update2_o = Signal(bool(0))

ldData=Signal(intbv(0)[8:])
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

     
    
dout=Signal(intbv(0)[32:])
addr_out=Signal(intbv(0)[32:])
we=Signal(bool(0))
oTX_programmer=Signal(bool(0))
oInfobyte=Signal(intbv(0)[8:])
 
    
    
oprog_Data_RS232=Signal(intbv(0)[8:])
oprog_WriteEnable_RS232=Signal(bool(0))
iprog_WrBuffer_full_RS232=Signal(bool(0))
programmer_enable=Signal(bool(1))

