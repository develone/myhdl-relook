module tb_signed2twoscomplement;

reg clk;
reg [15:0] x;
wire [14:0] z;

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
