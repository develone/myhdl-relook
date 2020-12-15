import myhdl
from myhdl import *
from PIL import Image
from signed2twoscomplement import signed2twoscomplement
from ram import ram
W0 = 15
im = Image.open("red-32.pgm")
pix = im.load()
w, h = im.size
m = list(im.getdata())
m = [m[i:i+im.size[0]] for i in range(0, len(m), im.size[0])]
#print m[0][0], m[0][1], m[0][2], m[0][3], m[0][4], m[0][5], m[0][6], m[0][7]
W0 = 15
ramsize = 1024
AZ = 10

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
dout = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
din = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
addr = Signal(intbv(0)[AZ:])
we = Signal(bool(0))
douto = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
dino = Signal(intbv(0, min=-(2**(W0)), max=(2**(W0))))
addro = Signal(intbv(0)[AZ:])
weo = Signal(bool(0))


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
def testbench(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o, x, z, dout, din, addr, we, douto, dino, addro, weo ):
	inst_0 = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)
	inst_1 = signed2twoscomplement(clk, x, z)
	ramsize = 1024
	ram_2 = ram(dout, din, addr, we, clk, depth=ramsize)
	ram_3 = ram(douto, dino, addro, weo, clk, depth=ramsize)
	@always(delay(10))
	def clkgen():
		clk.next = not clk
    
	@instance
	def stimulus():
		
		#print m[0][0], m[0][1], m[0][2], m[0][3] 
		addr.next = 0
		yield clk.posedge
		
		we.next = 0
		yield clk.posedge
		
		print m[0][0:29]
		for i in range(30):
			din.next = m[0][i]
			yield clk.posedge
			
			
			addr.next = i
			yield clk.posedge
			
			we.next = 1
			yield clk.posedge
			
			we.next = 0
			yield clk.posedge
			
			
		we.next = 0
		yield clk.posedge
		
		addr.next = 1
		yield clk.posedge
		
		#m[0][1]
		left_i.next = dout
		yield clk.posedge
		
		#m[0][2]
		addr.next = 2
		yield clk.posedge
		
		sam_i.next = dout
		yield clk.posedge
		
		addr.next = 3
		yield clk.posedge

		#m[0][3]
		right_i.next = dout
		yield clk.posedge

		ap = (m[0][0] - m[0][1])
		print ap
				
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
		
		addro.next = 0
		yield clk.posedge
		
		weo.next = 1
		yield clk.posedge
		
		dino.next = res_o
		yield clk.posedge
		
		weo.next = 0
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
		
		addro.next = 1
		yield clk.posedge
		
		weo.next = 1
		yield clk.posedge
		
		dino.next = res_o
		yield clk.posedge
		
		weo.next = 0
		yield clk.posedge
				
		raise StopSimulation
	return instances()
					
def convert_lift_step(hdl):
	lift_step_1 = lift_step(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o)
	lift_step_1.convert(hdl=hdl)

convert_lift_step(hdl='Verilog')
tb = testbench(left_i, sam_i, right_i, flgs_i, update_i, clk, res_o, update_o, x, z, dout, din, addr, we, douto, dino, addro, weo)
tb.config_sim(trace=True)
tb.run_sim()
