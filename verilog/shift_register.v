`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 29.04.2025 16:06:37
// Design Name: 
// Module Name: shift_register
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



// Shift Register module
module shift_register (
    input clk,
    input rst,
    input signed [15:0] data_in,
    output reg signed [15:0] data_out0,
    output reg signed [15:0] data_out1,
    output reg signed [15:0] data_out2
);
    reg signed [15:0] shift_reg[0:2];
    integer i;
    
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < 3; i = i + 1)
                shift_reg[i] <= 0;
        end else begin
            shift_reg[2] <= shift_reg[1];
            shift_reg[1] <= shift_reg[0];
            shift_reg[0] <= data_in;
        end
    end

    always @(*) begin
        data_out0 = shift_reg[0];
        data_out1 = shift_reg[1];
        data_out2 = shift_reg[2];
    end
endmodule