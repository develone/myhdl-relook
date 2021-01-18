from myhdl import *
#from constsig import *
from PIL import Image

im = Image.open("red-32.pgm")
pix = im.load()
w, h = im.size
m = list(im.getdata())
m = [m[i:i+im.size[0]] for i in range(0, len(m), im.size[0])]
iClk=Signal(bool(0))
ldData=Signal(intbv(0)[8:])
iData=Signal(intbv(0)[8:])
WriteEnable=Signal(bool(0))
@block
def updatebuff(iClk, iData, WriteEnable,ldData):
	delay = Signal(intbv(0)[4:])
	
	@always(iClk.posedge)
	def rtl ():
	  iData.next = ldData
	  if(WriteEnable==0):
	    WriteEnable.next=1
	  else:
	    WriteEnable.next=0
	
	return rtl
@block		
def testbench(clk, iData, WriteEnable,ldData):
  
  updatebuff_1 = updatebuff(iClk, iData, WriteEnable,ldData)
  
  @always(delay(10))
  def clkgen():
    clk.next = not clk
    
  @instance
  def stimulus():
    ldData.next = 0x41
    yield clk.posedge

    ldData.next = 0x39
    yield clk.posedge
    
    for i in range(1000):
      yield clk.posedge

    raise StopSimulation
  return instances()
					
def convert_updatebuff(hdl):
	updatebuff_1 = updatebuff(iClk, iData, WriteEnable,ldData)
	updatebuff_1.convert(hdl=hdl)

convert_updatebuff(hdl='Verilog')
tb = testbench(iClk, iData, WriteEnable,ldData)
tb.config_sim(trace=True)
tb.run_sim()
 
