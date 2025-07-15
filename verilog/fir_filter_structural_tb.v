`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 29.04.2025 16:30:25
// Design Name: 
// Module Name: fir_filter_structural_tb
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


module fir_filter_structural_tb;
    reg clk;
    reg rst;
    reg signed [15:0] x_in;
    wire signed [31:0] y_out;

    reg signed [15:0] input_mem [0:143999]; // Adjust size based on your input length
    integer i;
    integer output_file;

    // Instantiate FIR filter module
    fir_filter_structural uut (
        .clk(clk),
        .rst(rst),
        .x_in(x_in),
        .y_out(y_out)
    );

    // Clock generator
    always #31.25 clk = ~clk; // 100 MHz clock (10 ns period)

    // Testbench logic
    initial begin
        // Load input samples from hex file
        $readmemh("C:/Users/pasul/project_1/noise_audio_truncated.txt", input_mem);

        // Open output file
        output_file = $fopen("newstruct1.txt", "w");
        if (output_file == 0) begin
            $display("Error opening output file!");
            $stop;
        end

        // Initialize signals
        clk = 0;
        rst = 1;
        #10 rst = 0;

        // Apply input samples one-by-one
        for (i = 0; i < 144000; i = i + 1) begin
            x_in = input_mem[i];
            #10; // Wait for 1 clock cycle

            // Display input and output values
            $display("Time: %0t | Input: %h | Output: %h", $time, x_in, y_out);

            // Write the full 32-bit output to the file
            $fwrite(output_file, "%h\n", y_out[31:16]);
        end

        // Close output file
        $fclose(output_file);

        $display("FIR processing completed. Output saved in new1new.txt");
        $stop;
    end
endmodule

