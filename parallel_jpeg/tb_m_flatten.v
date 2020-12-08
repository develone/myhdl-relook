module tb_m_flatten;

wire [143:0] flat;

initial begin
    $to_myhdl(
        flat
    );
end

m_flatten dut(
    flat
);

endmodule
