import os
path = os.path
import myhdl
from myhdl import *
from lift_step import lift_step
from signed2twoscomplement import signed2twoscomplement
from mux import mux_data
from ram import ram
from fifo import fifo
from rd_pc import pc_read

from PIL import Image
im = Image.open("lena_256.png")
pix = im.load()
w, h = im.size
m = list(im.getdata())
im.show()
#print m.__sizeof__()
m = [m[i:i+im.size[0]] for i in range(0, len(m), im.size[0])]
#print m
#print m[0][0], m[1][0],m[2][0],m[3][0],m[4][0],m[5][0],m[6][0]
#print m[248][0],m[249][0], m[250][0],m[251][0],m[252][0],m[253][0],m[254][0]
W0 = 9
dout = Signal(intbv(0)[W0:])
din = Signal(intbv(0)[W0:])
addr = Signal(intbv(0)[8:])

we = Signal(bool(0))
clk = Signal(bool(0))
we_in = Signal(bool(0))
we_1 = Signal(bool(0))
addr_in = Signal(intbv(0)[8:])
 
toLift_Step = Signal(intbv(0)[W0:])
data_in = Signal(intbv(0)[W0:])

pc_data_in = Signal(intbv(0)[2:])
pc_data_rdy = Signal(intbv(0)[2:])

 
z = Signal(intbv(0)[W0:])
zfifo = Signal(intbv(0)[W0:])
read_pc_i = Signal(bool(0))
muxsel_i = Signal(bool(0))
muxaddrsel = Signal(intbv(0)[2:])

x = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0))))
xfifo = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0))))
res_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
left_i = Signal(intbv(0)[W0:])
right_i = Signal(intbv(0)[W0:])
sam_i = Signal(intbv(0)[W0:])
flgs_i = Signal(intbv(0)[4:])

update_i = Signal(bool(0))
update_o = Signal(bool(0))

SOF = Signal(bool(0))
syncFlag = Signal(bool(0))
rst_fsm = Signal(bool(1))

addr_left = Signal(intbv(0)[8:])
addr_sam = Signal(intbv(0)[8:])
addr_rht = Signal(intbv(0)[8:])
do_first = Signal(bool(0))
end_of_col = Signal(bool(0))
'''data from usb hostio'''
pc_data_in = Signal(intbv(0)[2:])
pc_data_rdy = Signal(intbv(0)[2:])

data_pc_in  = Signal(bool(0))

addr_in_toLift_Step = Signal(intbv(0)[8:])
del_ctn = Signal(intbv(0)[8:])
t_State = enum('INIT', 'ODD_L', 'ODD_S', 'ODD_R', 'RD_RAM_LF', 'RD_RAM_SA', 'RD_RAM_RT', 'LIFT', 'LIFT_EXE', 'LIFT_RD', 'LIFT_WR', 'LIFT_DEL1', 'LIFT_DEL2', 'LIFT_DEL3', 'EVEN_L', 'EVEN_S', 'EVEN_R',   'RD_FIFO', 'RD_FIFO_DEL', 'RD_FIFO_DEL1', 'RD_FIFO_DEL2', 'RD_FIFO_DEL3','RD_FIFO_DEL4','RD_FIFO_DEL5','RD_FIFO_DEL6','RD_FIFO_DEL7','RD_FIFO_DEL8','DONE', encoding="one_hot")
state = Signal(t_State.INIT)

reset_dly_c = 10
ASZ = 8
DSZ = W0
NO = bool(0)
YES = bool(1)

clk = Signal(bool(0))

enw_r = Signal(bool(0))
enr_r = Signal(bool(0))
empty_r = Signal(bool(0))
full_r = Signal(bool(0))
dataout_r = Signal(intbv(0)[DSZ:])
datain_r = Signal(intbv(0)[DSZ:])

enw_ro = Signal(bool(0))
enr_ro = Signal(bool(0))
empty_ro = Signal(bool(0))
full_ro = Signal(bool(0))
dataout_ro = Signal(intbv(0)[DSZ:])
datain_ro = Signal(intbv(0)[DSZ:])
'''
enw_x = Signal(bool(0))
enr_x = Signal(bool(0))
empty_x = Signal(bool(0))
full_x = Signal(bool(0))
dataout_x = Signal(intbv(0)[DSZ:])
datain_x = Signal(intbv(0)[DSZ:])
'''
readptr = Signal(intbv(0)[ASZ:])
writeptr = Signal(intbv(0)[ASZ:])
mem = [Signal(intbv(0)[DSZ:]) for ii in range(2**ASZ)]
# INIT, READ_DATA, DONE = range(3)

