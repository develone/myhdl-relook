module tb_main;

reg iClk;
wire iRst;
reg iRX;
wire oTX;
reg [7:0] iData;
reg WriteEnable;
wire oWrBuffer_full;
wire [7:0] oData;
reg [2:0] read_addr;
wire [2:0] rx_addr;
wire pwrup;

initial begin
    $from_myhdl(
        iClk,
        iRX,
        iData,
        WriteEnable,
        read_addr
    );
    $to_myhdl(
        iRst,
        oTX,
        oWrBuffer_full,
        oData,
        rx_addr,
        pwrup
    );
end

main dut(
    iClk,
    iRst,
    iRX,
    oTX,
    iData,
    WriteEnable,
    oWrBuffer_full,
    oData,
    read_addr,
    rx_addr,
    pwrup
);

endmodule
