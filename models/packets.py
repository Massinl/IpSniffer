from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex


class PacketModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.headers = ["Source IP", "Destination IP", "Protocol"]
        self.rows = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self.rows[index.row()][index.column()]

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None

    def add_row(self, src_ip, dst_ip, proto):
        row = len(self.rows)
        self.beginInsertRows(QModelIndex(), row, row)
        self.rows.append([src_ip, dst_ip, proto])
        self.endInsertRows()