ACTIVE_LOW = bool(0)



 
@block
def Odd_Even_Fsm(state, clk, rst_fsm, addr_left, muxsel_i, addr_sam, addr_rht, muxaddrsel, we_1, dout, left_i, sam_i, right_i, do_first, x, z, flgs_i, update_i, res_o, update_o, end_of_col, addr_in, xfifo, enr_r, enw_r, del_ctn ):

    @always(clk.posedge, rst_fsm.negedge)
    def FSM():
        if rst_fsm == ACTIVE_LOW:
            addr_left.next = 0
            addr_sam.next = 1
            addr_rht.next = 2
            do_first.next = 0
            flgs_i.next = 7
            end_of_col.next = 0
            #enr_r.next = 0
            #enw_r.next = 0
            addr_in.next = 0     
            state.next = t_State.INIT
        else:
            if state == t_State.INIT:
                we_in.next = 1
                muxsel_i.next = 1
                enr_r.next = 1 
                state.next = t_State.RD_FIFO
            elif state == t_State.ODD_L:
                if (muxsel_i == 0):
                    if ((addr_left < 254) ):
                        if (addr_left == 0) and (do_first == 0):
                            ''' do_first goes hi to execute first location'''
                            #do_first.next = 1
                            addr_left.next = 0
                            muxaddrsel.next = 0
                            we_1.next = 0
                            state.next = t_State.RD_RAM_LF

                        else:
			    
			    addr_left.next = addr_left + 2
                            muxaddrsel.next = 0
                            we_1.next = 0
                            state.next = t_State.RD_RAM_LF
                    
            elif state == t_State.ODD_S:
                    if (addr_sam < 254) :
                        if (addr_sam == 1)and (do_first == 0):
                            addr_sam.next = 1
                            muxaddrsel.next = 1
                            we_1.next = 0
                            state.next = t_State.RD_RAM_SA
                        else:
                            addr_sam.next = addr_sam + 2
                            muxaddrsel.next = 1
                            we_1.next = 0
                            state.next = t_State.RD_RAM_SA
            elif state == t_State.ODD_R:
                if (muxsel_i == 0):
                     if (addr_rht < 254):
                        if (addr_rht == 2)and (do_first == 0):
                            do_first.next = 1
                            addr_rht.next = 2
                            muxaddrsel.next = 2
                            we_1.next = 0
                            state.next = t_State.RD_RAM_RT
                        else:
                            addr_rht.next = addr_rht + 2
                            muxaddrsel.next = 2
                            we_1.next = 0
                            state.next = t_State.RD_RAM_RT
                     else:
                        addr_left.next = 1
                        addr_sam.next = 2
                        addr_rht.next = 3
                        do_first.next = 0
                        flgs_i.next = 6 
                        state.next = t_State.EVEN_L 
            elif state == t_State.EVEN_L:
                if (muxsel_i == 0):
                    if ((addr_left < 254)):
                        if (addr_left == 1)and (do_first == 0):

                            ''' do_first goes hi to execute first location'''
                            #do_first.next = 1
                            addr_left.next = 1
                            muxaddrsel.next = 0
                            we_1.next = 0
                            state.next = t_State.RD_RAM_LF

                        else:
			    
			    addr_left.next = addr_left + 2
                            muxaddrsel.next = 0
                            we_1.next = 0
                            state.next = t_State.RD_RAM_LF
 
            elif state == t_State.EVEN_S:
                    if (addr_sam < 254):
                        if (addr_sam == 2)and (do_first == 0):
                            addr_sam.next = 2
                            muxaddrsel.next = 1
                            we_1.next = 0
                            state.next = t_State.RD_RAM_SA
                        else:
                            addr_sam.next = addr_sam + 2
                            muxaddrsel.next = 1
                            we_1.next = 0
                            state.next = t_State.RD_RAM_SA
                    else:
                        addr_left.next = 1
                        addr_sam.next = 2
                        addr_rht.next = 3 
                        state.next = t_State.DONE 
            elif state == t_State.EVEN_R:

                if (muxsel_i == 0):
                     if (addr_rht < 254):
                        if (addr_rht == 3)and (do_first == 0):
                            do_first.next = 1
                            addr_rht.next = 3
                            muxaddrsel.next = 2
                            we_1.next = 0
                            state.next = t_State.RD_RAM_RT
                        else:
                            addr_rht.next = addr_rht + 2
                            muxaddrsel.next = 2
                            we_1.next = 0
                            state.next = t_State.RD_RAM_RT
                     else:
                        addr_left.next = 1
                        addr_sam.next = 2
                        addr_rht.next = 3 
                        state.next = t_State.DONE 
            elif state == t_State.DONE:
                end_of_col.next = 1 
                state.next = t_State.DONE
            elif state == t_State.RD_RAM_LF:
                left_i.next = dout
                if (flgs_i == 6):
                    state.next = t_State.EVEN_S
                else:
                    state.next = t_State.ODD_S
            elif state == t_State.RD_RAM_SA:
                sam_i.next = dout
                if (flgs_i == 6):
                    state.next = t_State.EVEN_R
                else:
                    state.next = t_State.ODD_R
            elif state == t_State.RD_RAM_RT:
                right_i.next = dout
                
                    
                state.next = t_State.LIFT
 
            elif state == t_State.LIFT:
                '''setting addr to sam'''
                #flgs_i.next = 7
                update_i.next = 1
                we_1.next = 1 
                muxaddrsel.next = 1 
               
                state.next = t_State.LIFT_EXE
            elif state == t_State.LIFT_EXE:
                
		muxaddrsel.next = 1       
                state.next = t_State.LIFT_RD
            elif state == t_State.LIFT_RD:
                muxaddrsel.next = 1
		x.next = res_o[W0:]       
                state.next = t_State.LIFT_WR
            elif state == t_State.LIFT_WR:
                muxaddrsel.next = 1
                #addr_sam.next = addr_sam + 1
		update_i.next = 0
                #we_1.next = 0        
                state.next = t_State.LIFT_DEL1
            elif state == t_State.LIFT_DEL1:
                muxaddrsel.next = 1
                #addr_sam.next = addr_sam + 1
		#update_i.next = 0
                #we_1.next = 0        
                state.next = t_State.LIFT_DEL2
            elif state == t_State.LIFT_DEL2:
                muxaddrsel.next = 1
                #addr_sam.next = addr_sam + 1
		#update_i.next = 0
                #we_1.next = 0
      
                state.next = t_State.LIFT_DEL3
            elif state == t_State.LIFT_DEL3:
                muxaddrsel.next = 1
                #addr_sam.next = addr_sam + 1
		#update_i.next = 0
                we_1.next = 0        
                state.next = t_State.ODD_L
            elif state == t_State.RD_FIFO:
                del_ctn.next = 0
                if (addr_in <= 254):
                    enr_r.next = 0
                    #xfifo.next = dataout_r[W0:]
                    state.next = t_State.RD_FIFO_DEL
                else:
                    muxsel_i.next = 0
                    enr_r.next = 0
                    we_in.next = 0
                    state.next = t_State.ODD_L
            elif state == t_State.RD_FIFO_DEL:
                    
                    xfifo.next = dataout_r[W0:]
                    state.next = t_State.RD_FIFO_DEL1
            elif state == t_State.RD_FIFO_DEL1:
                    #enr_r.next = 0
                    if (del_ctn < 2):
                        del_ctn.next = del_ctn + 1
                    else:
                        state.next = t_State.RD_FIFO_DEL7
            elif state == t_State.RD_FIFO_DEL2:
                    state.next = t_State.RD_FIFO_DEL3
            elif state == t_State.RD_FIFO_DEL3:
                    state.next = t_State.RD_FIFO_DEL4
            elif state == t_State.RD_FIFO_DEL4:
                    state.next = t_State.RD_FIFO_DEL5
            elif state == t_State.RD_FIFO_DEL5:
                     
                    state.next = t_State.RD_FIFO_DEL6
            elif state == t_State.RD_FIFO_DEL6:
                    state.next = t_State.RD_FIFO_DEL7
            elif state == t_State.RD_FIFO_DEL7:
                    enr_r.next = 1 
                    state.next = t_State.RD_FIFO_DEL8
            elif state == t_State.RD_FIFO_DEL8:
                    #enr_r.next = 1
                    addr_in.next = addr_in.next + 1
                    state.next = t_State.RD_FIFO
            else:
                raise ValueError("Undefined state")
            
    return FSM
