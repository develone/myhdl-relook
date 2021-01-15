`timescale 1ns / 1ps
	
	module  speechfifo_tb;
	
	
	reg i_clk;
	output wire o_uart_tx;
	
	speechfifo dut(
		i_clk,
		 
		o_uart_tx
	);
	

	initial
		begin
			$from_myhdl(i_clk);
			$to_myhdl(o_uart_tx);
	end	
	initial
		begin
			$dumpfile("speechfifo.vcd");
			$dumpvars(0, dut);
	end
endmodule
