import time
import random
from PySide6.QtCore import QThread, Signal


class PacketWorker(QThread):
    packet_captured = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True
        protocols = ["TCP", "UDP", "ICMP"]

        while self.running:
            src_ip = f"192.168.1.{random.randint(1, 254)}"
            dst_ip = random.choice(["8.8.8.8", "1.1.1.1", "224.0.0.1"])
            proto = random.choice(protocols)

            self.packet_captured.emit(src_ip, dst_ip, proto)
            
            
        # --DONT PUT THIS TOO LOW OR IT WILL FLOOD YOUR PC AND CRASH ---
            time.sleep(0.5)
        # --------------------------------------------------------------
        
        
    def stop(self):
        self.running = False
        self.wait()
