import numpy as np
from rtlsdr import RtlSdr
import csv
import time
from datetime import datetime

sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 100e6
sdr.gain = 'auto'

def get_rssi(samples):
    """Calculate RSSI in dBm"""
    power = np.mean(np.abs(samples)**2)
    rssi = 10 * np.log10(power)
    return rssi

def get_boresight(samples, sample_rate, center_freq):
    """Find boresight (frequency of peak signal)"""
    fft = np.fft.fftshift(np.fft.fft(samples))
    power = np.abs(fft)**2
    freqs = np.fft.fftshift(np.fft.fftfreq(len(samples), 1/sample_rate))
    peak_idx = np.argmax(power)
    boresight = center_freq + freqs[peak_idx]
    return boresight

def get_beamwidth(samples, sample_rate):
    """Estimate beamwidth from power spectrum"""
    fft = np.fft.fftshift(np.fft.fft(samples))
    power = np.abs(fft)**2
    freqs = np.fft.fftshift(np.fft.fftfreq(len(samples), 1/sample_rate))
    peak_idx = np.argmax(power)
    peak_power = power[peak_idx]
    half_power = peak_power / 2
    above_half = np.where(power >= half_power)[0]
    if len(above_half) > 1:
        beamwidth = abs(freqs[above_half[-1]] - freqs[above_half[0]])
    else:
        beamwidth = 0
    return beamwidth

# Write CSV header once before the loop
filename = "antenna_log.csv"
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'RSSI_dBm', 'Boresight_MHz', 'Beamwidth_MHz'])

print("Taking measurements... Press Ctrl+C to stop")

try:
    while True:
        samples = sdr.read_samples(256 * 1024)
        rssi = get_rssi(samples)
        boresight = get_boresight(samples, sdr.sample_rate, sdr.center_freq)
        beamwidth = get_beamwidth(samples, sdr.sample_rate)

        print(f"RSSI:      {rssi:.2f} dBm")
        print(f"Boresight: {boresight/1e6:.4f} MHz")
        print(f"Beamwidth: {beamwidth/1e6:.4f} MHz")

        # Append to CSV
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now(), rssi, boresight/1e6, beamwidth/1e6])

        print(f"Saved to {filename}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped.")
    sdr.close()
