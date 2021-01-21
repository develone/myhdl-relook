// File: main.v
// Generated by MyHDL 0.11
// Date: Thu Jan 21 13:32:15 2021


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

reg we;
wire [31:0] dout;
reg oprog_WriteEnable_RS232;
wire programmer_enable;
reg [7:0] oData;
reg [7:0] oprog_Data_RS232;
wire WriteEnable;
reg [2:0] rx_addr;
wire [31:0] addr_out;
reg iRst;
reg [2:0] read_addr;
wire [7:0] oInfobyte;
reg pwrup;
wire [7:0] iData;
wire oWrBuffer_full;
reg RS232Programmer0_isData;
reg [7:0] RS232Programmer0_Info_byte;
reg [8:0] RS232Programmer0_countbytesRX;
reg [31:0] RS232Programmer0_received_data;
reg [2:0] RS232Programmer0_state;
reg [31:0] RS232Programmer0_received_addr;
reg [1:0] RS232Programmer0_subcount;
reg RS232_Module0_sig_WrBuffer_full;
reg [8:0] RS232_Module0_tx_counter;
reg [3:0] RS232_Module0_tx_bit_count;
reg [8:0] RS232_Module0_rx_currentData;
reg [1:0] RS232_Module0_rx_State;
reg [2:0] RS232_Module0_write_addr;
reg [2:0] RS232_Module0_rx_addr;
reg [8:0] RS232_Module0_rx_counter;
reg [1:0] RS232_Module0_tx_State;
reg [9:0] RS232_Module0_SendREG;
reg [2:0] RS232_Module0_tx_addr;
reg [3:0] RS232_Module0_rx_bit_count;
reg [7:0] RS232_Module0_Receive_RAM [0:8-1];
reg [7:0] RS232_Module0_Transmit_RAM [0:8-1];

assign programmer_enable = 1'd1;
assign WriteEnable = 1'd0;
assign iData = 8'd0;


always @(posedge iClk, negedge iRst) begin: MAIN_RS232PROGRAMMER0_IO_WRITE_SYNC
    if ((iRst == 0)) begin
        RS232Programmer0_state <= 3'b000;
        read_addr <= 0;
        RS232Programmer0_Info_byte <= 9;
        RS232Programmer0_subcount <= 0;
        RS232Programmer0_isData <= 1'b0;
        RS232Programmer0_countbytesRX <= 0;
        oprog_WriteEnable_RS232 <= 1'b0;
        oprog_Data_RS232 <= 0;
        we <= 1'b0;
    end
    else begin
        oprog_WriteEnable_RS232 <= 1'b0;
        if (we) begin
            RS232Programmer0_received_data <= 0;
            RS232Programmer0_received_addr <= 0;
            RS232Programmer0_countbytesRX <= (RS232Programmer0_countbytesRX + 1);
            oprog_Data_RS232 <= RS232Programmer0_countbytesRX;
            oprog_WriteEnable_RS232 <= 1'b1;
        end
        we <= 1'b0;
        case (RS232Programmer0_state)
            3'b000: begin
                RS232Programmer0_isData <= 1'b0;
                if ((rx_addr != read_addr)) begin
                    read_addr <= ((read_addr + 1) % 8);
                    RS232Programmer0_state <= 3'b001;
                end
            end
            3'b001: begin
                if (((oData[6-1:3] == 0) || (oData[3-1:0] == 0))) begin
                    RS232Programmer0_Info_byte <= 9;
                end
                else begin
                    RS232Programmer0_Info_byte <= oData;
                    RS232Programmer0_state <= 3'b010;
                end
            end
            3'b010: begin
                if ((rx_addr != read_addr)) begin
                    RS232Programmer0_state <= 3'b100;
                end
                if ((RS232Programmer0_countbytesRX == 256)) begin
                    RS232Programmer0_state <= 3'b000;
                    RS232Programmer0_countbytesRX <= 0;
                    $write("alll 256 Datas received");
                    $write("\n");
                end
            end
            3'b011: begin
                RS232Programmer0_state <= 3'b100;
            end
            3'b100: begin
                RS232Programmer0_subcount <= ((RS232Programmer0_subcount + 1) % 4);
                if (RS232Programmer0_isData) begin
                    RS232Programmer0_received_data <= ((RS232Programmer0_received_data << 8) | oData);
                    if (((RS232Programmer0_subcount + 1) >= RS232Programmer0_Info_byte[6-1:3])) begin
                        RS232Programmer0_isData <= 1'b0;
                        RS232Programmer0_subcount <= 0;
                        we <= 1'b1;
                    end
                end
                else begin
                    RS232Programmer0_received_addr <= ((RS232Programmer0_received_addr << 8) | oData);
                    if (((RS232Programmer0_subcount + 1) >= RS232Programmer0_Info_byte[3-1:0])) begin
                        RS232Programmer0_isData <= 1'b1;
                        RS232Programmer0_subcount <= 0;
                    end
                end
                read_addr <= ((read_addr + 1) % 8);
                RS232Programmer0_state <= 3'b010;
            end
        endcase
        if ((!programmer_enable)) begin
            RS232Programmer0_state <= 3'b000;
            read_addr <= rx_addr;
        end
    end
