module tb_Odd_Even_Fsm;

wire [27:0] state;
reg clk;
reg rst_fsm;
wire [7:0] addr_left;
wire muxsel_i;
wire [7:0] addr_sam;
wire [7:0] addr_rht;
wire [1:0] muxaddrsel;
wire we_1;
reg [8:0] dout;
wire [8:0] left_i;
wire [8:0] sam_i;
wire [8:0] right_i;
wire do_first;
wire [9:0] x;
reg [8:0] z;
wire [3:0] flgs_i;
wire update_i;
reg [9:0] res_o;
reg update_o;
wire end_of_col;
wire [7:0] addr_in;
wire [9:0] xfifo;
wire enr_r;
reg enw_r;
wire [7:0] del_ctn;

initial begin
    $from_myhdl(
        clk,
        rst_fsm,
        dout,
        z,
        res_o,
        update_o,
        enw_r
    );
    $to_myhdl(
        state,
        addr_left,
        muxsel_i,
        addr_sam,
        addr_rht,
        muxaddrsel,
        we_1,
        left_i,
        sam_i,
        right_i,
        do_first,
        x,
        flgs_i,
        update_i,
        end_of_col,
        addr_in,
        xfifo,
        enr_r,
        del_ctn
    );
end

Odd_Even_Fsm dut(
    state,
    clk,
    rst_fsm,
    addr_left,
    muxsel_i,
    addr_sam,
    addr_rht,
    muxaddrsel,
    we_1,
    dout,
    left_i,
    sam_i,
    right_i,
    do_first,
    x,
    z,
    flgs_i,
    update_i,
    res_o,
    update_o,
    end_of_col,
    addr_in,
    xfifo,
    enr_r,
    enw_r,
    del_ctn
);

endmodule
