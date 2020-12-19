import myhdl
from myhdl import *
from PIL import Image
from signed2twoscomplement import signed2twoscomplement
from ram import ram
from oneminuszero import oneminuszero
from addrbump import addrbump
W0 = 15
ramsize = 32
AZ = 5

im = Image.open("red-32.pgm")
pix = im.load()
w, h = im.size
m = list(im.getdata())
m = [m[i:i+im.size[0]] for i in range(0, len(m), im.size[0])]
#print m[0][0], m[0][1], m[0][2], m[0][3], m[0][4], m[0][5], m[0][6], m[0][7]



res_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
left_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
right_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
sam_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
flgs_i = Signal(intbv(0)[4:])
clk = Signal(bool(0))
update_i = Signal(bool(0))
update_o = Signal(bool(0))
x = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0))))
z = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0))))

dout_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
din_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
addr_i = Signal(intbv(0)[AZ:])
we_i = Signal(bool(0))

dout_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
din_o = Signal(intbv(0, min= -(2**(W0)) ,max= (2**(W0))))
addr_o = Signal(intbv(0)[AZ:])
we_o = Signal(bool(0))

update1_i = Signal(bool(0))
update1_o = Signal(bool(0))
sub_o = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
first_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
snd_i = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))

addrtoinc = Signal(intbv(0)[AZ:])
incaddr = Signal(intbv(0)[AZ:])
update2_i = Signal(bool(0))
update2_o = Signal(bool(0))
		
@block
def lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o):
	
	@always(clk.posedge)
	def rtl ():
		if (update_i == 1):
			update_o.next = 0
			if (flgs_i == 7):
				res_o.next = sam_i.signed() - ( (left_i.signed() >> 1) + (right_i.signed() >> 1) )
			elif (flgs_i == 5):
				res_o.next = sam_i.signed() + ( (left_i.signed() >> 1) + (right_i.signed() >> 1) )
			elif (flgs_i == 6):
				res_o.next = sam_i.signed() + ( (left_i.signed() + right_i.signed() + 2) >> 2 )
			elif (flgs_i == 4):
				res_o.next = sam_i.signed() - ( (left_i.signed() + right_i.signed() + 2) >> 2 )
		else:
				update_o.next = 1
	return rtl
	    
