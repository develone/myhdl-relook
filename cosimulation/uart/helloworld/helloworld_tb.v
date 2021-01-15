`timescale 1ns / 1ps
	
	module  helloworld_tb;
	
	
	reg i_clk;
	
	output wire o_uart_tx;
	
	
	helloworld dut(
		.i_clk(i_clk),
		
		.o_uart_tx(o_uart_tx)
	);
	
 
	initial
		begin
			$from_myhdl(i_clk);
			$to_myhdl(o_uart_tx);
	end
	
	initial
		begin
			$dumpfile("helloworld.vcd");
			$dumpvars(0, dut);
 	end
endmodule