end



assign dout = RS232Programmer0_received_data;
assign addr_out = RS232Programmer0_received_addr;
assign oInfobyte = RS232Programmer0_Info_byte;


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
                if ((RS232_Module0_rx_counter == 217)) begin
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
                if ((RS232_Module0_rx_counter == 434)) begin
                    RS232_Module0_rx_counter <= 0;
                end
                if ((RS232_Module0_rx_bit_count == 9)) begin
                    RS232_Module0_rx_State <= 2;
                    RS232_Module0_rx_counter <= 0;
                end
            end
            'h2: begin
                RS232_Module0_rx_counter <= (RS232_Module0_rx_counter + 1);
                if ((RS232_Module0_rx_counter == 434)) begin
                    RS232_Module0_rx_State <= 0;
                    RS232_Module0_rx_counter <= 0;
                    if ((iRX == 1)) begin
                        RS232_Module0_Receive_RAM[RS232_Module0_rx_addr] <= RS232_Module0_rx_currentData[9-1:1];
                        RS232_Module0_rx_addr <= ((RS232_Module0_rx_addr + 1) % 8);
                    end
                end
            end
        endcase
        if ((WriteEnable && (!RS232_Module0_sig_WrBuffer_full))) begin
            RS232_Module0_Transmit_RAM[RS232_Module0_write_addr] <= iData;
            RS232_Module0_write_addr <= ((RS232_Module0_write_addr + 1) % 8);
        end
        case (RS232_Module0_tx_State)
            'h0: begin
                if ((RS232_Module0_write_addr != RS232_Module0_tx_addr)) begin
                    RS232_Module0_tx_counter <= 0;
                    RS232_Module0_tx_State <= 1;
                    RS232_Module0_tx_bit_count <= 0;
                    RS232_Module0_SendREG <= {1'h1, RS232_Module0_Transmit_RAM[RS232_Module0_tx_addr], 1'h0};
                    RS232_Module0_tx_addr <= ((RS232_Module0_tx_addr + 1) % 8);
                end
            end
            'h1: begin
                oTX <= RS232_Module0_SendREG[RS232_Module0_tx_bit_count];
                RS232_Module0_tx_counter <= (RS232_Module0_tx_counter + 1);
                if ((RS232_Module0_tx_counter == 434)) begin
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
    if ((((RS232_Module0_write_addr + 1) % 8) == RS232_Module0_tx_addr)) begin
        RS232_Module0_sig_WrBuffer_full = 1'b1;
    end
    else begin
        RS232_Module0_sig_WrBuffer_full = 1'b0;
    end
end



assign oWrBuffer_full = RS232_Module0_sig_WrBuffer_full;


always @(posedge iClk) begin: MAIN_PWRUPRST0_LOGIC2
    if (((iRst == 1) && (pwrup == 1))) begin
        iRst <= 0;
        pwrup <= 0;
    end
    if ((pwrup == 0)) begin
        iRst <= 1;
    end
end

endmodule