def top_odd_even(state, clk, rst_fsm, addr_left, muxsel_i, addr_sam, addr_rht,
 muxaddrsel, we_1, dout, left_i, sam_i, right_i, do_first, x, z, xfifo,
 zfifo, flgs_i, update_i, res_o, update_o, end_of_col, empty_r, full_r,
 enr_r, enw_r, dataout_r, datain_r , empty_ro, full_ro, enr_ro, enw_ro,
 dataout_ro, datain_ro, addr_in, del_ctn):
    instance_Odd_Even_Fsm = Odd_Even_Fsm (state, clk, rst_fsm, addr_left, muxsel_i, addr_sam, addr_rht, muxaddrsel, we_1, dout, left_i, sam_i, right_i, do_first, x, z, flgs_i, update_i, res_o, update_o, end_of_col, addr_in, xfifo, enr_r, enw_r, del_ctn)

    instance_ram = ram(dout, din, addr, we, clk)
    instance_mux_data =  mux_data(z, din, data_in, we_1, we, we_in, addr, addr_in, muxsel_i, muxaddrsel, addr_left, addr_sam, addr_rht,zfifo)
    instance_signed2twoscomplement = signed2twoscomplement(clk, x, z)
    instance_signed2twoscomplementfifo = signed2twoscomplement(clk, xfifo, zfifo)
    instance_lift_step = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)
    instance_pc_in = fifo(clk, empty_r, full_r, enr_r, enw_r, dataout_r, datain_r)
    instance_pc_out = fifo(clk, empty_ro, full_ro, enr_ro, enw_ro, dataout_ro, datain_ro)
    #instance_pd_read = pc_read(clk, data_in, toLift_Step, we_in, addr_in, muxsel_i, datactn_in, datactn, pc_data_in, pc_data_rdy ) 
    return instances()
