
import configparser
import json
import os
import sys
import openpyxl

from Create_final_excell_file_new import CREATE_EXCELL
from Load_file_form import Change_profession
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QColor, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                             QHeaderView, QMainWindow, QMessageBox,
                             QPushButton, QTableView, QVBoxLayout, QWidget)
from Table_element.All_money_window import ALL_MONEY_WINDOW

sys.path.insert(1,"Main\Bin")
from Avtorization_window import Avtorization_main_window


class MAIN_WORK_TABLE(QWidget): 
    
    def __init__(self,proffession_number):
        self.proffession_number = str(proffession_number)
        super(MAIN_WORK_TABLE, self).__init__()
        self.initUI()

    def LayoutAMW(self):
        self.AMW = ALL_MONEY_WINDOW(self.proffession_number)
        return self.AMW.layout
       
    def initUI(self):

        self.setWindowTitle("Расчет 199 премии")
        self.resize(500,300)
        # таблица с рабочим полем
        self.model = QStandardItemModel()
        self.data_table_view = QTableView()
        self.data_table_view.setModel(self.model)
        
        # таблица с суммами
        self.model_summ = QStandardItemModel()
        self.summ_table_view = QTableView()
        self.summ_table_view.setModel(self.model_summ)
        
        # форма с общей суммой
        ALL_SUMM = self.LayoutAMW()
        self.form_wit_summ = QFrame()
        self.form_wit_summ .setLayout(ALL_SUMM)

        self.top_layout = QGridLayout()
        self.main_layout = QVBoxLayout()
        self.Button_layout = QVBoxLayout()

        self.button = QPushButton("Создать файл для печати")
        self.button.clicked.connect(self.Button_create_excell_file_connect_to_avtorization)
        self.button2 = QPushButton("Выбрать другой файл")
        self.button2.clicked.connect(self.ChangeFile)

        self.money_layout = QVBoxLayout()
        self.money_layout.addWidget(self.summ_table_view)
        self.money_layout.addWidget(self.form_wit_summ)


        self.top_layout.addWidget(self.data_table_view,0,1)
        self.top_layout.addLayout(self.money_layout,0,2)
        # self.top_layout.addWidget(self.form_wit_summ ,0,1,3,3)
        self.Button_layout.addWidget(self.button)
        self.Button_layout.addWidget(self.button2)

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.Button_layout)
        self.setLayout(self.main_layout)

        
        self.save_input_user_for_load_in_file = {}
        self.save_input_user_for_summ_in_file = {}
        

        self.settings = QSettings("NITIC")
        self.settings.beginGroup("199_settings")
        self.path_with_json = self.settings.value(f"Path_with_json_{self.proffession_number}")
        self.path_with_input = self.settings.value(f"Path_with_input_{self.proffession_number}")
        self.settings.endGroup()

        with open(f"{self.path_with_json}", "r", encoding="utf-8") as file:
                    self.all_data = json.load(file)
        

        self.tabels = self.all_data["шифр"][self.proffession_number]["Табельный"]

        self.AddDataToDataTable()
        self.AddDataToSummTable()
        self.AddReplaceCell_DataTable()
        self.load_data()
        self.ParametersDataTable()
        self.ParametersSummTable()
        
        try:
            self.PrintSumm()
        except Exception as ex:
            print(ex)
        self.summ_pay()

    def Button_create_excell_file_action(self):
        
        self.year=self.all_data["шифр"][self.proffession_number]["Информация"]["год"]
        self.month = self.all_data["шифр"][self.proffession_number]["Информация"]["месяц"]

        self.settings = QSettings("NITIC")
        self.settings.beginGroup("199_settings")
        self.path_with_input = self.settings.value(f"Path_with_input_{self.proffession_number}")
        self.settings.endGroup()

        self.TEMP = configparser.ConfigParser()
        self.TEMP.read(f'{self.path_with_input}')


        # Проверка доступа
      
        access_path = self.path_with_input.split("\\")[2]
        self.settings.endGroup()
        print(f"{access_path}")

        self.settings.beginGroup("GOD_parameters")
        Current_user = self.settings.value("Current_user")


        self.settings.beginGroup('Users_access')
        user_access = self.settings.value(self.AV.text_name.text())
        print(user_access)
        
        if user_access == None:
            user_access = []
        
        if self.proffession_number == "87100" or "08300":
            access_path = "Woman"

        if access_path in user_access:
            if os.path.isfile(f'{self.path_with_input}'):

                if eval(self.TEMP["General"]["for_summ"]) == {}:
                    QMessageBox.warning(
                        self, 'Ошибка', 'Ошибка: замещающих нет')   
                else:
                    workbook = openpyxl.Workbook()
                    worksheet = workbook.active
                    self.CE = CREATE_EXCELL(proffession_number=self.proffession_number,
                                            worksheet=worksheet,
                                            workbook=workbook)
                    self.CE.Main()

                    
            else:
                QMessageBox.warning(
                        self, 'Ошибка', 'Ошибка: замещающих нет')
        else:
            QMessageBox.warning(
                        self, 'Ошибка', 'Ошибка: Нет доступа к печати ведомостей')

    def Button_create_excell_file_connect_to_avtorization(self):
        
        self.AV = Avtorization_main_window.AVTORIZATION_WINDOW(self.Button_create_excell_file_action)

        
        
    def ChangeFile(self):
        self.CHP = Change_profession(self.proffession_number)
        self.CHP.show()
        self.CHP.OK_button.clicked.connect(self.Restart)

    def Restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)
        
        
        
    def AddDataToDataTable(self):

