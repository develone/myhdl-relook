module tb_mainecho;

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

mainecho dut(
    iClk,
    iRX,
    oTX
);
initial begin
    $dumpfile("mainecho.vcd");
    $dumpvars();
end
endmodule