@block
def testbench(state, clk, rst_fsm, addr_left, muxsel_i, addr_sam, addr_rht,
 muxaddrsel, we_1, dout, left_i, sam_i, right_i, do_first, x, z,xfifo,
 zfifo, flgs_i, update_i, res_o, update_o, end_of_col, empty_r, full_r,
 enr_r, enw_r, dataout_r, datain_r, empty_ro, full_ro, enr_ro, enw_ro,
 dataout_ro, datain_ro, addr_in, del_ctn ):
     
    instance_Odd_Even_Fsm = Odd_Even_Fsm (state, clk, rst_fsm, addr_left, muxsel_i, addr_sam, addr_rht, muxaddrsel, we_1, dout, left_i, sam_i, right_i, do_first, x, z, flgs_i, update_i, res_o, update_o, end_of_col, addr_in, xfifo, enr_r, enw_r, del_ctn)
   
    instance_ram = ram(dout, din, addr, we, clk)
    
    instance_mux_data =  mux_data(z, din, data_in, we_1, we, we_in, addr, addr_in, muxsel_i, muxaddrsel, addr_left, addr_sam, addr_rht,zfifo)

    instance_signed2twoscomplement = signed2twoscomplement(clk, x, z)

    instance_signed2twoscomplementfifo = signed2twoscomplement(clk, xfifo, zfifo)

    instance_lift_step = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)
    
    instance_pc_in = fifo(clk, empty_r, full_r, enr_r, enw_r, dataout_r, datain_r)
    
    instance_pc_out = fifo(clk, empty_ro, full_ro, enr_ro, enw_ro, dataout_ro, datain_ro)
    
    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        rst_fsm.next = 0
        yield clk.posedge

        muxsel_i.next = 0
        yield clk.posedge
        enr_r.next = 0
        yield clk.posedge
        enw_r.next = 0
        yield clk.posedge 

 
 
        datain_r.next = m[0][0]
        yield clk.posedge
        enw_r.next = 1
        yield clk.posedge
        for j in range(1,255):
            k = 0
            if (full_r == 0):
            	datain_r.next = m[j][k]
                yield clk.posedge
            #print ("%d %d %d %d %d") % (now(), j, enw_r, full_r, m[j][k])     
        enw_r.next = 0
        yield clk.posedge

 
        muxsel_i.next = 0
        yield clk.posedge
         
        rst_fsm.next = 1
        yield clk.posedge
        print ("%d muxsel_i %d rst_fsm %d") % (now(), muxsel_i, rst_fsm)
        
        while (end_of_col == 0):

            print ("time %d flgs %d left %d sam %d right %d ") % (now(), flgs_i, left_i, sam_i, right_i)
            print ("time %d addr %d din %d we %d ") % (now(), addr, din, we)   
            yield clk.posedge
            print ("%d ") % (now())
        print "end of col"

        muxsel_i.next = 1
        yield clk.posedge
        rst_fsm.next = 0
        yield clk.posedge
        addr_in.next = 0
        yield clk.posedge
        we_in.next = 0
        m[0][k] = dout
        datain_ro.next= m[0][k]
        yield clk.posedge
        print ("%d data to ram %d %d") % (now(), datain_ro, addr_in)
        addr_in.next = addr_in + 1
        yield clk.posedge

        enw_ro.next = 1
        yield clk.posedge
        for j in range(1,254):
            m[0][k] = dout
            datain_ro.next= m[j][k]
            yield clk.posedge
            addr_in.next = addr_in + 1
            print ("%d data to ram %d %d") % (now(), datain_ro, addr_in)
            yield clk.posedge
            enw_ro.next = 1
            yield clk.posedge  
        raise StopSimulation
    return instances()