#ДОБАВЯЕМ РАБОЧИЙ КАЛЕНДАРЬ
        x = 0
        work_column=3
        for data in range(1,33):
            if data <16:
                item = QStandardItem(str(data))
                
                #делаем его нередактируемым
                item.setEditable(False)
                self.model.setItem(x, work_column, item)
                work_column+=1

            elif data == 16 :
                item = QStandardItem("-")
                item.setEditable(False)
                self.model.setItem(x, work_column, item)
                work_column+=1
                
            else:
                item = QStandardItem(str(data-1))
                item.setEditable(False)
                self.model.setItem(x+1, work_column-16, item)
                work_column+=1
        
# ДОБАВЛЯЕМ ПОЧАСОВОЙ КАЛЕНДАРЬ(РАБОЧИЙ ГРАФИК)
        # первое значение бэкграунда - окрашиваем календарь почасовой
        # второй значение бэкграунда - окрашиваем дневной календарь
        
        self.time_calendar = self.all_data["шифр"][self.proffession_number]["Рабочий календарь"]
        x = 0
        work_column=19
        for i,value in enumerate(self.time_calendar.values()):
            if i <15:
                item = QStandardItem(str(value))
                item.setEditable(False)
                self.model.setItem(x, work_column, item)
                # окрашиваем выходные в красный
                if value == "-":
                    self.model.item(x, work_column).setBackground(QColor(200,20,0))
                    self.model.item(x, work_column-16).setBackground(QColor(200,20,0))

                else:
                    self.model.item(x, work_column).setBackground(QColor(255,255,208))
                    self.model.item(x, work_column-16).setBackground(QColor(255,255,208))
                work_column+=1
            # т.к 16 колонка в календаре не используется добавляем туда прочерк
            # а значение добавляем вс ледующую строку сначала
            elif i == 15 :
                item = QStandardItem("-")
                item.setEditable(False)
                self.model.setItem(x, work_column, item)
                work_column+=1
                item = QStandardItem(str(value))
                item.setEditable(False)
                self.model.setItem(x+1, work_column-16, item)
                if value == "-":
                    self.model.item(x+1, work_column-16).setBackground(QColor(200,20,0))
                    self.model.item(x+1, work_column-32).setBackground(QColor(200,20,0))
                else:
                    self.model.item(x+1, work_column-16).setBackground(QColor(255,255,208))
                    self.model.item(x+1, work_column-32).setBackground(QColor(255,255,208))
                work_column+=1
            else:
                item = QStandardItem(str(value))
                item.setEditable(False)
                self.model.setItem(x+1, work_column-16, item)
                if value == "-":
                    self.model.item(x+1, work_column-16).setBackground(QColor(200,20,0))
                    self.model.item(x+1, work_column-32).setBackground(QColor(200,20,0))
                else:
                    self.model.item(x+1, work_column-16).setBackground(QColor(255,255,208))
                    self.model.item(x+1, work_column-32).setBackground(QColor(255,255,208))
                work_column+=1

