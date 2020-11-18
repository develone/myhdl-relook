module tb_fifo;

reg clk;
wire empty_r;
wire full_r;
reg enr_r;
reg enw_r;
wire [14:0] dataout_r;
reg [14:0] datain_r;

initial begin
    $from_myhdl(
        clk,
        enr_r,
        enw_r,
        datain_r
    );
    $to_myhdl(
        empty_r,
        full_r,
        dataout_r
    );
end

fifo dut(
    clk,
    empty_r,
    full_r,
    enr_r,
    enw_r,
    dataout_r,
    datain_r
);

endmodule
