// Jan Marjanovic, 2015
//
// This is a top module which combines DUT and MyHDL signals

module echo_top;

reg i_clk = 0;
 
reg		uart_rx; 
output	wire	uart_tx;
 
echotest dut (.i_clk(i_clk), .i_uart_rx(uart_rx),.o_uart_tx(uart_tx));
initial begin
	$from_myhdl(i_clk,uart_rx);
	$to_myhdl(uart_tx);
	 
end

initial begin
    $dumpfile("echo_top.vcd");
    $dumpvars();
end

endmodule
