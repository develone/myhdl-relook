// File: updatebuff.v
// Generated by MyHDL 0.11
// Date: Thu Feb  4 14:33:19 2021


`timescale 1ns/10ps

module updatebuff (
    iClk,
    iRst,
    iData,
    WriteEnable,
    ldData,
    oWrBuffer_full,
    obusy,
    rom_dout,
    rom_addr
);


input iClk;
input iRst;
output [7:0] iData;
reg [7:0] iData;
output WriteEnable;
reg WriteEnable;
output [7:0] ldData;
reg [7:0] ldData;
input oWrBuffer_full;
output obusy;
reg obusy;
input [7:0] rom_dout;
output [3:0] rom_addr;
reg [3:0] rom_addr;

reg [4:0] read_addr;
wire sig;
reg [2:0] state1;

assign sig = 1'd0;


always @(posedge iClk, negedge iRst) begin: UPDATEBUFF_RTL
    if ((iRst == 0)) begin
        iData <= 0;
        ldData <= 0;
        WriteEnable <= 0;
        read_addr <= 0;
        obusy <= 0;
        state1 <= 3'b000;
    end
    else begin
        state1 <= 3'b000;
        case (state1)
            3'b000: begin
                if (((!WriteEnable) && (!oWrBuffer_full))) begin
                    ldData <= rom_dout;
                    obusy <= 1;
                    state1 <= 3'b001;
                end
            end
            3'b001: begin
                state1 <= 3'b010;
            end
            3'b010: begin
                iData <= ldData;
                WriteEnable <= 1;
                state1 <= 3'b011;
            end
            3'b011: begin
                WriteEnable <= 0;
                if ((rom_addr < 11)) begin
                    rom_addr <= (rom_addr + 1);
                    state1 <= 3'b100;
                end
                else begin
                    rom_addr <= 0;
                    state1 <= 3'b000;
                end
            end
            3'b100: begin
                WriteEnable <= 0;
                state1 <= 3'b101;
            end
            3'b101: begin
                if ((!sig)) begin
                    state1 <= 3'b101;
                end
                else begin
                    state1 <= 3'b110;
                end
            end
            default: begin
                if ((state1 == 3'b110)) begin
                    obusy <= 0;
                    state1 <= 3'b000;
                end
            end
        endcase
    end
end

endmodule
