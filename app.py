import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableView, QVBoxLayout
from PySide6.QtCore import QAbstractTableModel, Qt


class TableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.headers = ["Source IP", "Destination IP", "Protocol"]

    def rowCount(self, parent=None):
        return 0

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTableView Base")
        self.resize(700, 400)

        self.table = QTableView()
        self.model = TableModel()
        self.table.setModel(self.model)

        # DO NOT enable sorting yet
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_styles()

    def load_styles(self):
        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
