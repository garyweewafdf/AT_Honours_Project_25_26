import numpy as np
import pandas as pd
from scapy.all import rdpcap, TCP, ARP
from datetime import datetime
import sys

dataset = sys.argv[1]
window_size = 5 
packets = rdpcap(dataset)
records = []

if len(sys.argv) != 3:
    print("process.py <pcap> <npy out>")
    sys.exit()

print(f"[+] Total Packets: {len(packets)}")

for pkt in packets:
    if not hasattr(pkt, "time"):
        continue

    timestamp = float(pkt.time)
    flowmod = 0
    packet_in = 0
    packet_out = 0
    arp_pkt = 0
    tcp_pkt = 0
    forwarded = 0

    if ARP in pkt: # ARP Packet Rate
        arp_pkt = 1

    if TCP in pkt: # TCP Packet Rate
        tcp_pkt = 1
        tcp = pkt[TCP]

        if tcp.sport == 6653 or tcp.dport == 6653:
            payload = bytes(tcp.payload)
            if len(payload) >= 8:
                try:
                    msg_type = payload[1] # OpenFlow Msg Type Rates
                    if msg_type == 10:
                        packet_in = 1
                    elif msg_type == 13:
                        packet_out = 1
                    elif msg_type == 14:
                        flowmod = 1
                except Exception:
                    pass

    if TCP in pkt or ARP in pkt: # Forward Rate
        forwarded = 1

    records.append([timestamp, flowmod, packet_in, packet_out, arp_pkt, tcp_pkt, forwarded])

columns = ["timestamp", "flowmod", "packet_in", "packet_out", "arp", "tcp", "forwarded"]

df = pd.DataFrame(records, columns=columns)
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df.set_index("timestamp", inplace=True)
print("[+] Packet Times:")
print("  [-] First packet:", df.index.min())
print("  [-] Last packet:", df.index.max())
print("  [-] Duration:", df.index.max() - df.index.min())

windowed = df.resample(f"{window_size}s").sum()
windowed = windowed / window_size
windowed = windowed.fillna(0)

print(f"[+] Window Shape: {windowed.shape}")
print("[+] Window Sample:\n")
print(windowed.head())

output_process_file = sys.argv[2]
np.save(output_process_file + ".npy", windowed.values) # Output Processed Dataset
