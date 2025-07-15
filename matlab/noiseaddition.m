% --- Configuration ---
clean_audio_file = 'music_file.mp3'; % Replace with your clean audio file
output_noisy_file = 'noisy_audio_white_1.wav'; % Name for the output noisy file
noise_level_db = 10; % Desired SNR in dB (lower value = more noise)

% --- Load Clean Audio File ---
try
    [clean_audio, fs] = audioread(clean_audio_file);
    clean_audio = clean_audio(:, 1); % Convert to mono if stereo
catch ME
    error('Error reading clean audio file: %s', ME.message);
end

% --- Calculate Signal Power ---
signal_power = mean(clean_audio.^2);

% --- Calculate Noise Power ---
target_snr_linear = 10^(noise_level_db / 10);
noise_power = signal_power / target_snr_linear;

% --- Generate White Gaussian Noise ---
noise = sqrt(noise_power) * randn(size(clean_audio));

% --- Add Noise to Clean Audio ---
noisy_audio = clean_audio + noise;

% --- Normalize to Avoid Clipping (Optional but Recommended) ---
% Find the maximum absolute value of the noisy audio
max_val = max(abs(noisy_audio));
% If the maximum value exceeds 1, normalize
if max_val > 1
    noisy_audio = noisy_audio / max_val;
    disp(['Warning: Noisy audio clipped. Normalized to prevent exceeding [-1, 1].']);
end

% --- Write Noisy Audio to File ---
try
    audiowrite(output_noisy_file, noisy_audio, fs);
    disp(['White Gaussian noise added. Noisy audio saved as: ', output_noisy_file]);
    disp(['Target SNR: ', num2str(noise_level_db), ' dB (approximately).']);
catch ME
    error('Error writing noisy audio file: %s', ME.message);
end

% --- Optional: Verify SNR ---
signal_power_actual = mean(clean_audio.^2);
noise_power_actual = mean(noise.^2);
snr_actual_db = 10 * log10(signal_power_actual / noise_power_actual);
disp(['Actual SNR of generated noisy audio: ', num2str(snr_actual_db), ' dB.']);

% --- Optional: Listen to the Audio ---
play_audio = input('Play original and noisy audio? (y/n): ', 's');
if strcmpi(play_audio, 'y')
    sound(clean_audio, fs);
    pause(length(clean_audio) / fs);
    sound(noisy_audio, fs);
end
