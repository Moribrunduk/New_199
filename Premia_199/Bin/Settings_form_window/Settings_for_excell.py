from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QFrame, QLineEdit, QLabel, QVBoxLayout, QPushButton, QGroupBox,QComboBox
import sys


import configparser

class Excell_settings(QWidget):
    def __init__(self):
        super(Excell_settings, self).__init__()
        self.settings = configparser.ConfigParser()
        self.settings.read("Main\Settings_199\SETTINGS.ini", encoding="utf-8")
        self.Load_data()
        self.persons_UI()
        self.vedomost_numbers_UI()
        self.Main_UI()
    
    def Main_UI(self):
        self.Main_layout = QGridLayout()
        self.name_layout = QFrame()
        self.name_layout.setLayout(self.main_layout_names)
        self.vedomost_layout = QFrame()
        self.vedomost_layout.setLayout(self.main_layout_vedomost)

        self.Main_layout.addWidget(self.name_layout,1,1)
        self.Main_layout.addWidget(self.vedomost_layout,2,1)
        self.setFixedSize(300,300)
        self.setLayout(self.Main_layout)

    def persons_UI(self):

        # # создаем группировку в рамке и добавляем туда виджеты
        self.layout_in_frame_names = QGridLayout()
        self.Main_person_box = QComboBox(self)    
        self.Main_person_list = ['Начальник НИТИЦ','И.о. начальника НИТИЦ']
        self.index = self.Main_person_list.index((self.settings["Excell_data"]["current_profession_index"]))
        self.Main_person_box.addItems(self.Main_person_list)
        self.Main_person_box.setCurrentIndex(self.index)
        self.Main_person_box.setEditable(False)


        self.Botiz_box = QComboBox(self)
        self.Botiz_list = ['Начальник БОТиЗ','И.о. начальника БОТиЗ']
        self.Botiz_box.addItems(self.Botiz_list)
        self.index = self.Botiz_list.index((self.settings["Excell_data"]["current_botiz_profession_index"]))
        self.Botiz_box.setCurrentIndex(self.index)
        self.Botiz_box.setEditable(False)

        self.Main_person_name_box = QComboBox(self)
        self.Main_person_name_box.addItems(self.Main_person_name_list)
        self.index = self.Main_person_name_list.index(self.settings["Excell_data"]["Current_main_name_index"])
        self.Main_person_name_box.setCurrentIndex(self.index)
        self.Main_person_name_box.setEditable(True)

        self.Botiz_name_box = QComboBox(self)
        self.Botiz_name_box.addItems(self.Botiz_name_list)
        self.index = self.Botiz_name_list.index(self.settings["Excell_data"]["current_botiz_name_index"])
        self.Botiz_name_box.setCurrentIndex(self.index)
        self.Botiz_name_box.setEditable(True)

        self.layout_in_frame_names.addWidget(self.Main_person_box,1,1)
        self.layout_in_frame_names.addWidget(self.Main_person_name_box,1,2)
        self.layout_in_frame_names.addWidget(self.Botiz_box,2,1)
        self.layout_in_frame_names.addWidget(self.Botiz_name_box,2,2)
        
       
        # # создаем рамку в которой будут все виджеты
        self.main_group_box = QGroupBox()
        self.main_group_box.setStyleSheet("QGroupBox{font-size: 12px}")
        self.main_group_box.setTitle("Настройки для печати ведомости")
        
        self.main_group_box.setLayout(self.layout_in_frame_names)

        # # создаем группировку вертикальная
        
        self.main_layout_names = QVBoxLayout()
        self.main_layout_names.addWidget(self.main_group_box)

        # # присваеваем главному экрану групировку виджетов
        # self.setLayout(self.main_layout_names)
        # return self.main_layout_names
    
    def vedomost_numbers_UI(self):
        # # создаем группировку в рамке и добавляем туда виджеты
        self.layout_in_frame_vedomost = QGridLayout()
        
        self.label_42 = QLabel("42")
        self.text_42 = QLineEdit(self.vedomosti["42"])
        self.text_42.setFixedWidth(35)

        self.label_KSP = QLabel("КCП")
        self.text_KSP = QLineEdit(self.vedomosti["7"])
        self.text_KSP.setFixedWidth(35)

        self.label_50 = QLabel("ССП-Э1")
        self.text_50 = QLineEdit(self.vedomosti["50"])
        self.text_50.setFixedWidth(35)

        self.label_55 = QLabel("ССП-Э2")
        self.text_55 = QLineEdit(self.vedomosti["55"])
        self.text_55.setFixedWidth(35)
        
        self.label_foto = QLabel("ФОТО")
        self.text_foto = QLineEdit(self.vedomosti["foto"])
        self.text_foto.setFixedWidth(35)

        self.label_PZRS = QLabel("ПЗРС")
        self.text_PZRS = QLineEdit(self.vedomosti["PZRS"])
        self.text_PZRS.setFixedWidth(35)

        
        self.layout_in_frame_vedomost.addWidget(self.label_42,1,1)
        self.layout_in_frame_vedomost.addWidget(self.text_42,1,2)
        self.layout_in_frame_vedomost.addWidget(self.label_KSP,1,3)
        self.layout_in_frame_vedomost.addWidget(self.text_KSP,1,4)
        self.layout_in_frame_vedomost.addWidget(self.label_50,2,1)
        self.layout_in_frame_vedomost.addWidget(self.text_50,2,2)
        self.layout_in_frame_vedomost.addWidget(self.label_55,2,3)
        self.layout_in_frame_vedomost.addWidget(self.text_55,2,4)
        self.layout_in_frame_vedomost.addWidget(self.label_foto,3,1)
        self.layout_in_frame_vedomost.addWidget(self.text_foto,3,2)
        self.layout_in_frame_vedomost.addWidget(self.label_PZRS,3,3)
        self.layout_in_frame_vedomost.addWidget(self.text_PZRS,3,4)

        
        # # создаем рамку в которой будут все виджеты
        self.main_group_box_vedomost = QGroupBox()
        self.main_group_box_vedomost.setStyleSheet("QGroupBox{font-size: 12px}")
        self.main_group_box_vedomost.setTitle("Порядковые № ведомостей")

        
        self.main_group_box_vedomost.setLayout(self.layout_in_frame_vedomost)

        # # создаем группировку вертикальная
        
        self.main_layout_vedomost = QVBoxLayout()
        self.main_layout_vedomost.addWidget(self.main_group_box_vedomost)

        # # присваеваем главному экрану групировку виджетов
        # self.setLayout(self.main_layout_vedomost)
        # return self.main_layout_vedomost

    def Load_data(self):
        self.Main_person_name_list = eval(self.settings["Excell_data"]["Main_person_name_list"])
        self.Botiz_name_list = eval(self.settings["Excell_data"]["Botiz_name_list"])
        self.vedomosti = eval(self.settings["Excell_data"]['vedomosti'])

       
    def Save_data(self,settings_file):
        if self.Main_person_name_box.currentText() not in self.Main_person_name_list:
            self.Main_person_name_list.append(self.Main_person_name_box.currentText())

        if self.Botiz_name_box.currentText() not in self.Botiz_name_list:
            self.Botiz_name_list.append(self.Botiz_name_box.currentText())
            
        settings_file["Excell_data"]["Main_person_name_list"] = str(self.Main_person_name_list)
        settings_file["Excell_data"]["Botiz_name_list"] = str(self.Botiz_name_list)
        settings_file["Excell_data"]["Current_profession_index"] = str(self.Main_person_box.currentText())
        settings_file["Excell_data"]["Current_main_name_index"] = str(self.Main_person_name_box.currentText())
        settings_file["Excell_data"]["Current_botiz_profession_index"] = str(self.Botiz_box.currentText())
        settings_file["Excell_data"]["Current_botiz_name_index"] = str(self.Botiz_name_box.currentText())
        settings_file["Excell_data"]["vedomosti"] = str({"42":self.text_42.text(),
                                                    "7":self.text_KSP.text(),
                                                    "50":self.text_50.text(),
                                                    "55":self.text_50.text(),
                                                    'foto':self.text_foto.text(),
                                                    "PZRS":self.text_PZRS.text()})
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    DRGG = Excell_settings()
    DRGG.show()
    
    # DPZRS =DefectoscopistPZRS()
    # FOTO = Fotolaborant()
    # FRMD = Form_with_day()
    app.exec_()