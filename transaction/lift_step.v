// File: lift_step.v
// Generated by MyHDL 0.11
// Date: Tue Dec 15 18:06:07 2020


`timescale 1ns/10ps

module lift_step (
    left_i,
    sam_i,
    right_i,
    flgs_i,
    update_i,
    clk,
    res_o,
    update_o
);


input signed [15:0] left_i;
input signed [15:0] sam_i;
input signed [15:0] right_i;
input [3:0] flgs_i;
input update_i;
input clk;
output signed [15:0] res_o;
reg signed [15:0] res_o;
output update_o;
reg update_o;




always @(posedge clk) begin: LIFT_STEP_RTL
    if ((update_i == 1)) begin
        update_o <= 0;
        case (flgs_i)
            'h7: begin
                res_o <= (sam_i - ($signed(left_i >>> 1) + $signed(right_i >>> 1)));
            end
            'h5: begin
                res_o <= (sam_i + ($signed(left_i >>> 1) + $signed(right_i >>> 1)));
            end
            'h6: begin
                res_o <= (sam_i + $signed(((left_i + right_i) + 2) >>> 2));
            end
            'h4: begin
                res_o <= (sam_i - $signed(((left_i + right_i) + 2) >>> 2));
            end
        endcase
    end
    else begin
        update_o <= 1;
    end
end

endmodule
