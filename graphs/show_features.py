import dpkt
import matplotlib.pyplot as plt
import numpy as np
from sys import argv

def feature_rates_per_window(pcap_file, window_size=5):

    timestamps = []
    packets = []

    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for ts, buf in pcap:

            eth = dpkt.ethernet.Ethernet(buf)

            feature = None

            if isinstance(eth.data, dpkt.arp.ARP):
                feature = "ARP"

            elif isinstance(eth.data, dpkt.ip.IP):

                ip = eth.data

                if isinstance(ip.data, dpkt.tcp.TCP):

                    tcp = ip.data

                    # OpenFlow channel
                    if tcp.sport == 6653 or tcp.dport == 6653:

                        payload = tcp.data

                        if len(payload) > 1:
                            msg_type = payload[1]

                            if msg_type == 13:
                                feature = "PACKET_OUT"
                            elif msg_type == 10:
                                feature = "PACKET_IN"
                            elif msg_type == 14:
                                feature = "FlowMod"

                    else:
                        feature = "TCP"

                elif isinstance(ip.data, dpkt.udp.UDP):
                    feature = "Forwarding"

            timestamps.append(ts)
            packets.append(feature)

    timestamps = np.array(timestamps)

    start_time = timestamps.min()
    end_time = timestamps.max()

    duration = end_time - start_time

    num_windows = int(duration // window_size) + 1

    feature_windows = {
        "FlowMod": np.zeros(num_windows),
        "PACKET_IN": np.zeros(num_windows),
        "PACKET_OUT": np.zeros(num_windows),
        "ARP": np.zeros(num_windows),
        "TCP": np.zeros(num_windows),
        "Forwarding": np.zeros(num_windows)
    }

    for ts, feature in zip(timestamps, packets):

        index = int((ts - start_time) // window_size)

        if feature in feature_windows:
            feature_windows[feature][index] += 1

    # convert counts → rates
    for feature in feature_windows:
        feature_windows[feature] = feature_windows[feature] / window_size

    return feature_windows, num_windows


pcap_file = argv[1]

feature_rates, num_windows = feature_rates_per_window(pcap_file)

windows = np.arange(num_windows)

plt.figure(figsize=(12,6))

plt.plot(windows, feature_rates["FlowMod"], label="FlowMod rate", color="purple")
plt.plot(windows, feature_rates["PACKET_IN"], label="PACKET_IN rate", color="red")
plt.plot(windows, feature_rates["PACKET_OUT"], label="PACKET_OUT rate", color="orange")
plt.plot(windows, feature_rates["ARP"], label="ARP rate", color="green")
plt.plot(windows, feature_rates["TCP"], label="TCP packet rate", color="blue")
plt.plot(windows, feature_rates["Forwarding"], label="Forwarding rate", color="black")

plt.xlabel("Window Index")
plt.ylabel("Rate (packets/sec)")
if argv[1] == "mixed.pcap":
    plt.title("Feature Behaviour - Testing PCAP")
else:
    plt.title("Feature Behaviour - Training PCAP")

plt.legend()
plt.grid(True)

plt.show()
