# Digital-Lowpass-Filter-using-Vivado
1.1 Field and Area of Work
The project belongs to the field of Digital Signal Processing (DSP), a vital branch of electronics and communication engineering concerned with the analysis and manipulation of signals in the digital domain. DSP techniques enable a wide range of real-time signal operations such as filtering, compression, modulation, and noise reduction. Within DSP, one of the most prominent and essential areas is digital filter design — the process of shaping a signal’s frequency content to achieve desired characteristics. Filters are integral to virtually every DSP application, including audio processing, wireless communications, biomedical instrumentation, speech recognition, and radar systems.
Among the two primary types of digital filters, Infinite Impulse Response (IIR) and Finite Impulse Response (FIR). FIR filters are widely preferred for applications demanding high accuracy, linear phase response, and guaranteed stability. This project specifically focuses on FIR filter design, with an emphasis on low-pass filtering, which permits low-frequency components of a signal to pass while attenuating unwanted high-frequency components.
1.2 Topic Overview: Low-Pass FIR Filter
A low-pass FIR filter is designed to suppress the frequency components above a specified cutoff frequency while allowing lower frequencies to pass through unaffected. This makes it ideal for applications such as audio enhancement, removal of high-frequency noise, anti-aliasing prior to analog-to-digital conversion, and biomedical signal filtering. FIR filters are implemented as linear convolution operations between the input signal and a set of pre-determined coefficients. These filters inherently possess several advantages:
Guaranteed stability due to the absence of feedback.
Capability to maintain linear phase (i.e., no phase distortion).
Flexibility in designing sharp transitions between passband and stopband by increasing filter order.
Ease of implementation in fixed-point arithmetic, making them suitable for hardware like FPGAs.
However, one challenge with FIR filters is that higher performance requires a higher filter order, which increases computational complexity. This trade-off between performance and efficiency forms the core design consideration in this work.
1.3 Existing Systems and Their Limitations
	Traditionally, analog filters were used to perform signal conditioning. These are hardware-based solutions built with components like resistors, capacitors, and inductors. While effective, analog filters suffer from issues such as component tolerances, lack of reconfigurability, and vulnerability to environmental changes like temperature and aging.
On the digital side, IIR filters offer computational efficiency because they require fewer coefficients for a given performance. However, IIR filters present significant drawbacks:
They can become unstable, especially at higher orders.
They do not preserve the phase of signals due to their non-linear phase response.
Their feedback structure makes them more sensitive to quantization errors, especially in fixed-point arithmetic.
Because of these limitations, many modern applications that require precision, predictability, and linear phase behavior turn to FIR filters, despite their higher order requirement.
1.4 Motivation for FIR Low-Pass Filtering
	In many real-time signal applications — particularly those involving audio signals, biomedical signals (e.g., ECG), or sensor data — preserving the waveform’s shape is critical. Any distortion introduced due to non-linear phase response or instability can compromise signal integrity and lead to poor outcomes. FIR filters address these concerns directly.
For example, in an audio processing system, it is vital that the output sound remains true to the original, with only the noise removed. A linear phase FIR filter achieves this by ensuring all frequency components of the signal are delayed equally, preserving temporal relationships.
This project is motivated by the need to design FIR filters that can effectively clean noisy signals while maintaining important signal characteristics — particularly in the passband. Additionally, the desire to implement these filters on real-time platforms such as FPGAs necessitates the exploration of filter orders, coefficient quantization, and the trade-offs involved.
1.5 Aim of the Project
	The aim of this project is to design, simulate, analyze, and implement low-pass FIR filters of various orders using both software and hardware-oriented tools. The primary objectives are:
To generate FIR low-pass filter coefficients using standard windowing techniques (e.g., rectangular window).
To analyze the frequency response of these filters across different orders (2, 4, 8, 16, 32, 64).
To apply the filters to real-world signals (such as noisy audio or chirp signals) and measure performance using metrics like SNR (Signal-to-Noise Ratio) in the passband and stopband.
To visualize the results in both time and frequency domains using FFT plots, spectrograms, and waveform overlays.
To evaluate the trade-off between filter performance and complexity.
To prepare the filter for hardware implementation (such as using Xilinx Vivado) for deployment in FPGA systems.
Ultimately, the project aims to validate the superiority of FIR filters in applications requiring phase fidelity and stability, and to  demonstrate how thoughtful design and analysis can lead to practical, real-time digital filtering solutions.

