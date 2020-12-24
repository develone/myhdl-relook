from myhdl import *
W0 = 15
ramsize = 32
AZ = 5

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
