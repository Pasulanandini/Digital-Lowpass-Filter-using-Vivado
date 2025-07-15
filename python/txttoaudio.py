import numpy as np
import wave

# === CONFIG ===
input_txt = "44filtered64.txt"
output_wav = "44filtered64.wav"
Fs = 16000  # Sample rate

# === 1. Read and fix hex samples ===
samples = []
with open(input_txt, "r") as f:
    for idx, line in enumerate(f):
        hex_val = line.strip()
        if not hex_val:
            continue
        try:
            val = int(hex_val, 16)
            if val > 0xFFFF:
                raise ValueError(f"Line {idx}: Value {val} exceeds 16-bit range.")
            # Convert to signed 16-bit manually
            if val >= 0x8000:
                val = val - 0x10000  # Two's complement
            samples.append(val)
        except ValueError as e:
            print(f"⚠️ Skipping invalid line {idx}: {hex_val} — {e}")

# Convert safely to np.int16
samples_np = np.array(samples, dtype=np.int16)

# === 2. Write to WAV ===
with wave.open(output_wav, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16-bit
    wf.setframerate(Fs)
    wf.writeframes(samples_np.tobytes())

print(f"✅ Successfully saved WAV file as: {output_wav}")
