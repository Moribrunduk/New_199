import sys
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication, QFrame, QPushButton,QLineEdit,QLabel)
from configparser import ConfigParser


from widget_for_main_window import (DefectoscopistRGG , DefectoscopistPZRS, Fotolaborant)
from Days_name_form import Form_with_day
import Settings_for_excell
from Settings_for_excell import Excell_settings



class Settings_window(QWidget):
    
    def __init__(self):
        super(Settings_window,self).__init__()
        self.settings = ConfigParser()
        self.settings.read("Main\Settings_199\SETTINGS.ini", encoding="utf-8")
        self.initUI()
        
    # создаем функцию которая переопределяет хозяина виджета
    def DRGG_FUNC(self):
        self.DRGG = DefectoscopistRGG()
        return self.DRGG.main_layout
    
    def DPZRS_FUNC(self):
        self.DPZRS = DefectoscopistPZRS()
        return self.DPZRS.main_layout
    
    def FOTO_FUNC(self):
        self.FOTO = Fotolaborant()
        return self.FOTO.main_layout
    
    def DAYS_FUNC(self):
        self.DAYS = Form_with_day()
        return self.DAYS.main_layout
    def EXCELL_FUNC(self):
        self.EXCELL_SETTINGS = Excell_settings()
        return self.EXCELL_SETTINGS.Main_layout

    def Save_data(self):
        self.settings_file = ConfigParser()
        self.settings_file.read("Main\Settings_199\SETTINGS.ini", encoding="utf-8")

        self.DRGG.Save_data(self.settings_file)
        self.DPZRS.Save_data(self.settings_file)
        self.FOTO.Save_data(self.settings_file)
        self.DAYS.Save_data(self.settings_file)
        self.EXCELL_SETTINGS.Save_data(self.settings_file)

        with open("Main\Settings_199\SETTINGS.ini","w",encoding="utf-8") as config_file:
            self.settings_file.write(config_file)


    def initUI(self):

        # создаем рамки
        DRGG = self.DRGG_FUNC()
        self.form_for_rgg = QFrame()
        self.form_for_rgg.setLayout(DRGG)
        
        DPZRS = self.DPZRS_FUNC()
        self.form_for_pzrs = QFrame()
        self.form_for_pzrs.setLayout(DPZRS)
        
        FOTO = self.FOTO_FUNC()
        self.form_for_foto = QFrame()
        self.form_for_foto.setLayout(FOTO)
        DAYS = self.DAYS_FUNC()
        self.form_for_days = QFrame()
        self.form_for_days.setLayout(DAYS)

        EXCELL = self.EXCELL_FUNC()
        self.form_excell_settings = QFrame()
        self.form_excell_settings.setLayout(EXCELL)
        # группировка для рамок
        self.layout_for_load_widget = QGridLayout()
        self.layout_for_load_widget.addWidget(self.form_for_rgg,0,0)
        self.layout_for_load_widget.addWidget(self.form_for_pzrs,1,0)
        self.layout_for_load_widget.addWidget(self.form_for_foto,2,0)
        self.layout_for_load_widget.addWidget(self.form_for_days,0,1,2,1)
        self.layout_for_load_widget.addWidget(self.form_excell_settings,2,1)

        self.layout_for_load_widget.setColumnMinimumWidth(1,100)
        self.layout_for_load_widget.setColumnStretch(1,100)
        self.layout_for_load_widget.setAlignment(self.form_for_days,QtCore.Qt.AlignTop)
        # кнопка сохранения
        self.button_save = QPushButton()
        self.button_save.setText("Cохранить")
        self.button_save.clicked.connect(self.Save_data)
        # self.button_save_2 = QPushButton()
        # self.button_save_2.setText("ока")
        # self.button_save_2.clicked.connect(self.button_save.click)
        self.layout_for_load_widget.addWidget(self.button_save,3,2)
        # self.layout_for_load_widget.addWidget(self.button_save_2,4,2)
        # основная группировка
        self.setLayout(self.layout_for_load_widget)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Settings_window()
    w.show()
    sys.exit(app.exec_())