def convert_Odd_Even_Fsm(hdl):
	Odd_Even_Fsm_1 = Odd_Even_Fsm(state, clk, rst_fsm, addr_left, muxsel_i, addr_sam, addr_rht, muxaddrsel, we_1, dout, left_i, sam_i, right_i, do_first, x, z, flgs_i, update_i, res_o, update_o, end_of_col, addr_in, xfifo, enr_r, enw_r, del_ctn )

	Odd_Even_Fsm_1.convert(hdl=hdl)




def iverilogtest(state, clk, rst_fsm, addr_left, muxsel_i, addr_sam, addr_rht,
 muxaddrsel, we_1, dout, left_i, sam_i, right_i, do_first, x, z,xfifo,
 zfifo, flgs_i, update_i, res_o, update_o, end_of_col, empty_r, full_r,
 enr_r, enw_r, dataout_r, datain_r, empty_ro, full_ro, enr_ro, enw_ro,
 dataout_ro, datain_ro, addr_in, del_ctn):
 

    cmd = "iverilog -o odd_even_fsm top_odd_even.v tb_top_odd_even.v"
    os.system(cmd)
    def _test():
#        dut = Cosimulation("vvp -m ./myhdl.vpi const_assign", aBit=my_bit, aByte=my_byte)
#         dut = const_assign(aBit=my_bit, aByte=my_byte)
    	def _test():
            dut = Cosimulation("vvp -m ./myhdl.vpi odd_even_fsm", aBit=my_bit, aByte=my_byte)
#           dut = odd_even_fsm(aBit=my_bit, aByte=my_byte)

        @instance
        def stim():

            raise StopSimulation

        return dut, stim
def main():
    tb = testbench(state, clk, rst_fsm, addr_left, muxsel_i, addr_sam, addr_rht,
 muxaddrsel, we_1, dout, left_i, sam_i, right_i, do_first, x, z,xfifo,
 zfifo, flgs_i, update_i, res_o, update_o, end_of_col, empty_r, full_r,
 enr_r, enw_r, dataout_r, datain_r, empty_ro, full_ro, enr_ro, enw_ro,
 dataout_ro, datain_ro, addr_in, del_ctn)
    #convert_Odd_Even_Fsm(hdl='Verilog')
    tb.config_sim(trace=True)
    tb.run_sim()
    

    

    
    

if __name__ == '__main__':
    main()
    '''
    import os
from myhdl import *


def const_assign(aBit, aByte):

    b = Signal(bool(True)) # to avoid "myhdl.AlwaysCombError: sensitivity list is empty"

    @always_comb
    def logic():
        aBit.next = b
        aByte.next = 0x55

    return logic

def convert():
    my_bit = Signal(bool(0))
    my_byte = Signal(intbv(0)[8:])
    toVerilog(const_assign, my_bit, my_byte)

def test():
    my_bit = Signal(bool(0))
    my_byte = Signal(intbv(0)[8:])

    cmd = "iverilog -o const_assign const_assign.v tb_const_assign.v"
    os.system(cmd)

    def _test():
        dut = Cosimulation("vvp -m ./myhdl.vpi const_assign", aBit=my_bit, aByte=my_byte)
#         dut = const_assign(aBit=my_bit, aByte=my_byte)

        @instance
        def stim():
            print "-------------"

            yield delay(10)
            print "Expected ({}, {}), detected ({}, {})".format(True, 0x55, my_bit, my_byte)

            yield delay(10)
            print "Expected ({}, {}), detected ({}, {})".format(True, 0x55, my_bit, my_byte)

            yield delay(10)
            print "Expected ({}, {}), detected ({}, {})".format(True, 0x55, my_bit, my_byte)

            print "-------------"

            raise StopSimulation

        return dut, stim

    Simulation(_test()).run()

if __name__ == '__main__':
    convert()
    test()
    '''
