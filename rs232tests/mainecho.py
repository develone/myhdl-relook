from myhdl import *
import RS232_Norbo
import RS232Programmer
#from RS232Programmer import RS232Programmer
from pwruprst import pwruprst
from rs232sig import *
from updateecho import updateecho
 

from pps import pps
from rom import rom

t_State = enum('IDLE','READ_INFO_DATA', 'INFO_DATA_HERE','WAIT_ONE_CLK', 'RECEIVE_IT')
t_state1 = enum('IDLE','DEL0','DEL1','DEL2','DEL3','DEL4','DEL5')
state1 = Signal(t_state1.IDLE)

"""
yosys -l simple.log -p 'synth_ice40 -blif mainecho.blif -json mainecho.json' mainecho.v
nextpnr-ice40 --hx8k --pcf mainecho.pcf --json mainecho.json --asc mainecho.asc
icetime -d hx8k -c 100 mainecho.asc
icepack mainecho.asc mainecho.bin
"""


@block
def mainecho(iClk,iRX,oTX):

    pwruprst_inst = pwruprst(iClk,iRst,pwrup)
    
    pps0_inst=pps(iClk,ppscounter,sig)
    
    #rom0_inst=rom(rom_dout,rom_addr,CONTENT)
    
     
    
    updateecho0_inst=updateecho(iClk,iRst,iData, WriteEnable,ldData,oWrBuffer_full,obusy)
    
    #transbuff0_inst = transbuff(iClk,iRst,WriteEnable,ldData,sig,rom_dout,rom_addr,CONTENT,oldData)

    rs232_module_inst=RS232_Norbo.RS232_Module(iClk,iRst,iRX,oTX, \
        iData,WriteEnable, oWrBuffer_full,oData,read_addr, \
        rx_addr,Clkfrequenz=Clk_f, \
        Baudrate=BAUDRATE,RX_BUFFER_LENGTH=RX_BUFF_LEN,TX_BUFFER_LENGTH=TX_BUFF_LEN)
    """
    programmer_inst=RS232Programmer.RS232Programmer(iClk,iRst, \
        programmer_enable,oInfobyte,dout,addr_out,we, \
        oprog_Data_RS232,oprog_WriteEnable_RS232, \
        iprog_WrBuffer_full_RS232,oData,read_addr,rx_addr)"""
    return instances()

def convert_mainecho(hdl):

    mainecho_0 = mainecho(iClk,iRX,oTX)
    mainecho_0.convert(hdl=hdl)

@block
def test_bench():

    ##### Signal definitions #####

    ##### Instanziate RS232 Module #####
    main_0 = main(iClk,iRX,oTX)

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

        state1.next = t_state1.IDLE
        
        for i in range(1000000):
            yield iClk.posedge
        raise StopSimulation

    #return  clk_gen,Monitor,stimulus,rs232_instance,programmer_inst,rs232loopback,Monitor2#,Monitor_oTX
    return  clk_gen,Monitor,stimulus,main_0,rs232loopback,Monitor2#,Monitor_oTX


#convert_mainecho(hdl='Verilog')
"""
tb = test_bench()
tb.config_sim(trace=True)
tb.run_sim()"""

