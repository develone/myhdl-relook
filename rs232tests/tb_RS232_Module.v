module tb_RS232_Module;

reg iClk;
reg iRst;
reg iRX;
wire oTX;
reg [7:0] iData;
reg WriteEnable;
wire oWrBuffer_full;
wire [7:0] oData;
reg [2:0] read_addr;
wire [2:0] oRx_addr;

initial begin
    $from_myhdl(
        iClk,
        iRst,
        iRX,
        iData,
        WriteEnable,
        read_addr
    );
    $to_myhdl(
        oTX,
        oWrBuffer_full,
        oData,
        oRx_addr
    );
end

RS232_Module dut(
    iClk,
    iRst,
    iRX,
    oTX,
    iData,
    WriteEnable,
    oWrBuffer_full,
    oData,
    read_addr,
    oRx_addr
);

endmodule
