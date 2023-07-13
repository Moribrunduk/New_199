import sys
import os
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QGridLayout,QVBoxLayout, QApplication, QGroupBox, QPushButton,QLineEdit,QLabel)
from configparser import ConfigParser

class Form_with_day(QWidget):
    def __init__(self):
        super(Form_with_day, self).__init__()
        self.settings = ConfigParser()
        self.settings.read("Main\Settings_199\SETTINGS.ini", encoding="utf-8")
        self.InitUI_2()

    def InitUI_2(self):
        self.days_keys = eval(self.settings["Days"]["days_keys"])
        self.days_values = eval(self.settings["Days"]["days_values"])
        self.layout_in_frame = QGridLayout()
        try:
            self.row = 1
            self.label_1_1 = QLineEdit(self.days_keys[0])
            self.label_1_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_1_1,self.row,1)
            self.label_text_1_2 = QLineEdit(self.days_values[0])
            self.layout_in_frame.addWidget(self.label_text_1_2,self.row,2)
            self.row+=1

            self.label_2_1 = QLineEdit(self.days_keys[1])
            self.label_2_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_2_1,self.row,1)
            self.label_text_2_2 = QLineEdit(self.days_values[1])
            self.layout_in_frame.addWidget(self.label_text_2_2,self.row,2)
            self.row+=1

            self.label_3_1 = QLineEdit(self.days_keys[2])
            self.label_3_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_3_1,self.row,1)
            self.label_text_3_2 = QLineEdit(self.days_values[2])
            self.layout_in_frame.addWidget(self.label_text_3_2,self.row,2)
            self.row+=1

            self.label_4_1 = QLineEdit(self.days_keys[3])
            self.label_4_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_4_1,self.row,1)
            self.label_text_4_2 = QLineEdit(self.days_values[3])
            self.layout_in_frame.addWidget(self.label_text_4_2,self.row,2)
            self.row+=1

            self.label_5_1 = QLineEdit(self.days_keys[4])
            self.label_5_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_5_1,self.row,1)
            self.label_text_5_2 = QLineEdit(self.days_values[4])
            self.layout_in_frame.addWidget(self.label_text_5_2,self.row,2)
            self.row+=1

            self.label_6_1 = QLineEdit(self.days_keys[5])
            self.label_6_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_6_1,self.row,1)
            self.label_text_6_2 = QLineEdit(self.days_values[5])
            self.layout_in_frame.addWidget(self.label_text_6_2,self.row,2)
            self.row+=1

            self.label_7_1 = QLineEdit(self.days_keys[6])
            self.label_7_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_7_1,self.row,1)
            self.label_text_7_2 = QLineEdit(self.days_values[6])
            self.layout_in_frame.addWidget(self.label_text_7_2,self.row,2)
            self.row+=1

            self.label_8_1 = QLineEdit(self.days_keys[7])
            self.label_8_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_8_1,self.row,1)
            self.label_text_8_2 = QLineEdit(self.days_values[7])
            self.layout_in_frame.addWidget(self.label_text_8_2,self.row,2)
            self.row+=1

            self.label_9_1 = QLineEdit(self.days_keys[8])
            self.label_9_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_9_1,self.row,1)
            self.label_text_9_2 = QLineEdit(self.days_values[8])
            self.layout_in_frame.addWidget(self.label_text_9_2,self.row,2)
            self.row+=1

            self.label_10_1 = QLineEdit(self.days_keys[9])
            self.label_10_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_10_1,self.row,1)
            self.label_text_10_2 = QLineEdit(self.days_values[9])
            self.layout_in_frame.addWidget(self.label_text_10_2,self.row,2)
            self.row+=1

            self.label_11_1 = QLineEdit(self.days_keys[10])
            self.label_11_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_11_1,self.row,1)
            self.label_text_11_2 = QLineEdit(self.days_values[10])
            self.layout_in_frame.addWidget(self.label_text_11_2,self.row,2)
            self.row+=1

            self.label_12_1 = QLineEdit(self.days_keys[11])
            self.label_12_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_12_1,self.row,1)
            self.label_text_12_2 = QLineEdit(self.days_values[11])
            self.layout_in_frame.addWidget(self.label_text_12_2,self.row,2)
            self.row+=1

            self.label_13_1 = QLineEdit(self.days_keys[12])
            self.label_13_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_13_1,self.row,1)
            self.label_text_13_2 = QLineEdit(self.days_values[12])
            self.layout_in_frame.addWidget(self.label_text_13_2,self.row,2)
            self.row+=1

            self.label_14_1 = QLineEdit(self.days_keys[13])
            self.label_14_1.setFixedWidth(50)
            self.layout_in_frame.addWidget(self.label_14_1,self.row,1)
            self.label_text_14_2 = QLineEdit(self.days_values[13])
            self.layout_in_frame.addWidget(self.label_text_14,self.row,2)
        except IndexError:
            if self.row<14:

                self.empty_label_1 = QLineEdit("")
                self.empty_label_1.setFixedWidth(50)
                self.layout_in_frame.addWidget(self.empty_label_1,self.row,1)
                self.empty_label_text_1 = QLineEdit("")
                self.layout_in_frame.addWidget(self.empty_label_text_1,self.row,2)
                self.row+=1
            if self.row<14:
                self.empty_label_2 = QLineEdit("")
                self.empty_label_2.setFixedWidth(50)
                self.layout_in_frame.addWidget(self.empty_label_2,self.row,1)
                self.empty_label_text_2 = QLineEdit("")
                self.layout_in_frame.addWidget(self.empty_label_text_2,self.row,2)
            
        self.main_group_box = QGroupBox()
        self.main_group_box.setStyleSheet("QGroupBox{font-size: 12px}")
        self.main_group_box.setTitle("Сокращения в табеле")
        self.main_group_box.setLayout(self.layout_in_frame)   
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.main_group_box)
        
        self.setLayout(self.main_layout)
    

    def Save_data(self,settings_file):
            self.days_keys = []
            try:
                self.days_keys.append(self.label_1_1.text())
                self.days_keys.append(self.label_2_1.text())
                self.days_keys.append(self.label_3_1.text())
                self.days_keys.append(self.label_4_1.text())
                self.days_keys.append(self.label_5_1.text())
                self.days_keys.append(self.label_6_1.text())
                self.days_keys.append(self.label_7_1.text())
                self.days_keys.append(self.label_8_1.text())
                self.days_keys.append(self.label_9_1.text())
                self.days_keys.append(self.label_10_1.text())
                self.days_keys.append(self.label_11_1.text())
                self.days_keys.append(self.label_12_1.text())
                self.days_keys.append(self.label_13_1.text())
                self.days_keys.append(self.label_14_1.text())
            except:
                pass
            try:
                if self.empty_label_1.text() !="" and self.empty_label_text_1.text() !="":
                    self.days_keys.append(self.empty_label_1.text())
                if self.empty_label_2.text() !="" and self.empty_label_text_2.text() !="":
                    self.days_keys.append(self.empty_label_2.text())
            except AttributeError:
                pass
            
            self.days_values = []
            try:
                self.days_values.append(self.label_text_1_2.text())
                self.days_values.append(self.label_text_2_2.text())
                self.days_values.append(self.label_text_3_2.text())
                self.days_values.append(self.label_text_4_2.text())
                self.days_values.append(self.label_text_5_2.text())
                self.days_values.append(self.label_text_6_2.text())
                self.days_values.append(self.label_text_7_2.text())
                self.days_values.append(self.label_text_8_2.text())
                self.days_values.append(self.label_text_9_2.text())
                self.days_values.append(self.label_text_10_2.text())
                self.days_values.append(self.label_text_11_2.text())
                self.days_values.append(self.label_text_12_2.text())
                self.days_values.append(self.label_text_13_2.text())
                self.days_values.append(self.label_text_14_2.text())
            except:
                pass
            try:
                if self.empty_label_1.text() !="" and self.empty_label_text_1.text() !="":
                    self.days_values.append(self.empty_label_text_1.text())
                if self.empty_label_2.text() !="" and self.empty_label_text_2.text() !="":
                    self.days_values.append(self.empty_label_text_2.text())
            except AttributeError:
                pass

            while "" in self.days_keys:
                self.days_keys.remove("")
            while  "" in self.days_values:
                self.days_values.remove("")
        
            settings_file["Days"]["days_keys"]=str(self.days_keys)
            settings_file["Days"]["days_values"]=str(self.days_values)
            # with open("Main\Settings_199\SETTINGS_days.ini","w",encoding="utf-8") as config_file:
            #     self.settings.write(config_file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    FRMD = Form_with_day()
    FRMD.show()
    app.exec_()