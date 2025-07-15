Fs_target = 16000; % Target sampling frequency
num_seconds = 9;    % Target duration in seconds
num_samples_target = Fs_target * num_seconds; % Calculate the desired number of samples

[y, Fs_original] = audioread('44.wav'); %your audio with added noise (music+noise)
y = y(:, 1); % Convert to mono if stereo

disp(['Original sampling frequency: ', num2str(Fs_original), ' Hz']);
disp(['Original number of samples (before processing): ', num2str(length(y))]);

if length(y) > num_samples_target
    % If the audio has more samples than desired, truncate it
    y_truncated = y(1:num_samples_target);
    disp(['Audio truncated to ', num2str(length(y_truncated)), ' samples.']);
elseif length(y) < num_samples_target
    % If the audio has fewer samples, you might want to pad it with zeros
    % or handle it differently based on your application.
    % Here, we'll just use the available samples.
    y_truncated = y;
    disp(['Warning: Audio has fewer samples (', num2str(length(y_truncated)), ') than target (', num2str(num_samples_target), '). Using available samples.']);
else
    % If the number of samples is already the target, no truncation needed
    y_truncated = y;
    disp(['Audio already has the target number of samples: ', num2str(length(y_truncated))]);
end

% Scale to 16-bit integer format (Q15 fixed-point)
y_fixed = round(y_truncated * 2^15);

% Convert to 16-bit 2's complement hexadecimal
y_fixed_hex = dec2hex(mod(y_fixed, 2^16), 4);

% Save as hexadecimal for Verilog readmemh
fid = fopen('44_truncated.txt', 'w'); % output file name 44_truncated.txt where samples are saved
for i = 1:length(y_fixed_hex)
    fprintf(fid, '%s\n', y_fixed_hex(i, :)); % Save each sample on a new line
end
fclose(fid);

disp('Truncated audio samples saved to 44_truncated.txt (Hex Format, 2''s Complement)');
