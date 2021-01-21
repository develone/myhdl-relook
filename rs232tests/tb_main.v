module tb_main;

reg iClk;
reg iRX;
wire oTX;

initial begin
    $from_myhdl(
        iClk,
        iRX
    );
    $to_myhdl(
        oTX
    );
end

main dut(
    iClk,
    iRX,
    oTX
);

endmodule
