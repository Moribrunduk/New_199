import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QGridLayout, QPushButton,QVBoxLayout,QLineEdit,QLabel,QMessageBox,QGroupBox,QFileDialog
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings,QDate

from Create_json_file import CREATE_JSON_DATA
from Calendar import CalenderX,MyApp

import xlrd
 
class Interface(QWidget):
    def __init__(self):
        super(Interface,self).__init__()
        self.load_settings()
        self.initUI()
        self.save_settings()
     
        
    def initUI(self):
        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.brigadir_text = QLabel("Бригадир")
        self.brigadir_text.setFont(QFont('Timez New Roman', 15))
        self.brigadir_text.setAlignment(QtCore.Qt.AlignCenter)
        self.brigadir_text.setFixedSize(180,20)
        self.brigadir_input = QLineEdit(self.brigadir_text_input)
        self.brigadir_input.textChanged.connect(self.save_settings)
        self.brigadir_input.setFixedSize(160,50)
        self.button_print = QPushButton("Печать периода")
        self.button_print.setFixedSize(180,200)

        self.brigadir_box_layout = QGroupBox()
        self.layout_in_brigadir_box = QVBoxLayout()
        self.layout_in_brigadir_box.addWidget(self.brigadir_text)
        self.layout_in_brigadir_box.addWidget(self.brigadir_input)
        self.brigadir_box_layout.setLayout(self.layout_in_brigadir_box)
        self.tabel_label = QLabel(self.tabel_label_text)
        self.tabel_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tabel_button = QPushButton("Подключить табель", clicked = self.connect_tabel)
        self.layout_in_tabel_box = QVBoxLayout()
        self.layout_in_tabel_box.addWidget(self.tabel_label)
        self.layout_in_tabel_box.addWidget(self.tabel_button)
        self.tabel_box_layout = QGroupBox()
        self.tabel_box_layout.setLayout(self.layout_in_tabel_box)

        self.right_layout.addWidget(self.brigadir_box_layout)
        self.right_layout.addWidget(self.tabel_box_layout)
        self.right_layout.addWidget(self.button_print)
        
        self.main_layout.addLayout(self.right_layout)
        
        self.setLayout(self.main_layout)
        
        self.setFixedSize(200,400)
        

    def load_settings(self):
        self.calendar_widjet = CalenderX()
        self.cal = MyApp()
        self.a = self.cal.calendar
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("Talons_program")
        if  self.settings.value("brigadir") == None:
            self.brigadir_text_input = "Введите Фамилию И.О."
        elif self.settings.value("brigadir") == "":
            self.brigadir_text_input = "Введите Фамилию И.О."
        else:
            self.brigadir_text_input = self.settings.value("brigadir")
        
        if self.settings.value("file_path") == None :
            self.tabel_label_text = "Табель не подключен"
        elif self.settings.value("file_path") == "":
            self.tabel_label_text = "Табель не подключен"
        else:
            self.tabel_label_text = self.settings.value("file_path")
            work_book = xlrd.open_workbook(self.tabel_label_text)
            work_sheet = work_book.sheet_by_name("Табель")
            self.data_year = work_sheet.cell(1,0).value.replace(" ",'')
            print(self.data_year)
            self.data_month = work_sheet.cell(1,2).value
            print(self.data_month)
            self.tabel_label_text=(f"{self.data_month} {self.data_year}")
            
            

    def create_json(self):
        self.create = CREATE_JSON_DATA()
        self.create.main()  
    
    def connect_tabel(self):
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("Talons_program")

        filepath, filetype = QFileDialog.getOpenFileName(self,
                                "Выбрать файл",
                                ".",
                                "Text Files(*.xls)")
        self.settings.setValue("file_path",filepath)
        try:
            work_book = xlrd.open_workbook(filepath)
            work_sheet = work_book.sheet_by_name("Табель")
            self.data_year = work_sheet.cell(1,0).value.replace(" ",'')
            print(self.data_year)
            self.settings.setValue("Current_year",self.data_year)
            self.data_month = work_sheet.cell(1,2).value
            self.settings.setValue("Current_month",self.data_month)
            print(self.data_month)
            self.tabel_label.setText(f"{self.data_month} {self.data_year}")
            self.create_json()
        except:
            self.tabel_label.setText("Табель не подключен")
            self.settings.setValue("file_path","")
        

    def save_settings(self):
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("Talons_program")
        self.settings.setValue("brigadir",self.brigadir_input.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = Interface()
    mw.show()
    sys.exit(app.exec_())