# ДОБАВЛЯЕМ ЯЧЕЙКИ(КОРЯВО)

        x=1+1
        work_column =0
        for tabel in self.tabels:
            item = QStandardItem("")
            self.model.setItem(x, work_column, item)
            x=x+2
       
# ДОБАВЛЯЕМ ТАБЕЛЬНЫЕ

    # заполняем данные
        x=1+1
        work_column =0
        for tabel in self.tabels:
            item = QStandardItem(tabel)
            item.setEditable(False)
            
            self.model.setItem(x, work_column, item)
            self.data_table_view.setSpan(x,work_column,2,1)
            x=x+2
        
    # окрашиваем ячейки
        x=1+1
        try:
            for tabel in self.tabels:
                if x % 2 == 0:
                    self.model.item(x, work_column).setBackground(QColor(255,255,208))
                    x=x+4
        except: AttributeError 

        work_column+=1
        
        
# ДОБАВЛЯЕМ ФАМИЛИИ
        x = 1+1
        for tabel in self.tabels:
            item = QStandardItem(self.tabels[tabel]["фамилия"])
            item.setEditable(False)
            self.model.setItem(x, work_column, item)
            x=x+2
        
        x=1+1
        try:
            for tabel in self.tabels:
                if x % 2 == 0:
                    self.model.item(x, work_column).setBackground(QColor(255,255,208))
                    x=x+4
        except: AttributeError 

# ДОБАВЛЯЕМ ИНИЦИАЛЫ

        x = 2+1
        for tabel in self.tabels:
            item = QStandardItem(self.tabels[tabel]["инициалы"])
            item.setEditable(False)
            self.model.setItem(x, work_column, item)
            x=x+2
        
        x = 2+1
        try:
            for tabel in self.tabels:
                if x % 1 == 0:
                    self.model.item(x, work_column).setBackground(QColor(255,255,208))
                    x=x+4
        except: AttributeError 
        
        work_column+=1

# ДОБАВЛЯЕМ РАЗРЯДЫ

        x = 1+1
        for tabel in self.tabels:
            item = QStandardItem(str(self.tabels[tabel]["разряд"]))
            item.setEditable(False)
            self.model.setItem(x, work_column, item)
            self.data_table_view.setSpan(x,work_column,2,1)
            x=x+2
        
        x = 1+1

        try:
            for tabel in self.tabels:
                if x % 2 == 0:
                    self.model.item(x, work_column).setBackground(QColor(255,255,208))
                    x=x+4
        except: AttributeError 

        work_column+=1


# ДОБАВЛЯЕМ ГРАФИК ОТРАБОТАННЫХ СМЕН
        x = 1+1
        for tabel in self.tabels:
            for day in range(0,len(self.tabels[tabel]["отработанные смены"])):
                if day<16:
                    item = QStandardItem(str(self.tabels[tabel]["отработанные смены"][day]))
                    item.setEditable(False)
                    self.model.setItem(x, day+work_column,item )
                else:
                    item = QStandardItem(str(self.tabels[tabel]["отработанные смены"][day]))
                    item.setEditable(False)
                    self.model.setItem(x+1, day+work_column-16, item)
            x=x+2
        
        x = 1+1
        try:
            for tabel in self.tabels:
                for day in range(0,len(self.tabels[tabel]["отработанные смены"])):
                    if day<16:
                        self.model.item(x, day+work_column).setBackground(QColor(204,204,204))
                    else:
                        self.model.item(x+1, day+work_column-16).setBackground(QColor(204,204,204))
                x=x+4
        except: AttributeError
        
        work_column+=16

