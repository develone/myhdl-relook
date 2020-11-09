import myhdl
from myhdl import block, always, instance, Signal, ResetSignal, delay, enum
from fsm import framer_ctrl, t_state

ACTIVE_LOW = 0


def convert_fsm(hdl):
	sof = Signal(bool(0))
	sync_flag = Signal(bool(0))
	clk = Signal(bool(0))
	reset_n = ResetSignal(1, active=ACTIVE_LOW, isasync=True)
	state = Signal(t_state.SEARCH)
		
	frame_ctrl_0 = framer_ctrl(sof, state, sync_flag, clk, reset_n)
	frame_ctrl_0.convert(hdl=hdl)
	

		
convert_fsm(hdl='Verilog')
