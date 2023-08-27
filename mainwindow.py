from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QObject
from page_scaner import PageScaner


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/MainWindow.ui', self)

        self.pushButton.clicked.connect(self.pushButton_click)
        self.pushButton_2.clicked.connect(self.pushButton_2_click)
        self.pushButton_3.clicked.connect(self.pushButton_3_click)

    def task_finished(self) -> None:
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setText('Dừng')

        QMessageBox.information(self, 'Thông báo', 'Đã dừng' if not self.scaner.running else 'Hoàn thành')

    def pushButton_3_click(self) -> None:
        self.pushButton_3.setText('Dừng...')
        self.scaner.stop()

    def pushButton_2_click(self) -> None:
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)

        config = QObject()
        config.max_thread_count = self.spinBox.value()
        config.get_max_page_count = lambda: self.tableWidget.rowCount()
        config.get_page_id = lambda row: self.tableWidget.item(row, 1)

        self.scaner = PageScaner(config)
        self.scaner.finished.connect(self.task_finished)
        self.scaner.update_page_name.connect(lambda row, text: self.tableWidget.setItem(row, 0, QTableWidgetItem(text)))
        self.scaner.update_likes.connect(lambda row, text: self.tableWidget.setItem(row, 2, QTableWidgetItem(text)))
        self.scaner.update_address.connect(lambda row, text: self.tableWidget.setItem(row, 3, QTableWidgetItem(text)))
        self.scaner.update_verified.connect(lambda row, text: self.tableWidget.setItem(row, 4, QTableWidgetItem(text)))
        self.scaner.start()

    def pushButton_click(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open', '.', 'Text Documents (*.txt)')
        if not file_path:
            return
        
        with open(file_path, encoding='utf-8') as file:
            lines = file.readlines()

        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

        for line in lines:
            line = line.strip()

            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 1, QTableWidgetItem(line))

        self.label_7.setText(str(self.tableWidget.rowCount()))
        self.lineEdit.setText(file_path)
        self.pushButton_2.setEnabled(self.tableWidget.rowCount() > 0)