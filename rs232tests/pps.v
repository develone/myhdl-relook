// File: pps.v
// Generated by MyHDL 0.11
// Date: Mon Feb  1 18:40:43 2021


`timescale 1ns/10ps

module pps (
    iClk,
    ppscounter,
    sig
);


input iClk;
output [31:0] ppscounter;
reg [31:0] ppscounter;
output sig;
reg sig;

reg [7:0] sighi;



always @(posedge iClk) begin: PPS_PPSI
    if ((ppscounter < 50000000)) begin
        ppscounter <= (ppscounter + 1);
        if ((ppscounter < sighi)) begin
            sig <= 1;
        end
        else begin
            sig <= 0;
            sighi <= 0;
        end
    end
    else begin
        ppscounter <= 0;
        sig <= 1;
        sighi <= 1000;
    end
end

endmodule