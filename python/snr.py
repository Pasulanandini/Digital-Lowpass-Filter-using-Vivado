import numpy as np
from scipy.io import wavfile

# === Configuration ===
fs = 16000
fft_len = 131072  # Power of 2 for efficient FFT
passband = (0, 4500)
stopband = (5500, fs // 2)

# === File paths ===
noisy_path = "44.wav"
filtered_paths = {
    "Order 2": "44filtered2.wav",
    "Order 4": "44filtered4.wav",
    "Order 8": "44filtered8.wav",
    "Order 16": "44filtered16.wav"
}

# === Load and normalize ===
def load(path):
    fs_, data = wavfile.read(path)
    if data.ndim > 1:  # Stereo to mono
        data = np.mean(data, axis=1)
    return data.astype(np.float32) / 32768.0

noisy = load(noisy_path)

# === SNR calculation in frequency band ===
def band_power(signal, fs, band):
    spectrum = np.fft.rfft(signal, n=fft_len)
    freqs = np.fft.rfftfreq(fft_len, d=1/fs)
    band_indices = (freqs >= band[0]) & (freqs <= band[1])
    power = np.mean(np.abs(spectrum[band_indices])**2)
    return power

# === Compute SNRs ===
print("📊 SNR Results (in dB):\n")
print(f"{'Order':<10}{'Passband SNR':>18}{'Stopband SNR':>20}")
print("-" * 48)

for label, path in filtered_paths.items():
    processed = load(path)
    min_len = min(len(noisy), len(processed))
    noisy_clip = noisy[:min_len]
    proc_clip = processed[:min_len]

    # Passband SNR
    p_noisy_pass = band_power(noisy_clip, fs, passband)
    p_proc_pass = band_power(proc_clip, fs, passband)
    snr_pass = 10 * np.log10(p_noisy_pass / p_proc_pass)

    # Stopband SNR
    p_noisy_stop = band_power(noisy_clip, fs, stopband)
    p_proc_stop = band_power(proc_clip, fs, stopband)
    snr_stop = 10 * np.log10(p_noisy_stop / p_proc_stop)

    print(f"{label:<10}{snr_pass:18.2f}{snr_stop:20.2f}")
