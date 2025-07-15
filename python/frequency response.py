import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, freqz

# Parameters
Fs = 16000              # Sampling frequency in Hz
Fc = 5000               # Cutoff frequency in Hz
orders = [2, 4, 8, 16]  # Filter orders to analyze

# Create 2x2 subplot figure
fig, axs = plt.subplots(2, 2, figsize=(10, 6))
axs = axs.flatten()

for i, N in enumerate(orders):
    # Design FIR lowpass filter with Rectangular window
    b = firwin(numtaps=N+1, cutoff=Fc, window='boxcar', fs=Fs, pass_zero='lowpass')

    # Compute frequency response
    w, h = freqz(b, worN=1024, fs=Fs)
    h_dB = 20 * np.log10(np.abs(h))

    # Plot on subplot
    axs[i].plot(w, h_dB, 'b', linewidth=1.5)
    axs[i].axvline(Fc, color='r', linestyle='--', linewidth=1.2)  # Cutoff marker
    axs[i].set_title(f'Order = {N}')
    axs[i].set_xlabel('Frequency (Hz)')
    axs[i].set_ylabel('Gain (dB)')
    axs[i].grid(True)

# Main title
fig.suptitle('Frequency Response of Lowpass FIR Filters (Rectangular Window)', fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show the plot
plt.show()
