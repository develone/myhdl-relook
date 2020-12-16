import myhdl
from myhdl import *
from PIL import Image
from signed2twoscomplement import signed2twoscomplement
from ram import ram
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
def testbench(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o, x, z, dout_i, din_i, addr_i, we_i, dout_o, din_o, addr_o, we_o ):
	inst_0 = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)
	inst_1 = signed2twoscomplement(clk, x, z)
	ramsize = 32
	ram_2 = ram(dout_i, din_i, addr_i, we_i, clk, depth=ramsize)
	ram_3 = ram(dout_o, din_o, addr_o, we_o, clk, depth=ramsize)
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
			 
		for i in range(32):
			din_i.next = m[0][i]
			yield clk.posedge
			
			
			addr_i.next = i
			yield clk.posedge
			
			we_i.next = 1
			yield clk.posedge
			
			we_i.next = 0
			yield clk.posedge
						
		we_i.next = 0
		yield clk.posedge
		
		addr_i.next = 1
		yield clk.posedge
		
		#m[0][1]
		left_i.next = dout_i
		yield clk.posedge
		
		#m[0][2]
		addr_i.next = 2
		yield clk.posedge
		
		sam_i.next = dout_i
		yield clk.posedge
		
		addr_i.next = 3
		yield clk.posedge

		#m[0][3]
		right_i.next = dout_i
		yield clk.posedge

		ap = (m[0][0] - m[0][1])
		print ap
		
		addr_o.next = 0
		yield clk.posedge
		
		we_o.next = 1
		yield clk.posedge
		
		din_o.next = ap
		yield clk.posedge
		
		we_o.next = 0
		yield clk.posedge
				
		flgs_i.next = 7
		yield clk.posedge
		
		update_i.next = 1
		yield clk.posedge
		
		
		
		update_i.next = 0
		yield clk.posedge
		
		x.next = res_o
		yield clk.posedge
		
		op = ap
		print op, ap
		
		left_i.next = ap
		yield clk.posedge
		
		sam_i.next = m[0][1]
		yield clk.posedge	

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
		
		addr_o.next = 16
		yield clk.posedge
		
		we_o.next = 1
		yield clk.posedge
		
		din_o.next = res_o
		yield clk.posedge
		
		we_o.next = 0
		yield clk.posedge
		
		#*********************
		print  m[0][4], m[0][5], m[0][6], m[0][7]
		
		left_i.next = m[0][3]
		yield clk.posedge
		
		sam_i.next = m[0][4]
		yield clk.posedge
		
		right_i.next = m[0][5]
		yield clk.posedge
		
		ap = (m[0][4] - m[0][5])
		print ap
		
		addr_o.next = 1
		yield clk.posedge
		
		we_o.next = 1
		yield clk.posedge
		
		din_o.next = ap
		yield clk.posedge
		
		we_o.next = 0
		yield clk.posedge
		
		
		flgs_i.next = 7
		yield clk.posedge
		
		update_i.next = 1
		yield clk.posedge
		
		update_i.next = 0
		yield clk.posedge
		
		x.next = res_o
		yield clk.posedge
		
		left_i.next = 8	#question
		yield clk.posedge
		
		sam_i.next = m[0][3]
		yield clk.posedge
		
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
		
		addr_o.next = 17
		yield clk.posedge
		
		we_o.next = 1
		yield clk.posedge
		
		din_o.next = res_o
		yield clk.posedge
		
		we_o.next = 0
		yield clk.posedge
				
		raise StopSimulation
	return instances()
					
def convert_lift_step(hdl):
	lift_step_1 = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)
	lift_step_1.convert(hdl=hdl)

convert_lift_step(hdl='Verilog')
tb = testbench(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o, x, z, dout_i, din_i, addr_i, we_i, dout_o, din_o, addr_o, we_o)
tb.config_sim(trace=True)
tb.run_sim()
