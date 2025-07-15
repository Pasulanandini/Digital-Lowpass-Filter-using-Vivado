import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

# === Configuration ===
cutoff_freq = 5000  # Hz
fs_expected = 16000  # Hz

# === File paths ===
filtered_versions = {
    "Order 2": "44filtered2.wav",
    "Order 4": "44filtered4.wav",
    "Order 8": "44filtered8.wav",
    "Order 16": "44filtered16.wav"
   # "Order 32": "44filtered32.wav",
   # "Order 64": "44filtered64.wav"
}
clean_path = "44.wav"

# === Helper Functions ===
def load_audio(path):
    if not os.path.exists(path):
        print(f"⚠️  File not found: {path}")
        return None, None
    fs, data = wavfile.read(path)
    if data.ndim > 1:
        data = np.mean(data, axis=1)
    data = data.astype(np.float32) / 32768.0
    return data, fs

def compute_band_snr(reference, test, fs, band):
    fft_len = min(len(reference), len(test))
    ref_fft = np.fft.rfft(reference[:fft_len])
    test_fft = np.fft.rfft(test[:fft_len])
    freqs = np.fft.rfftfreq(fft_len, d=1/fs)
    indices = np.where((freqs >= band[0]) & (freqs <= band[1]))[0]
    ref_band = np.abs(ref_fft[indices])
    test_band = np.abs(test_fft[indices])
    noise_band = test_band - ref_band
    signal_power = np.mean(ref_band ** 2)
    noise_power = np.mean(noise_band ** 2)
    return 10 * np.log10(signal_power / noise_power) if noise_power > 0 else np.inf

def nextpow2(n):
    return int(np.ceil(np.log2(n)))

def plot_fft_subplot(signal, label, color, pos, fs, total):
    fft_len = 2 ** nextpow2(len(signal))
    fft_data = np.abs(np.fft.rfft(signal, n=fft_len))
    freqs = np.fft.rfftfreq(fft_len, d=1/fs)

    plt.subplot(total, 1, pos)
    plt.plot(freqs, fft_data, color=color)
    plt.axvline(cutoff_freq, color='blue', linestyle='--', linewidth=1, label='5 kHz Cutoff')
    plt.title(f"{label}", fontsize=10, pad=4)
    plt.xlim(0, 8000)
    if pos < total:
        plt.xticks([])  # Hide x-axis ticks except bottom
    else:
        plt.xlabel("Frequency (Hz)", fontsize=9)
    plt.ylabel("Magnitude", fontsize=9)
    plt.grid(True)

# === Load and plot ===
original, fs = load_audio(clean_path)
if original is None or fs != fs_expected:
    print("❌ Error loading original signal or sampling rate mismatch.")
else:
    total_plots = 1 + len(filtered_versions)
    plt.figure(figsize=(12, total_plots * 2.2))  # Adjust height per subplot

    plot_fft_subplot(original, "Original Signal (Unfiltered)", "black", 1, fs, total_plots)

    for i, (label, path) in enumerate(filtered_versions.items(), start=2):
        filtered, fs_filt = load_audio(path)
        if filtered is None or fs_filt != fs_expected:
            print(f"⚠️ Skipping {label} due to error or FS mismatch.")
            continue

        min_len = min(len(original), len(filtered))
        orig_trim = original[:min_len]
        filt_trim = filtered[:min_len]

        plot_fft_subplot(filt_trim, f"Filtered Output - {label}", "green", i, fs, total_plots)

        # Optional SNR reporting
        pb_snr = compute_band_snr(orig_trim, filt_trim, fs, (0, 4500))
        sb_snr = compute_band_snr(orig_trim, filt_trim, fs, (5500, fs // 2))
        print(f"\n📊 {label}")
        print(f"  ▶ Passband SNR  : {pb_snr:.2f} dB")
        print(f"  ▶ Stopband SNR  : {sb_snr:.2f} dB")

    plt.suptitle("FFT Spectrum of Original and FIR Filtered Signals", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
