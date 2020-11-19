// File: lift_step.v
// Generated by MyHDL 0.11
// Date: Wed Nov 18 18:09:22 2020


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


input [8:0] left_i;
input [8:0] sam_i;
input [8:0] right_i;
input [3:0] flgs_i;
input update_i;
input clk;
output signed [9:0] res_o;
reg signed [9:0] res_o;
output update_o;
reg update_o;




always @(posedge clk) begin: LIFT_STEP_RTL
    if ((update_i == 1)) begin
        update_o <= 0;
        case (flgs_i)
            'h7: begin
                res_o <= ($signed(sam_i) - ($signed($signed(left_i) >>> 1) + $signed($signed(right_i) >>> 1)));
            end
            'h5: begin
                res_o <= ($signed(sam_i) + ($signed($signed(left_i) >>> 1) + $signed($signed(right_i) >>> 1)));
            end
            'h6: begin
                res_o <= ($signed(sam_i) + $signed((($signed(left_i) + $signed(right_i)) + 2) >>> 2));
            end
            'h4: begin
                res_o <= ($signed(sam_i) - $signed((($signed(left_i) + $signed(right_i)) + 2) >>> 2));
            end
        endcase
    end
    else begin
        update_o <= 1;
    end
end

endmodule
