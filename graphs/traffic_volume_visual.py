import dpkt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


def traffic_volume_per_window(pcap_file, num_windows=361):
    timestamps = []
    sizes = []

    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            timestamps.append(ts)
            sizes.append(len(buf))

    timestamps = np.array(timestamps)
    sizes = np.array(sizes)

    timestamps = timestamps - timestamps.min()
    duration = timestamps.max()

    window_size = duration / num_windows
    traffic_volume = np.zeros(num_windows)

    for t, s in zip(timestamps, sizes):
        index = int(t // window_size)
        if index < num_windows:
            traffic_volume[index] += s

    return traffic_volume


training_pcap = "" # un-processed training PCAP
testing_pcap = "" # un-processed testing pcap

train_volume = traffic_volume_per_window(training_pcap)
test_volume = traffic_volume_per_window(testing_pcap)

windows = np.arange(361)

# anomaly ranges
anomaly_ranges = [(127,154), (240,277)]

def is_anomaly(i):
    for start, end in anomaly_ranges:
        if start <= i <= end:
            return True
    return False


plt.figure(figsize=(12,6))

# Training traffic
plt.plot(windows, train_volume, label="Training Traffic", color="green")

# Testing traffic with anomaly highlighting
for i in range(len(windows)-1):

    if is_anomaly(i):
        plt.plot(windows[i:i+2], test_volume[i:i+2], color="red")
    else:
        plt.plot(windows[i:i+2], test_volume[i:i+2], color="orange")

plt.xlabel("Window Index (0–360)")
plt.ylabel("Traffic Volume (Bytes)")
plt.title("Traffic Volume per Window with True Anomalies Highlighted")

legend_elements = [
    Line2D([0], [0], color='green', lw=2, label='Training PCAP'),
    Line2D([0], [0], color='orange', lw=2, label='Testing PCAP'),
    Line2D([0], [0], color='red', lw=2, label='FRF Execution')
]

plt.legend(handles=legend_elements)
plt.grid(True)

plt.show()
