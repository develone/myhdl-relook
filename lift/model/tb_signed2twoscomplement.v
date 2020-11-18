module tb_signed2twoscomplement;

reg clk;
reg [9:0] x;
wire [8:0] z;

initial begin
    $from_myhdl(
        clk,
        x
    );
    $to_myhdl(
        z
    );
end

signed2twoscomplement dut(
    clk,
    x,
    z
);

endmodule
