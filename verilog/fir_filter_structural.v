`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 29.04.2025 16:08:53
// Design Name: 
// Module Name: fir_filter_structural
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


// Top-level structural FIR filter
module fir_filter_structural (
    input clk,
    input rst,
    input signed [15:0] x_in,
    output signed [31:0] y_out
);
    wire signed [15:0] x0, x1, x2;
    wire signed [31:0] mul0, mul1, mul2;
    wire signed [31:0] sum0, sum1;

    // Coefficients hard-coded or can be loaded
    wire signed [15:0] coeffs[0:2];
    assign coeffs[0] = 16'h1ACF; // Example value
    assign coeffs[1] = 16'h4A83; // Example value
    assign coeffs[2] = 16'h1ACF; // Example value

    // Instantiate shift register
    shift_register shift_inst (
        .clk(clk),
        .rst(rst),
        .data_in(x_in),
        .data_out0(x0),
        .data_out1(x1),
        .data_out2(x2)
    );

    // Instantiate multipliers
    multiplier mul0_inst (.a(x0), .b(coeffs[0]), .product(mul0));
    multiplier mul1_inst (.a(x1), .b(coeffs[1]), .product(mul1));
    multiplier mul2_inst (.a(x2), .b(coeffs[2]), .product(mul2));

    // Instantiate adders
    adder add0_inst (.a(mul0), .b(mul1), .sum(sum0));
    adder add1_inst (.a(sum0), .b(mul2), .sum(sum1));

    // Output assignment
    assign y_out = sum1;
endmodule  




  
 
  

