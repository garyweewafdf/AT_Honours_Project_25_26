import dpkt
import matplotlib.pyplot as plt
import numpy as np
from sys import argv


def protocol_counts_per_time_window(pcap_file, window_size=5):

    timestamps = []
    packet_protocols = []

    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            protocol = "Other"

            if isinstance(eth.data, dpkt.arp.ARP):
                protocol = "ARP"

            elif isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data

                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp = ip.data
                    
                    if tcp.sport == 6653 or tcp.dport == 6653:
                        protocol = "OpenFlow"
                    else:
                        protocol = "TCP"

                elif isinstance(ip.data, dpkt.udp.UDP):
                    protocol = "UDP"

                elif ip.p == 1:
                    protocol = "ICMP"

            timestamps.append(ts)
            packet_protocols.append(protocol)

    timestamps = np.array(timestamps)

    start_time = timestamps.min()
    end_time = timestamps.max()

    total_duration = end_time - start_time
    num_windows = int(total_duration // window_size) + 1

    protocol_windows = {
        "TCP": np.zeros(num_windows),
        "UDP": np.zeros(num_windows),
        "ICMP": np.zeros(num_windows),
        "ARP": np.zeros(num_windows),
        "OpenFlow": np.zeros(num_windows)
    }

    protocol_totals = {
        "TCP": 0,
        "UDP": 0,
        "ICMP": 0,
        "ARP": 0,
        "OpenFlow": 0
    }

    for ts, proto in zip(timestamps, packet_protocols):
        index = int((ts - start_time) // window_size)
        if proto in protocol_windows:
            protocol_windows[proto][index] += 1
            protocol_totals[proto] += 1

    total_packets = sum(protocol_totals.values())
    protocol_percentages = {
        proto: (count / total_packets) * 100 if total_packets > 0 else 0
        for proto, count in protocol_totals.items()
    }

    return protocol_windows, protocol_percentages, num_windows


pcap_file = argv[1]
protocol_windows, protocol_percentages, num_windows = protocol_counts_per_time_window(pcap_file)
windows = np.arange(num_windows)

plt.figure(figsize=(12,6))

plt.plot(
    windows,
    protocol_windows["TCP"],
    label=f"TCP (excluding OpenFlow) {protocol_percentages['TCP']:.1f}%",
    color="blue"
)

plt.plot(
    windows,
    protocol_windows["UDP"],
    label=f"UDP {protocol_percentages['UDP']:.1f}%",
    color="orange"
)

plt.plot(
    windows,
    protocol_windows["ICMP"],
    label=f"ICMP {protocol_percentages['ICMP']:.1f}%",
    color="green"
)

plt.plot(
    windows,
    protocol_windows["ARP"],
    label=f"ARP {protocol_percentages['ARP']:.1f}%",
    color="pink"
)

plt.plot(
    windows,
    protocol_windows["OpenFlow"],
    label=f"OpenFlow {protocol_percentages['OpenFlow']:.1f}%",
    color="purple"
)

plt.xlabel("Window Index (5s)")
plt.ylabel("Packet Count")
if argv[1] == "mixed.pcap":
    plt.title("Protocol Distribution - Testing PCAP")
else:
    plt.title("Protocol Distribution - Training PCAP")

plt.legend()
plt.grid(True)

plt.show()
