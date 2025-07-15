module fir(
    input clk,
    input rst,
    input signed [15:0] x_in,
    output reg signed [31:0] y_out
);
    parameter N = 3;
    reg signed [15:0] coeffs [0:N-1];
    reg signed [15:0] shift_reg [0:N-1];
    integer i;
    reg signed [31:0] acc;

    initial begin
        $readmemh("C:/Users/pasul/project_1/fir_coefficients.txt", coeffs);
    end

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < N; i = i + 1)
                shift_reg[i] <= 16'd0;
            y_out <= 32'd0;
        end else begin
            for (i = N-1; i > 0; i = i - 1)
                shift_reg[i] <= shift_reg[i-1];
            shift_reg[0] <= x_in;

            acc = 0;
            for (i = 0; i < N; i = i + 1)
                acc = acc + $signed(shift_reg[i]) * $signed(coeffs[i]);
            y_out <= acc;
        end
    end
endmodule


module fir1_tb;
    reg clk;
    reg rst;
    reg signed [15:0] x_in;
    wire signed [31:0] y_out;
    reg signed [15:0] input_mem [0:150464];
    integer i, output_file;

    fir uut (
        .clk(clk),
        .rst(rst),
        .x_in(x_in),
        .y_out(y_out)
    );

    always #50 clk = ~clk;

    initial begin
        clk = 0;
        rst = 1;
        #100 rst = 0;

        $readmemh("C:/Users/pasul/project_1/input_audio_16khz.txt", input_mem);
        output_file = $fopen("vivadoch.txt", "w");

        for (i = 0; i < 150465; i = i + 1) begin
            x_in = input_mem[i];
            @(posedge clk);
            $fwrite(output_file, "%h\n", y_out[31:16]);  // take top 16 bits
        end

        $fclose(output_file);
        $stop;
    end
endmodule

