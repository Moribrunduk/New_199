from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox,QComboBox
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets

import configparser

settings = configparser.ConfigParser()

settings.read("Main\Settings_199\SETTINGS.ini", encoding="utf-8")


class Excell_settings(QWidget):
    def __init__(self):
        super(Excell_settings, self).__init__()
        self.Main()

    def Main(self):
        self.initUI()
        self.action_for_save_data()
        
    def initUI(self):

        # создаем горизонтальную группировку которую вставим в рамку |3 ----
        #                                                            |4 ---- Процент
        #                                                            |5 ---- |30|%

        # self.layout_for_settings = QHBoxLayout()
        # # правый столбик в настройках
        # self.layout_for_procent_in_settings = QVBoxLayout()
        # procent_label = QLabel("% оплаты\n от тарифа")
        # self.procent_text = QLineEdit(settings["87100"]["procent_text"])
        # self.procent_text.setStyleSheet("QLineEdit{font-size: 25px}")
        # self.procent_text.setMaximumSize(50,50)
        

        # self.layout_for_procent_in_settings.addWidget(procent_label)
        # self.layout_for_procent_in_settings.addWidget(self.procent_text)

        # # левый столбик в настройках
        # self.layout_for_group_cvalification = QGridLayout()

        # cv_three = QLabel("    3")
        # cv_three.setMaximumWidth(20)
        # rub = QLabel("P")
        # self.cv_three_tarif = QLineEdit(settings["87100"]["cv_three_tarif"])
        # self.cv_three_tarif.setMaximumWidth(50)
        
        
        # self.layout_for_group_cvalification.addWidget(cv_three,0,0)
        # self.layout_for_group_cvalification.addWidget(self.cv_three_tarif,0,1)
        # self.layout_for_group_cvalification.setAlignment(self.cv_three_tarif,QtCore.Qt.AlignLeft)
        # self.layout_for_group_cvalification.addWidget(rub,0,2)
        # self.layout_for_group_cvalification.setAlignment(rub,QtCore.Qt.AlignLeft)

        # cv_four = QLabel("    4")
        # cv_four.setMaximumWidth(20)
        # rub = QLabel("P")
        # self.cv_four_tarif = QLineEdit(settings["87100"]["cv_four_tarif"])
        # self.cv_four_tarif.setMaximumWidth(50)
        
        # self.layout_for_group_cvalification.addWidget(cv_four,1,0)
        # self.layout_for_group_cvalification.addWidget(self.cv_four_tarif,1,1)
        # self.layout_for_group_cvalification.setAlignment(self.cv_four_tarif,QtCore.Qt.AlignLeft)
        # self.layout_for_group_cvalification.addWidget(rub,1,2)
        # self.layout_for_group_cvalification.setAlignment(rub,QtCore.Qt.AlignLeft)

        # cv_five = QLabel("    5")
        # cv_five.setMaximumWidth(20)
        # rub = QLabel("P")
        # self.cv_five_tarif = QLineEdit(settings["87100"]["cv_five_tarif"])
        # self.cv_five_tarif.setMaximumWidth(50)
        
        # self.layout_for_group_cvalification.addWidget(cv_five,2,0)
        # self.layout_for_group_cvalification.addWidget(self.cv_five_tarif,2,1)
        # self.layout_for_group_cvalification.setAlignment(self.cv_five_tarif,QtCore.Qt.AlignLeft)
        # self.layout_for_group_cvalification.addWidget(rub,2,2)
        # self.layout_for_group_cvalification.setAlignment(rub,QtCore.Qt.AlignLeft)

        # cv_six = QLabel("    6")
        # cv_six.setMaximumWidth(20)
        # rub = QLabel("P")
        # self.cv_six_tarif = QLineEdit(settings["87100"]["cv_six_tarif"])
        # self.cv_six_tarif.setMaximumWidth(50)
        
        # self.layout_for_group_cvalification.addWidget(cv_six,3,0)
        # self.layout_for_group_cvalification.addWidget(self.cv_six_tarif,3,1)
        # self.layout_for_group_cvalification.setAlignment(self.cv_six_tarif,QtCore.Qt.AlignLeft)
        # self.layout_for_group_cvalification.addWidget(rub,3,2)
        # self.layout_for_group_cvalification.setAlignment(rub,QtCore.Qt.AlignLeft)
        
        # self.layout_for_settings.addLayout(self.layout_for_group_cvalification)
        # self.layout_for_settings.addLayout(self.layout_for_procent_in_settings)


        # # создаем группировку в рамке и добавляем туда виджеты
        self.layout_in_frame = QGridLayout()

        self.Main_person_box = QComboBox(self)
        self.Main_person_list = ['Начальник НИТИЦ','И.о. начальника НИТИЦ']
        self.Main_person_box.addItems(self.Main_person_list)
        self.Main_person_box.setEditable(False)


        self.Botiz_box = QComboBox(self)
        self.Botiz_list = ['Начальник БОТиЗ','И.о. начальника БОТиЗ']
        self.Botiz_box.addItems(self.Botiz_list)
        self.Botiz_box.setEditable(False)

        self.Main_person_name_box = QComboBox(self)
        self.Main_person_name_list = ['Власов А.И.','Малыгин И.В.']
        self.Main_person_name_box.addItems(self.Main_person_name_list)
        self.Main_person_name_box.setEditable(True)

        self.Botiz_name_box = QComboBox(self)
        self.Botiz_name_list = ['Львова Н.А.','Михайлова В.А.']
        self.Botiz_name_box.addItems(self.Botiz_name_list)
        self.Botiz_name_box.setEditable(True)



        self.layout_in_frame.addWidget(self.Main_person_box,1,1)
        self.layout_in_frame.addWidget(self.Main_person_name_box,1,2)
        self.layout_in_frame.addWidget(self.Botiz_box,2,1)
        self.layout_in_frame.addWidget(self.Botiz_name_box,2,2)

        # self.layout_in_frame.addLayout(self.layout_for_settings)
       
        # # создаем рамку в которой будут все виджеты
        self.main_group_box = QGroupBox()
        self.main_group_box.setStyleSheet("QGroupBox{font-size: 12px}")
        self.main_group_box.setTitle("Настройки для печати ведомости")
        # self.main_group_box.setMaximumWidth(200)
        # self.main_group_box.setMaximumHeight(200)
        self.main_group_box.setLayout(self.layout_in_frame)

        # # создаем группировку вертикальная
        
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.main_group_box)
        
        # # присваеваем главному экрану групировку виджетов
        self.setLayout(self.main_layout)
    
    def action_for_save_data(self):
        self.Main_person_box.currentIndexChanged.connect(self.save_data)
        self.Main_person_name_box.currentIndexChanged.connect(self.save_data)
        self.Botiz_box.currentIndexChanged.connect(self.save_data)
        self.Botiz_name_box.currentIndexChanged.connect(self.save_data)
    
    def save_data(self):
        print('сохр')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    DRGG = Excell_settings()
    DRGG.show()
    # DPZRS =DefectoscopistPZRS()
    # FOTO = Fotolaborant()
    # FRMD = Form_with_day()
    app.exec_()