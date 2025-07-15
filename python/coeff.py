import numpy as np

# --- Parameters ---
order = 64                      # Filter order
fc = 5000                     # Cutoff frequency (Hz)
fs = 16000                    # Sampling frequency (Hz)
output_file = "fir_order64_rectangular.txt"

# --- Number of taps ---
num_taps = order + 1
M = order
fc_norm = fc / fs  # Normalized cutoff frequency (0.0 to 0.5)

# --- Generate sinc function for ideal low-pass filter ---
h = []
for n in range(num_taps):
    if n == M / 2:
        h.append(2 * fc_norm)
    else:
        h.append(np.sin(2 * np.pi * fc_norm * (n - M / 2)) / (np.pi * (n - M / 2)))

h = np.array(h)

# --- Normalize to all non-negative (for unsigned hardware interpretation) ---
#h = h - np.min(h)
#h = h / np.max(h)
h = h / np.sum(h)

# --- Convert to Q15 format (0 to 32767) ---
h_q15 = np.round(h * 32767).astype(np.int16)

# --- Convert to 16-bit hex strings ---
h_hex = [format(val & 0xFFFF, '04X') for val in h_q15]

# --- Write to output file ---
with open(output_file, "w") as f:
    for hex_val in h_hex:
        f.write(hex_val + "\n")

print(f"✅ {num_taps} coefficients written to {output_file}")