@block
def testbench(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o, x, z, dout_i, din_i, addr_i, we_i, dout_o, din_o, addr_o, we_o, first_i, snd_i,  update1_i, sub_o, update1_o, addrtoinc, update2_i, incaddr, update2_o):
	inst_0 = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)
	inst_1 = signed2twoscomplement(clk, x, z)
	ramsize = 32
	ram_2 = ram(dout_i, din_i, addr_i, we_i, clk, depth=ramsize)
	ram_3 = ram(dout_o, din_o, addr_o, we_o, clk, depth=ramsize)
	inst_3 = oneminuszero(first_i, snd_i,  update1_i, clk, sub_o, update1_o)
	addrbump_1 = addrbump(addrtoinc, update2_i, clk, incaddr, update2_o)
	
	@always(delay(10))
	def clkgen():
		clk.next = not clk
    
	@instance
	def stimulus():
		
		"""
		read a line from image
		set addr_i to begin of the read
		set we_i to 1 to enable write
		set din_i from pixel read
		set we_i to 0 after all pixels of the line are read
		""" 
		
		for i in range(0,31):
			din_i.next = m[0][i]
			yield clk.posedge
			
			we_i.next = 1
			yield clk.posedge
			
			we_i.next = 0
			yield clk.posedge
			
			addrtoinc.next = i
			yield clk.posedge
			
			update2_i.next = 1
			yield clk.posedge
				
			update2_i.next = 0
			yield clk.posedge
			
			addr_i.next = incaddr
			yield clk.posedge
					
		col = 0
		row = 0
		
		addr0 = 1
		addr1 = 0
		addr2 = 0				
		for row in range(0,1):
			
			
			
			#ap = (m[0][0] - m[0][1]) ap = (m[0][8] - m[0][9])
			addr1 = row*4
			
			we_i.next = 0
			yield clk.posedge
			
			#addr0 1 5 9
			#addr2 starts at 0, 4, 8, 12
			#addr1 starts at 0, 1, 2, 3  
			addr_i.next = addr1
			yield clk.posedge
			
			#m[0][0]
			#read addr 0 as the first_i addr 0 & left_i addr 1 of ram used for input
			first_i.next = dout_i
			yield clk.posedge
			
			addrtoinc.next = row
			yield clk.posedge
			
			update2_i.next = 1
			yield clk.posedge
				
			update2_i.next = 0
			yield clk.posedge
			
			addr_i.next = incaddr
			yield clk.posedge
			
			#addr2 = addr2 + 1********
			
			#addr2  at 1, 5, 9, 13 addr1  at 0, 1, 2, 3
			#reads addr 1 to snd_o & addr 1 to left_i
			#addr_i.next = addr2**********
			#yield clk.posedge************
						
			#m[0][1]
			#read addr 1
			snd_i.next = dout_i
			yield clk.posedge			
			
			update1_i.next = 1
			yield clk.posedge
				
			update1_i.next = 0
			yield clk.posedge
			 
			x.next = sub_o
			yield clk.posedge		 
		
			we_o.next = 1
			yield clk.posedge

			din_o.next = sub_o
			yield clk.posedge
		
			we_o.next = 0
			yield clk.posedge
			
		
			#m[0][1]
			#addr 1 to left_i
			left_i.next = dout_i
			yield clk.posedge
			
			addrtoinc.next = addr_i
			yield clk.posedge
			
			update2_i.next = 1
			yield clk.posedge
				
			update2_i.next = 0
			yield clk.posedge
			
			addr_i.next = incaddr
			yield clk.posedge
			
			#addr2 = addr2 + 1**********
			
			#addr1  at 0, 1, 2, 3, 4
			#addr2  at 2, 6, 10, 14
			
			#m[0][2]
			#addr_i.next = addr2***********
			#yield clk.posedge*************
		
			#addr 2 to sam_i
			
			sam_i.next = dout_i
			yield clk.posedge
			
			addrtoinc.next = addr_i
			yield clk.posedge
			
			update2_i.next = 1
			yield clk.posedge
				
			update2_i.next = 0
			yield clk.posedge
			
			addr_i.next = incaddr
			yield clk.posedge
					
			#addr2 = addr2 + 1****************

			#addr_i.next = addr2*************
			#yield clk.posedge***************
			
			#addr2  at 3, 7, 11, 15
			#m[0][3]
			right_i.next = dout_i
			yield clk.posedge
			
			addrtoinc.next = addr_i
			yield clk.posedge
			
			update2_i.next = 1
			yield clk.posedge
				
			update2_i.next = 0
			yield clk.posedge
			
			addr_i.next = incaddr
			yield clk.posedge
			
			#addr2 = addr2 + 1
			#addr2 now at 0 4 8 12 
							
			flgs_i.next = 7
			yield clk.posedge
		
			update_i.next = 1
			yield clk.posedge
				
			update_i.next = 0
			yield clk.posedge
			 
			x.next = res_o
			yield clk.posedge
			
			print flgs_i,z
			#op = ap
			#print op, ap, i
		
			left_i.next = sub_o
			yield clk.posedge
		
			#addr0 to sam_i
			
			we_i.next = 0
			yield clk.posedge
			
			addr_i.next = addr0
			yield clk.posedge
			
			#sam_i.next = m[row][i+1]
			sam_i.next = dout_i
			yield clk.posedge
			
			addr0 = addr0 + 4	
			
			#right_i gets the result of hi pass
			right_i.next = res_o
			yield clk.posedge
		
			flgs_i.next = 6
			yield clk.posedge
		
			update_i.next = 1
			yield clk.posedge
		
			update_i.next = 0
			yield clk.posedge
			
			
			x.next = res_o
			yield clk.posedge
			
			#setting addr1 to save lo pass
			#addr starts at 16, 17, 18, 19
			addr1 = addr1 + 16
			
			addr_o.next = addr1
			yield clk.posedge
			
			
		
			we_o.next = 1
			yield clk.posedge
		
			din_o.next = res_o
			yield clk.posedge
		
			we_o.next = 0
			yield clk.posedge
			for col in range(1,4):
				print col
			
			
			 
			
		raise StopSimulation
	return instances()
					
def convert_lift_step(hdl):
	lift_step_1 = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)
	lift_step_1.convert(hdl=hdl)

convert_lift_step(hdl='Verilog')
tb = testbench(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o, x, z, dout_i, din_i, addr_i, we_i, dout_o, din_o, addr_o, we_o, first_i, snd_i,  update1_i, sub_o, update1_o, addrtoinc, update2_i, incaddr, update2_o)
tb.config_sim(trace=True)
tb.run_sim()
