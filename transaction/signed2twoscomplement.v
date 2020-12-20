// File: signed2twoscomplement.v
// Generated by MyHDL 0.11
// Date: Mon Dec 14 09:34:07 2020


`timescale 1ns/10ps

module signed2twoscomplement (
    clk,
    x,
    z
);


input clk;
input signed [15:0] x;
output signed [15:0] z;
reg signed [15:0] z;




always @(posedge clk) begin: SIGNED2TWOSCOMPLEMENT_UNSIGNED_LOGIC
    z <= x;
end

endmodule