import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QTableView,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit
)
from PySide6.QtCore import (
    QSortFilterProxyModel, 
    Qt
)

from models.packets import PacketModel
from workers.packet_worker import PacketWorker
from models.packet_filter_proxy import PacketFilterProxy



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IP Monitor")
        self.resize(700, 400)
        self.setMinimumSize(500, 300)
        
        # table model
        self.table = QTableView()
        self.model = PacketModel()
        
        self.proxy = PacketFilterProxy(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)


        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        # Buttons
        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.clear_btn = QPushButton("Clear")
        
        self.stop_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)

        self.start_btn.clicked.connect(self.start_capture)
        self.stop_btn.clicked.connect(self.stop_capture)
        self.clear_btn.clicked.connect(self.clear_table)
        
        #seacrh bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search IP...")
        
        self.search_bar.textChanged.connect(
            self.proxy.setFilterFixedString
        )

        # Layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.clear_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.search_bar)
        self.setLayout(layout)

        # Worker
        self.worker = PacketWorker()
        self.worker = PacketWorker(iface="en0") # Need to add a selected interface for this
        self.worker.packet_captured.connect(self.on_packet)
        

    def start_capture(self):
        if not self.worker.isRunning():
            self.worker.start()
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)

    def stop_capture(self):
        if self.worker.isRunning():
            self.worker.stop()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            
    def clear_table(self):
        self.model.beginResetModel()
        self.model.rows.clear()
        self.model.endResetModel()
        self.clear_btn.setEnabled(False)

    def on_packet(self, src_ip, dst_ip, proto):
        self.model.add_row(src_ip, dst_ip, proto)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
