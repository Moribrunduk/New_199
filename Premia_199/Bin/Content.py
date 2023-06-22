import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow,QTabWidget,QWidget,QVBoxLayout,QGridLayout
from PyQt5.QtCore import QSettings

sys.path.insert(0,"Premia_199\Bin")
from Main_table import MAIN_WORK_TABLE
sys.path.insert(1,"Premia_199\Bin\Settings_form_window")
from Settings_form_window.Main_settings_window import Settings_window

from Load_file_form import Change_profession
import configparser

        
class MAIN_WINDOW(QMainWindow):
    def __init__(self):
        super(MAIN_WINDOW,self).__init__()
        self.initUI()

    def initUI(self):
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.tabWidget = QTabWidget()
        self.Load_Qset()
        self.Tab_DRGG()
        self.Tab_PZRS()
        self.Tab_FOTO()
        # self.SETTINGS_TAB()
        self.layout = QGridLayout(self.centralwidget)
        self.layout.addWidget(self.tabWidget)
        self.showMaximized()

    def Load_Qset(self):
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("199_settings")
        self.path_with_json_87100 = self.settings.value("Path_with_json_87100")
        self.path_with_input_87100 = self.settings.value("Path_with_input_87100")
        self.path_with_json_87200 = self.settings.value("Path_with_json_87200")
        self.path_with_input_87200 = self.settings.value("Path_with_input_87200")
        self.path_with_json_08300 = self.settings.value("Path_with_json_08300")
        self.path_with_input_08300 = self.settings.value("Path_with_input_08300")

    def Tab_DRGG(self):
        can_load = False #переменная которая позволяет загрузить таблицу
        # проверяем записанный путь к файлу
        if self.path_with_json_87100 == None or self.path_with_input_87100 == None:
            can_load = False
        # проверяем есть ли такой файл
        elif os.path.isfile(self.path_with_json_87100) or os.path.isfile(self.path_with_json_87100):
            can_load = True

        if can_load == False:
            print("[позиция] ---- 1")
            TableDRGG = Change_profession("87100")
            TableDRGG.OK_button.clicked.connect(self.load_tab_drgg)
            self.tabWidget.insertTab(1,TableDRGG, f"Дефектоскописты РГГ(87100)")
            print(self.path_with_json_87100)
            print(self.path_with_input_87100)
        else:
            try:
                print(self.path_with_json_87100)
                TableDRGG = MAIN_WORK_TABLE("87100")
                self.tabWidget.insertTab(1,TableDRGG, f"Дефектоскописты РГГ(87100)")
            except Exception as ex:
                print(ex)
        
    def load_tab_drgg(self):
        TableDRGG = MAIN_WORK_TABLE("87100")
        self.tabWidget.insertTab(1, TableDRGG, f"Дефектоскописты РГГ(87100)")
        self.tabWidget.removeTab(0)
        
  
    def Tab_PZRS(self):
        can_load = False #переменная которая позволяет загрузить таблицу
        # проверяем записанный путь к файлу
        if self.path_with_json_87200 == None or self.path_with_input_87200 == None:
            can_load = False
        # проверяем есть ли такой файл
        elif os.path.isfile(self.path_with_json_87200) or os.path.isfile(self.path_with_json_87200):
            can_load = True

        if can_load == False:
            TablePZRS = Change_profession("87200")
            TablePZRS.OK_button.clicked.connect(self.load_tab_pzrs)
            self.tabWidget.insertTab(2,TablePZRS, f"Дефектоскописты ПЗРС(87200)")
            
        else:
            try:
                print(self.path_with_json_87200)
                TablePZRS = MAIN_WORK_TABLE("87200")
                self.tabWidget.insertTab(2,TablePZRS, f"Дефектоскописты ПЗРС(87200)")
            except Exception as ex:
                print(ex)
        
    
    def load_tab_pzrs(self):
        TablePZRS = MAIN_WORK_TABLE("87200")
        self.tabWidget.insertTab(2, TablePZRS, f"Дефектоскописты ПЗРС(87200)")
        self.tabWidget.removeTab(1)

    
    def Tab_FOTO(self):
        can_load = False #переменная которая позволяет загрузить таблицу
        # проверяем записанный путь к файлу
        if self.path_with_json_08300 == None or self.path_with_input_08300 == None:
            can_load = False
        # проверяем есть ли такой файл
        elif os.path.isfile(self.path_with_json_08300) or os.path.isfile(self.path_with_json_08300):
            can_load = True

        if can_load == False:
            TableFOTO = Change_profession("08300")
            TableFOTO.OK_button.clicked.connect(self.load_tab_foto)
            self.tabWidget.insertTab(3, TableFOTO, f"Фотолаборанты(08300)")
            
        else:
            try:
                TableFOTO = MAIN_WORK_TABLE("08300")
                self.tabWidget.insertTab(3, TableFOTO, f"Фотолаборанты(08300)")
            except Exception as ex:
                print(ex)
                

            

    def load_tab_foto(self):
        TableFOTO = MAIN_WORK_TABLE("08300")
        self.tabWidget.insertTab(3, TableFOTO, f"Фотолаборанты(08300)")
        self.tabWidget.removeTab(2)
    


    def SETTINGS_TAB(self):
        SETTINGS = Settings_window()        
        self.tabWidget.insertTab(4, SETTINGS, f"Настройки") 
    
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MAIN_WINDOW()
    sys.exit(app.exec_())