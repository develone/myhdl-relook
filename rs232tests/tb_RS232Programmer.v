module tb_RS232Programmer;

reg clk;
reg rst;
reg enable;
wire [7:0] oInfobyte;
wire [31:0] dout;
wire [31:0] addr_out;
wire we;
wire [7:0] iData_RS232;
wire WriteEnable_RS232;
reg oWrBuffer_full_RS232;
reg [7:0] oData_RS232;
wire [2:0] read_addr_RS232;
reg [2:0] rx_addr_RS232;

initial begin
    $from_myhdl(
        clk,
        rst,
        enable,
        oWrBuffer_full_RS232,
        oData_RS232,
        rx_addr_RS232
    );
    $to_myhdl(
        oInfobyte,
        dout,
        addr_out,
        we,
        iData_RS232,
        WriteEnable_RS232,
        read_addr_RS232
    );
end

RS232Programmer dut(
    clk,
    rst,
    enable,
    oInfobyte,
    dout,
    addr_out,
    we,
    iData_RS232,
    WriteEnable_RS232,
    oWrBuffer_full_RS232,
    oData_RS232,
    read_addr_RS232,
    rx_addr_RS232
);

endmodule
