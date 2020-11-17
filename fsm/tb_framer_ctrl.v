module tb_framer_ctrl;

wire sof;
wire [1:0] state;
reg sync_flag;
reg clk;
reg reset_n;

initial begin
    $from_myhdl(
        sync_flag,
        clk,
        reset_n
    );
    $to_myhdl(
        sof,
        state
    );
end
initial begin
    $dumpfile("counter_top.vcd");
    $dumpvars();
end

framer_ctrl dut(
    sof,
    state,
    sync_flag,
    clk,
    reset_n
);

endmodule
