from myhdl import *
#from jpeg_constants import *
import  random
from PIL import Image
im = Image.open("red-sub.pgm")
pix = im.load()
w, h = im.size
m = list(im.getdata())
im.show()
m = [m[i:i+im.size[0]] for i in range(0, len(m), im.size[0])]

W0 = 9
LVL0 = 16
@block
def m_flatten(matrix, flat):
	flat_i = ConcatSignal(*[mcol(W0,0) for mrow in matrix for mcol in mrow])
	@always_comb
	def rtl():
		flat.next = flat_i
	return rtl

@block
def test_flatten(matrix,flat):

	
	tbdut = m_flatten(matrix, flat)
	@instance
	def tbstim():
		yield delay(1)
		print(bin(flat, W0*LVL0))
		for j in range(512):
			j = random.randrange(-2**(W0-1),2**(W0-1))
			x = Signal(intbv(j, min=-2**(W0), max=2**(W0)))
			z = Signal(intbv(0)[W0:])
			z = m[0][0]
            #print ("%d %d %d %d %d") % (now(), j, enw_r, full_r, m[j][k])    
			for mrow in range(3,-1,-1):
				for mcol in range(3,-1,-1):
					z = x[W0:]
					print bin(z,W0)
					matrix[mrow][mcol].next = z

					print mrow, mcol, z.signed()

					if (flat[W0:0] == flat[W0*LVL0:(W0*LVL0)-W0]):
						print 'lsb', flat[W0:0],  flat[W0:0].signed(),'msb', flat[W0*LVL0:(W0*LVL0)-W0],  flat[W0*LVL0:(W0*LVL0)-W0].signed()

					yield delay(1)
					print(bin(flat, W0*LVL0))
			'''
			for mrow in range(3,-1,-1):
				for mcol in range(3,-1,-1):

					print bin(z,10)
					matrix[mrow][mcol].next = 0
					yield delay(1)
					print(bin(flat, 160))
			'''
	return instances()
#Simulation(test_flatten()).run()
matrix = [[Signal(intbv(0)[W0:]) for mcol in range(4)] for mrow in range(4)]
flat = Signal(intbv(0)[W0*LVL0:])
def convert(hdl):

	 
	m_flatten_0 = m_flatten(matrix, flat)
	m_flatten_0.convert(hdl=hdl)
	#toVerilog(m_flatten, matrix, flat)
	#toVHDL(m_flatten, matrix, flat)
#convert(hdl='Verilog')
tb = test_flatten( matrix, flat)
tb.config_sim(trace=True)
tb.run_sim()
