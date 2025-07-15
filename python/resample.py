import soundfile as sf
from scipy.signal import resample
import numpy as np
import os

def resample_audio(input_path, output_path, target_fs=16000):
    # Load original audio
    data, original_fs = sf.read(input_path)
    
    # Convert to mono if stereo
    if data.ndim > 1:
        data = np.mean(data, axis=1)

    if original_fs == target_fs:
        print(f"{input_path} already at {target_fs} Hz. Saving copy as {output_path}")
        sf.write(output_path, data, target_fs)
        return

    # Compute new number of samples
    duration = len(data) / original_fs
    target_samples = int(duration * target_fs)

    # Resample
    data_resampled = resample(data, target_samples)

    # Save to new file
    sf.write(output_path, data_resampled, target_fs)
    print(f"✅ Resampled {input_path} from {original_fs} → {target_fs} Hz. Saved as {output_path}")

# === Files to Resample ===
files_to_resample = {
    "music_file.wav": "music_file_16k.wav",
    "noisy_audio_white.wav": "noisy_audio_white_16k.wav"
    # Add more if needed
}

for original, resampled in files_to_resample.items():
    if os.path.exists(original):
        resample_audio(original, resampled)
    else:
        print(f"⚠️ File not found: {original}")
