from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys, requests
from dblight_connect import db, cursor
from datetime import datetime
from sheetapi import appendsheet, deleterow, clear_except_first

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("light.ui", self)
        self.btn_on.clicked.connect(self.LED_ON)
        self.btn_off.clicked.connect(self.LED_OFF)
        self.btn_reset.clicked.connect(self.reset_table)

        self.showstatus()
    
    def say_hi(self):
        QMessageBox.information(self, 'Information', 'Hello World!')
    
    def LED_ON(self):
        url = 'https://72a2-2001-44c8-6208-3f46-00-1.ngrok-free.app/'
        response = requests.get(url+'on')
        if response.status_code == 200:
            QMessageBox.information(self, 'Information', 'LED_ON')
            self.insert_light("LED_ON")
        else:
            pass
    
    def LED_OFF(self):
        url = 'https://72a2-2001-44c8-6208-3f46-00-1.ngrok-free.app/'
        response = requests.get(url+'off')
        if response.status_code == 200:
            QMessageBox.information(self, 'Information', 'LED_OFF')
            self.insert_light("LED_OFF")
        else:
            pass
    
    def insert_light(self, text):
        status = text
        now = datetime.now()
        day = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")
        #print(time)
        sql = 'insert into light(status, day, time) values(?, ?, ?);'
        values = (status, day, time)

        rs = cursor.execute(sql, values)
        db.commit()
        if rs.rowcount>0:
            QMessageBox.information(self, 'Information', f'สถานะ: {status}\nเวลา:{time} นาที\n')
            self.showstatus()
            appendsheet(status, day, time)
        else:
            QMessageBox.warning(self, 'warning', 'Unable to insert!')
    
    def showstatus(self):
        sql = "SELECT * FROM light"
        status = cursor.execute(sql).fetchall()
        #print(status)
        n = len(status)
        self.text_status.setRowCount(n)
        row = 0
        for sta in status: #sta => [0] (1, 'LED_ON', '12:00:00')
            self.text_status.setItem(row, 0, QTableWidgetItem(str(sta[0])))
            self.text_status.setItem(row, 1, QTableWidgetItem(sta[1]))
            self.text_status.setItem(row, 2, QTableWidgetItem(sta[2]))
            self.text_status.setItem(row, 3, QTableWidgetItem(sta[3]))
            row += 1

        
    
    def reset_table(self):
        cursor.execute("DROP TABLE IF EXISTS light;")

        rs = cursor.execute("""
        CREATE TABLE light (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT,
            day TEXT,         
            time TEXT
        );
        """)
        db.commit()
        if rs.rowcount== -1:
            QMessageBox.information(self, 'Information', f'ล้างข้อมูลแล้ว')
            self.showstatus()
            clear_except_first()

        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()