# ДОБАВЛЯЕМ ЯЧЕЙКИ В КОТОРЫЕ БУДЕМ ЗАНОСИТЬ ТАБЕЛЬНЫЕ ЗАМЕЩАЮЩИХ(рабочая часть с правой стороны)
        
        x = 1+1
        work_row = x
        for x in range(work_row,len(self.tabels)*2+work_row):
            for y in range(0,16):
                item = QStandardItem(None)
                # делаем их все нередактируемые и заполняем цветом
                item.setEditable(False)
                self.model.setItem(x, y+work_column, item)
        work_row = 4
        try:
            for x in range(work_row,len(self.tabels)*2+work_row,4):
                for y in range(0,16):
                    self.model.item(x, y+work_column).setBackground(QColor(204,204,204))
                    self.model.item(x+1, y+work_column).setBackground(QColor(204,204,204))
        except AttributeError:
            pass

# ЗАДАЕМ БЭКГРАУНД ЯЧЕЙКАМ С ВЫХОДНЫМИ

        self.time_calendar = self.all_data["шифр"][self.proffession_number]["Рабочий календарь"]
        work_row = 2
        work_column = 3
        for x in range(work_row,len(self.tabels)*2+work_row,2):
            work_column = 3
            for i,value in enumerate(self.time_calendar.values()):
                if i <15:
                    print(value)
                    try:
                        if value == "-":
                            print("jkj")
                            self.model.item(x, work_column+i).setBackground(QColor(200,100,100))
                            self.model.item(x, work_column+16+i).setBackground(QColor(200,100,100))
                    except: AttributeError
                elif i>=15:
                    try:
                        if value == "-":
                            print("jkj")
                            self.model.item(x+1, work_column-16+i+1).setBackground(QColor(200,100,100))
                            self.model.item(x+1, work_column+i+1).setBackground(QColor(200,100,100))
                    except: AttributeError
        
    def AddDataToSummTable(self):
        # добавляем ячейки с фамилией и нулевой суммой

        work_row = 0
        work_column = 0
        summ = float(self.all_data["шифр"][self.proffession_number]["Общая сумма"])
        hours = self.all_data["шифр"][self.proffession_number]["Часы_для_деления_по_среднему"]
        
        print(type(summ))
        print(type(hours))
        try:
            summ_per_hours = (summ/hours)
        except ZeroDivisionError:
            summ_per_hours = 0
        print(summ_per_hours)
        
        for tabel in self.tabels.keys():
            number = QStandardItem(str(tabel))
            name = QStandardItem(f'{self.tabels[tabel]["фамилия"]} {self.tabels[tabel]["инициалы"]}')
            nul = QStandardItem("           0.00")
            can_pay = (summ_per_hours*self.tabels[tabel]["Количество_часов_для_средней_суммы"])
            can_pay = QStandardItem((("{:.2f}").format(can_pay)))
            number.setEditable(False)
            name.setEditable(False)
            self.model_summ.setItem(work_row, work_column, number)
            self.model_summ.setItem(work_row, work_column+1, name)
            self.model_summ.setItem(work_row, work_column+2, nul)
            self.model_summ.setItem(work_row, work_column+3, can_pay)
            
            
            work_row+=1
        
    def AddReplaceCell_DataTable(self):
        # РАСКРАШИВАЕМ ЯЧЕЙКИ ТАБЛИЦЫ ГДЕ МОЖНО ДАТЬ ЗАМЕЩЕНИЕ

        # НАЧАЛЬНАЯ КОЛОНКа # TODO сделать чтобы она изменялась по всему документу
        work_column = 18+1
        # НАЧАЛЬНАЯ СТРОКА # TODO сделать чтобы она изменялась по всему документу
        x = 1+1
        # пробегаемся по табельным
        for tabel in self.tabels:
            # Итерируем рабочий календарь по количеству дней
            for day in range(0,len(self.all_data["шифр"][self.proffession_number]["Рабочий календарь"])+1):
                # Проверяем есть ли в день у указанного табельного замещающие(если есть, значит отмечаем в таблице этот день)
                if self.tabels[tabel]["Замещающие"].get(str(day)) !=None:
                    # если дни <16 это первая строка
                    if day<16:
                        item = QStandardItem("")
                        item.setBackground(QColor(0,128,128))
                        self.model.setItem(x, day+work_column-1,item)
                    # если дни=>16 вторая строка
                    else:
                        item = QStandardItem("")
                        item.setBackground(QColor(0,128,128))
                        self.model.setItem(x+1, day+work_column-16,item)
            x=x+2

    def input_user_color_and_save(self):
        
        
        # извлекаем из JSON год и месяц
        self.year=self.all_data["шифр"][self.proffession_number]["Информация"]["год"]
        self.month = self.all_data["шифр"][self.proffession_number]["Информация"]["месяц"]

        self.TEMP = configparser.ConfigParser()
        self.TEMP.read(self.path_with_input)
        
        # загружаем данные из файла, и если файла нет используем пустой словарь
        try:
            data_dict_from_input_user = self.TEMP["General"]['input_user']
            data_dict_from_input_user = dict(eval(data_dict_from_input_user))
            save_input_user_for_load_in_file = data_dict_from_input_user
            
            data_dict_from_summ = self.TEMP["General"]["for_summ"]
            data_dict_from_summ = dict(eval(data_dict_from_summ))
            save_input_user_for_summ_in_file = data_dict_from_summ
        except:
            self.TEMP["General"] = {}
            save_input_user_for_load_in_file = {}
            save_input_user_for_summ_in_file = {}
        
        # ПРИНИМАЕМ ОТ ПОЛЬЗОВАТЕЛЯ ВВОД И ОРАШИВАЕМ ЯЧЕЙКИ В ЗАВИСИМОСТИ ОТ ЗНАЧЕНИЯ
        row = self.data_table_view.currentIndex().row()
        column = self.data_table_view.currentIndex().column()

        # Проверяем табельный к которой относится выбранная ячейка.
        # если значение None то поднимаемся на одну строку выше(ячейки обьединенные,значение только в первом)
        if self.model.index(row,0).data() == None:

            try:
                tabel = self.model.index(row-1,0).data()
                date = self.model.index(1,column-16).data()
                user_input = self.data_table_view.currentIndex().data()
                if user_input in self.tabels[tabel]["Замещающие"][date]:
                    self.model.item(row, column).setBackground(QColor(0,128,0))

                    save_input_user_for_load_in_file[row,column] = user_input, (0,128,0)
                    # (табельный,количество часов замещаемых,день замещения,разряд) 
                    save_input_user_for_summ_in_file[self.model.index(row-1,0).data(),
                                                    self.model.index(1,column-16).data(),
                                                    self.model.index(1,column).data(),
                                                    self.model.index(row-1,2).data(),

                                                    ] =  user_input
                    

                elif user_input =="":
                    self.model.item(row, column).setBackground(QColor(0,128,128))
                    try:

                        del save_input_user_for_load_in_file[row,column] 
                        del save_input_user_for_summ_in_file[self.model.index(row-1,0).data(),
                                                            self.model.index(1,column-16).data(),
                                                            self.model.index(1,column).data(),
                                                            self.model.index(row-1,2).data(),
                                                            ]
                    except:
                        pass

                elif user_input not in self.tabels[tabel]["Замещающие"][date]:
                    self.model.item(row, column).setBackground(QColor(255,0,0))
                    save_input_user_for_load_in_file[row,column] = user_input, (255,0,0)

                    # save_input_user_for_summ_in_file[self.model.index(row-1,0).data(),
                    #                                 self.model.index(1,column-16).data()
                    #                                 ] =  user_input
                    

            except KeyError:
                print("-")
        else:
            try:
                tabel = self.model.index(row,0).data()
                date = self.model.index(0,column-16).data()
                user_input = self.data_table_view.currentIndex().data()
                if user_input in self.tabels[tabel]["Замещающие"][date]:
                    self.model.item(row, column).setBackground(QColor(0,128,0))
                    save_input_user_for_load_in_file[row,column] = user_input, (0,128,0)
                    save_input_user_for_summ_in_file[self.model.index(row,0).data(),
                                                    self.model.index(0,column-16).data(),    
                                                    self.model.index(0,column).data(),
                                                    self.model.index(row,2).data(),
                                                    ] = user_input
                    print("[INFO] - - ", user_input)
                elif user_input =="":
                    self.model.item(row, column).setBackground(QColor(0,128,128))
                    try:

                        del save_input_user_for_load_in_file[row,column] 
                        del save_input_user_for_summ_in_file[self.model.index(row,0).data(),
                                                        self.model.index(0,column-16).data(),
                                                        self.model.index(0,column).data(),
                                                        self.model.index(row,2).data(),
                                                        ]
                    except:
                        pass

                elif user_input not in self.tabels[tabel]["Замещающие"][date]:
                    self.model.item(row, column).setBackground(QColor(255,0,0))
                    save_input_user_for_load_in_file[row,column] = user_input, (255,0,0)
                    print("[INFO] - - ", user_input)
                    # save_input_user_for_summ_in_file[self.model.index(row,0).data(),
                    #                                 self.model.index(0,column-16).data()
                    #                                 ] = user_input
            except KeyError:
                print("-")
        
        self.TEMP["General"]["input_user"]= str(save_input_user_for_load_in_file)
        self.TEMP["General"]["for_summ"]  = str(save_input_user_for_summ_in_file)

        with open(f'{self.path_with_input}', "w", encoding="utf-8") as configfile:
            self.TEMP.write(configfile)

    def load_data(self):
        # try:

            self.TEMP = configparser.ConfigParser()
            self.TEMP.read(f"{self.path_with_input}")

            data_dict = self.TEMP["General"]["input_user"]
            data_dict = eval(data_dict)
            # формат словаря
            # {(строка,ячейка):(табельный,(R,G,B цвет))
            for Key, Value in data_dict.items():
                row = Key[0]
                column = Key[1]
                item = QStandardItem(Value[0])
                item.setBackground(QColor(Value[1][0],Value[1][1],Value[1][2]))
                self.model.setItem(row, column,item)
        # except:
        #     print("НЕТ ФАЙЛА")
        
    def summ_pay(self):
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("199_settings")
        TEMP_PATH = self.settings.value(f"Path_with_input_{self.proffession_number}")
        JSON_PATH = self.settings.value(f"Path_with_json_{self.proffession_number}")
        self.settings.endGroup()

        SETTINGS = configparser.ConfigParser()
        SETTINGS.read("Main\Settings_199\SETTINGS.ini", encoding="UTF-8")

        INPUT_TEMP = configparser.ConfigParser()
        INPUT_TEMP.read(TEMP_PATH, encoding="utf-8")

        # загружаем данные из джсон
        with open(f'{JSON_PATH}', "r", encoding="utf-8") as file:
            all_data = json.load(file)
        # количество рабочих часов
        hours = all_data["шифр"][self.proffession_number]["Информация"]["рабочих_часов"]
        # print(hours)

        # применям коэффициенты вредности
        if self.proffession_number == "87100":
            self.harmfulness = 0.24
            self.coefficient = int(SETTINGS[self.proffession_number]["procent_text"])/100

        elif self.proffession_number == "87200":
            self.harmfulness = 0.04
            self.coefficient = int(SETTINGS[self.proffession_number]["procent_text"])/100

        elif self.proffession_number == "08300":
            self.harmfulness = 0.08
            self.coefficient = int(SETTINGS[self.proffession_number]["procent_text"])/100

        if os.path.isfile(TEMP_PATH):
            data_dict = INPUT_TEMP["General"]["for_summ"]
            # создаем словарь табельных которые замещают
            tabels_dict = {}
            for tabel in all_data["шифр"][self.proffession_number]["Табельный"]:
                tabels_dict[tabel]=0

            data_dict = eval(data_dict)
            # print("----словарь_с_данными для суммы-----")
            
            def Summ(personal_number):
                level = all_data["шифр"][self.proffession_number]["Табельный"][personal_number]["разряд"]
                # print(level)
                if level == 3:
                    # тариф
                    tarif = int(SETTINGS[self.proffession_number]["cv_three_tarif"])
                    money_per_hours = (tarif/hours)*self.coefficient
                    money_per_hours_in_harmfullness = money_per_hours+money_per_hours*self.harmfulness
                      
                elif level == 4:
                    tarif = int(SETTINGS[self.proffession_number]["cv_four_tarif"])
                    money_per_hours = (tarif/hours)*self.coefficient
                    money_per_hours_in_harmfullness = money_per_hours+money_per_hours*self.harmfulness
                elif level == 5:
                    tarif = int(SETTINGS[self.proffession_number]["cv_five_tarif"])
                    money_per_hours = (tarif/hours)*self.coefficient
                    money_per_hours_in_harmfullness = money_per_hours+money_per_hours*self.harmfulness
                elif level == 6:
                    tarif = int(SETTINGS[self.proffession_number]["cv_six_tarif"])
                    money_per_hours = (tarif/hours)*self.coefficient
                    money_per_hours_in_harmfullness = money_per_hours+money_per_hours*self.harmfulness
                # print(float('{:.2f}'.format(money_per_hours_in_harmfullness)))
                return float('{:.2f}'.format(money_per_hours_in_harmfullness))

            # заполняем словарь(табельный:cумма)
            for value in data_dict.values():
                if value not in tabels_dict:
                    tabels_dict[value] = 0
            
            for tabel, summ in tabels_dict.items():

                for key,values in data_dict.items():
                    if values == tabel:
                        money = Summ(key[0])*int(key[2])
                        summ = tabels_dict[tabel]
                        tabels_dict[tabel]=summ+money
            print(tabels_dict)
            return(tabels_dict)
    
    def PrintSumm(self):
        
        x = self.summ_pay()
        if x == None:
            print("нет файла")
        print(x)
        
        count = 0
        for tabel in self.tabels.keys():
            for key,value in x.items():
                if int(key)==int(tabel):
                    rub = QStandardItem("{:.2f}".format(value))
                    rub.setEditable(False)
                    self.model_summ.setItem(count, 2, rub)
            count+=1
              
    def ParametersDataTable(self):
        #Задаем параметры таблицы
        # self.data_table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.data_table_view.horizontalHeader().setMinimumSectionSize(30)
        self.data_table_view.resizeColumnsToContents()

        # убираем нумерацию строк и столбцов
        self.data_table_view.verticalHeader().setVisible(False)
        self.data_table_view.horizontalHeader().setVisible(False)


        #Показывае данные при изменении в ячейке
        self.model.itemChanged.connect(self.input_user_color_and_save)
        # self.model.itemChanged.connect(self.summ_pay)
        #При изменении в левой таблице итемов, вносим сумму в правую таблицу
        self.model.itemChanged.connect(self.PrintSumm)
    
    def ParametersSummTable(self):
        #Задаем параметры таблицы
        self.summ_table_view.horizontalHeader().setMinimumSectionSize(30)
        self.summ_table_view.resizeColumnsToContents()
        
        # Считаем ширину таблицы
        vwidth = self.summ_table_view.verticalHeader().width()
        hwidth = self.summ_table_view.horizontalHeader().length()
        fwidth = self.summ_table_view.frameWidth() * 2
        scrollBarHeight = self.summ_table_view.horizontalScrollBar().height()
        self.summ_table_view.setFixedWidth(vwidth + hwidth + fwidth + scrollBarHeight)
        self.summ_table_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # убираем нумерацию строк и столбцов
        self.summ_table_view.verticalHeader().setVisible(False)
        self.summ_table_view.horizontalHeader().setVisible(False)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MAIN_WORK_TABLE("87100")
    main.show()
    sys.exit(app.exec_())
