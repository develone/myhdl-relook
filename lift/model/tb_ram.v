module tb_ram;

wire [14:0] dout;
reg [14:0] din;
reg [7:0] addr;
reg we;
reg clk;

initial begin
    $from_myhdl(
        din,
        addr,
        we,
        clk
    );
    $to_myhdl(
        dout
    );
end

ram dut(
    dout,
    din,
    addr,
    we,
    clk
);

endmodule
