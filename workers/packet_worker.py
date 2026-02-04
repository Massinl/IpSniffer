from PySide6.QtCore import QThread, Signal
from scapy.all import sniff, IP, TCP, UDP, ICMP


class PacketWorker(QThread):
    packet_captured = Signal(str, str, str)

    def __init__(self, iface=None):
        super().__init__()
        self.running = False
        self.iface = iface  # e.g. "en0"

    def run(self):
        self.running = True

        sniff(
            iface=self.iface,
            prn=self.process_packet,
            store=False,
            stop_filter=lambda _: not self.running
        )

    def process_packet(self, packet):
        if IP not in packet:
            return

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        if TCP in packet:
            proto = "TCP"
        elif UDP in packet:
            proto = "UDP"
        elif ICMP in packet:
            proto = "ICMP"
        else:
            proto = "OTHER"

        self.packet_captured.emit(src_ip, dst_ip, proto)

    def stop(self):
        self.running = False
        self.wait()
