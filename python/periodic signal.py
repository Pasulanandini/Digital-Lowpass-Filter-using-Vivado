import numpy as np
from scipy.io.wavfile import read, write
from scipy.fft import rfft, irfft, rfftfreq

# === Parameters ===
input_file = "4.wav"
output_file = "44.wav"
max_freq_to_repeat = 750     # Hz, upper end of the band to tile
target_freq_limit = 8000     # Hz, how far up you want to fill
   
# === Load & mono-mix ===
sr, data = read(input_file)
if data.ndim > 1:
    data = data.mean(axis=1)           # simple stereo → mono
data = data.astype(np.float32)
data /= np.max(np.abs(data))           # normalize to [-1,1]

N = len(data)

# === Compute real FFT ===
spec = rfft(data)
freqs = rfftfreq(N, 1/sr)             # frequencies for each bin

# === Extract 0–750 Hz band ===
band_mask = freqs <= max_freq_to_repeat
band = spec[band_mask]
L_band = band.size

# === Determine how many bins up to 8 kHz ===
target_bins = np.sum(freqs <= target_freq_limit)

# === Tile that band to fill [0…8 kHz] ===
repeats = int(np.ceil(target_bins / L_band))
tiled = np.tile(band, repeats)[:target_bins]

# === Build new positive-freq spectrum ===
new_spec = np.zeros_like(spec)
new_spec[:target_bins] = tiled
# bins above target_freq_limit remain zero (i.e. we carve out everything >8 kHz)

# === Inverse FFT back to time domain ===
out = irfft(new_spec, n=N)

# === Renormalize & write 16-bit WAV ===
out /= np.max(np.abs(out))
out_int16 = np.int16(out * 32767)
write(output_file, sr, out_int16)

print(f"✅ Saved tiled-band signal to {output_file}")
