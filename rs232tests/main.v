// File: main.v
// Generated by MyHDL 0.11
// Date: Thu Feb  4 14:36:37 2021


`timescale 1ns/10ps

module main (
    iClk,
    iRX,
    oTX
);


input iClk;
input iRX;
output oTX;
reg oTX;

reg obusy;
reg [7:0] iData;
reg [7:0] ldData;
reg iRst;
reg [7:0] oData;
reg [4:0] rx_addr;
reg [4:0] read_addr;
reg sig;
reg [5:0] pwrup;
reg WriteEnable;
wire oWrBuffer_full;
reg [31:0] ppscounter;
reg [7:0] rom_dout;
reg [3:0] rom_addr;
reg [2:0] updatebuff0_state1;
reg [7:0] pps0_sighi;
reg RS232_Module0_sig_WrBuffer_full;
reg [5:0] RS232_Module0_tx_counter;
reg [3:0] RS232_Module0_tx_bit_count;
reg [8:0] RS232_Module0_rx_currentData;
reg [1:0] RS232_Module0_rx_State;
reg [4:0] RS232_Module0_write_addr;
reg [4:0] RS232_Module0_rx_addr;
reg [5:0] RS232_Module0_rx_counter;
reg [1:0] RS232_Module0_tx_State;
reg [9:0] RS232_Module0_SendREG;
reg [4:0] RS232_Module0_tx_addr;
reg [3:0] RS232_Module0_rx_bit_count;
reg [7:0] RS232_Module0_Receive_RAM [0:20-1];
reg [7:0] RS232_Module0_Transmit_RAM [0:20-1];



always @(rom_addr) begin: MAIN_ROM0_READ
    case (rom_addr)
        0: rom_dout = 72;
        1: rom_dout = 69;
        2: rom_dout = 76;
        3: rom_dout = 76;
        4: rom_dout = 79;
        5: rom_dout = 87;
        6: rom_dout = 79;
        7: rom_dout = 82;
        8: rom_dout = 76;
        9: rom_dout = 68;
        10: rom_dout = 13;
        default: rom_dout = 10;
    endcase
end


always @(posedge iClk, negedge iRst) begin: MAIN_UPDATEBUFF0_RTL
    if ((iRst == 0)) begin
        iData <= 0;
        ldData <= 0;
        WriteEnable <= 0;
        read_addr <= 0;
        obusy <= 0;
        updatebuff0_state1 <= 3'b000;
    end
    else begin
        updatebuff0_state1 <= 3'b000;
        case (updatebuff0_state1)
            3'b000: begin
                if (((!WriteEnable) && (!oWrBuffer_full))) begin
                    ldData <= rom_dout;
                    obusy <= 1;
                    updatebuff0_state1 <= 3'b001;
                end
            end
            3'b001: begin
                updatebuff0_state1 <= 3'b010;
            end
            3'b010: begin
                iData <= ldData;
                WriteEnable <= 1;
                updatebuff0_state1 <= 3'b011;
            end
            3'b011: begin
                WriteEnable <= 0;
                if ((rom_addr < 11)) begin
                    rom_addr <= (rom_addr + 1);
                    updatebuff0_state1 <= 3'b100;
                end
                else begin
                    rom_addr <= 0;
                    updatebuff0_state1 <= 3'b000;
                end
            end
            3'b100: begin
                WriteEnable <= 0;
                updatebuff0_state1 <= 3'b101;
            end
            3'b101: begin
                if ((!sig)) begin
                    updatebuff0_state1 <= 3'b101;
                end
                else begin
                    updatebuff0_state1 <= 3'b110;
                end
            end
            default: begin
                if ((updatebuff0_state1 == 3'b110)) begin
                    obusy <= 0;
                    updatebuff0_state1 <= 3'b000;
                end
            end
        endcase
    end
end


always @(posedge iClk) begin: MAIN_PPS0_PPSI
    if ((ppscounter < 50000000)) begin
        ppscounter <= (ppscounter + 1);
        if ((ppscounter < pps0_sighi)) begin
            sig <= 1;
        end
        else begin
            sig <= 0;
            pps0_sighi <= 0;
        end
    end
    else begin
        ppscounter <= 0;
        sig <= 1;
        pps0_sighi <= 1000;
    end
end


always @(posedge iClk, negedge iRst) begin: MAIN_RS232_MODULE0_SEQ_LOGIC
    if ((iRst == 0)) begin
        RS232_Module0_rx_State <= 0;
        RS232_Module0_rx_counter <= 0;
        RS232_Module0_rx_currentData <= 0;
        RS232_Module0_rx_bit_count <= 0;
        RS232_Module0_rx_addr <= 0;
        rx_addr <= 0;
        RS232_Module0_tx_State <= 0;
        RS232_Module0_tx_addr <= 0;
        RS232_Module0_write_addr <= 0;
        RS232_Module0_SendREG <= 0;
        RS232_Module0_tx_counter <= 0;
        RS232_Module0_tx_bit_count <= 0;
    end
    else begin
        rx_addr <= RS232_Module0_rx_addr;
        oData <= RS232_Module0_Receive_RAM[read_addr];
        oTX <= 1;
        case (RS232_Module0_rx_State)
            'h0: begin
                if ((iRX == 0)) begin
                    RS232_Module0_rx_counter <= (RS232_Module0_rx_counter + 1);
                end
                else begin
                    RS232_Module0_rx_counter <= 0;
                end
                if ((RS232_Module0_rx_counter == 25)) begin
                    RS232_Module0_rx_State <= 1;
                    RS232_Module0_rx_counter <= 0;
                    RS232_Module0_rx_bit_count <= 0;
                end
            end
            'h1: begin
                RS232_Module0_rx_counter <= (RS232_Module0_rx_counter + 1);
                if ((RS232_Module0_rx_counter == 0)) begin
                    RS232_Module0_rx_currentData <= {iRX, RS232_Module0_rx_currentData[9-1:1]};
                    RS232_Module0_rx_bit_count <= (RS232_Module0_rx_bit_count + 1);
                end
                if ((RS232_Module0_rx_counter == 50)) begin
                    RS232_Module0_rx_counter <= 0;
                end
                if ((RS232_Module0_rx_bit_count == 9)) begin
                    RS232_Module0_rx_State <= 2;
                    RS232_Module0_rx_counter <= 0;
                end
            end
            'h2: begin
                RS232_Module0_rx_counter <= (RS232_Module0_rx_counter + 1);
                if ((RS232_Module0_rx_counter == 50)) begin
                    RS232_Module0_rx_State <= 0;
                    RS232_Module0_rx_counter <= 0;
                    if ((iRX == 1)) begin
                        RS232_Module0_Receive_RAM[RS232_Module0_rx_addr] <= RS232_Module0_rx_currentData[9-1:1];
                        RS232_Module0_rx_addr <= ((RS232_Module0_rx_addr + 1) % 20);
                    end
                end
            end
        endcase
        if ((WriteEnable && (!RS232_Module0_sig_WrBuffer_full))) begin
            RS232_Module0_Transmit_RAM[RS232_Module0_write_addr] <= iData;
            RS232_Module0_write_addr <= ((RS232_Module0_write_addr + 1) % 20);
        end
        case (RS232_Module0_tx_State)
            'h0: begin
                if ((RS232_Module0_write_addr != RS232_Module0_tx_addr)) begin
                    RS232_Module0_tx_counter <= 0;
                    RS232_Module0_tx_State <= 1;
                    RS232_Module0_tx_bit_count <= 0;
                    RS232_Module0_SendREG <= {1'h1, RS232_Module0_Transmit_RAM[RS232_Module0_tx_addr], 1'h0};
                    RS232_Module0_tx_addr <= ((RS232_Module0_tx_addr + 1) % 20);
                end
            end
            'h1: begin
                oTX <= RS232_Module0_SendREG[RS232_Module0_tx_bit_count];
                RS232_Module0_tx_counter <= (RS232_Module0_tx_counter + 1);
                if ((RS232_Module0_tx_counter == 50)) begin
                    RS232_Module0_tx_bit_count <= (RS232_Module0_tx_bit_count + 1);
                    RS232_Module0_tx_counter <= 0;
                    if ((RS232_Module0_tx_bit_count == 9)) begin
                        RS232_Module0_tx_State <= 0;
                    end
                end
            end
        endcase
    end
end


always @(RS232_Module0_write_addr, RS232_Module0_tx_addr) begin: MAIN_RS232_MODULE0_COMB_LOGIC
    if ((((RS232_Module0_write_addr + 1) % 20) == RS232_Module0_tx_addr)) begin
        RS232_Module0_sig_WrBuffer_full = 1'b1;
    end
    else begin
        RS232_Module0_sig_WrBuffer_full = 1'b0;
    end
end



assign oWrBuffer_full = RS232_Module0_sig_WrBuffer_full;


always @(posedge iClk) begin: MAIN_PWRUPRST0_LOGIC2
    if (((iRst == 1) && (pwrup == 40))) begin
        iRst <= 0;
    end
    else begin
        if ((pwrup <= 60)) begin
            pwrup <= (pwrup + 1);
        end
    end
    if ((pwrup == 60)) begin
        iRst <= 1;
    end
end

endmodule
