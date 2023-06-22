import os
import sys
import json
from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QColor
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableView,QApplication,QPushButton,QGridLayout,QMainWindow,QVBoxLayout,QHeaderView,QMessageBox, QFrame

import configparser

class ADD_INPUT_TABLE(QWidget):
    def __init__(self,model,table,button,layout,main_layout,count,height,width):
        super(ADD_INPUT_TABLE,self).__init__()
        # счет виджетов
        self.count = count
        self.model = model
        self.table = table
        self.dellete_button = button
        self.layout = layout
        self.main_layout = main_layout
        self.vheight = height
        self.fwidth = width
        self.initUI()
        

    def initUI(self):
        # таблица в которую будем добавлять новых людей в список полученя талонов
        self.table.setModel(self.model)
        # задаем расположение таблиц с вводом персональных данных
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.dellete_button)
        #задаем расположение таблицы
        self.main_layout.addLayout(self.layout,self.count,1)
        #добавляем настройки кнопки удаления
        self.dellete_button_settings()
    
    def dellete_button_settings(self):
        self.dellete_button.setFixedHeight(self.vheight+self.fwidth)
        self.dellete_button.clicked.connect(self.dellete_button_action)   
        
    def dellete_button_action(self):
        
        # self.main_layout.removeWidget(self.table)
        # self.table.deleteLater()
        self.table.hide()
        self.dellete_button.setText("Удалено")
        self.dellete_button.setEnabled(False)
        # self.layout.removeWidget(self.dellete_button)
        # self.dellete_button.deleteLater()
       
class MAIN_WORK_TABLE(QWidget): 
    def __init__(self):
        super(MAIN_WORK_TABLE, self).__init__()
        self.count=1
        self.count_table = 0
        self.initUI()
    
    def initUI(self):

        self.setWindowTitle("Добавить персонажа в список талонов")
        # self.resize(500,300)
        #таблица в которой будут отображены заголовки
        self.model_heading_table = QStandardItemModel()
        self.heading_table = QTableView()
        self.heading_table.setModel(self.model_heading_table)

        # задаем расположение таблицы с заголовками
        self.layout_heading_table = QHBoxLayout()
        self.layout_heading_table.addWidget(self.heading_table)
        # кнопка которая позволит добавит нового человека
        self.button = QPushButton("Добавить")
        self.layout_heading_table.addWidget(self.button)

        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.layout_heading_table,0,1)
    
        self.setLayout(self.main_layout)
        self.all_function()

    def all_function(self):
        self.add_data_from_json()
        self.add_data_to_heading_table()
        self.settings_heading_table()
        self.add_button_settings()
    
    def add_data_from_json(self):
        """функция которая определяет расположения файла JSON для 199"""
        settings = configparser.ConfigParser()
        settings.read("data/SETTINGS.ini", encoding="utf-8")
        path = settings["Settings"][f'current_directory_87100']
        if path == "": 
            print('Нет файла')
            # TODO: Запускаем функцияю из программы 199, которая создает основной JSON файл
            pass
        elif not os.path.isfile(f'{path}'):
            print('файла по указанному пути не существует')
            # TODO: Запускаем функцияю из программы 199, которая создает основной JSON файл
        else:
            with open(f"{path}", "r", encoding="utf-8") as file:
                all_data = json.load(file)

        self.all_data = all_data
        
    def add_data_to_heading_table(self):
        work_calendar = self.all_data['шифр']['87100']["Рабочий календарь"]
        
        item = QStandardItem("Таб.")
        item.setEditable(False)
        self.model_heading_table.setItem(0, 0, item)
        self.heading_table.setSpan(0,0,2,1)

        item = item = QStandardItem("Фамилия И.О")
        item.setEditable(False)
        self.model_heading_table.setItem(0, 1, item)
        self.heading_table.setSpan(0,1,2,1)

        item = QStandardItem("Профессия,\nдолжность")
        item.setEditable(False)
        self.model_heading_table.setItem(0, 2, item)
        self.heading_table.setSpan(0,2,2,1)

        count = 3
        for i,day in enumerate(work_calendar.items(),1):
            if i <= 15:
                item = QStandardItem(day[0])
                item.setEditable(False)
                if day[1]=="-":
                    item.setBackground(QColor(200,100,100))

                self.model_heading_table.setItem(0, count, item)
                count+=1
            if i == 15:
                item = QStandardItem("-")
                item.setEditable(False)
                self.model_heading_table.setItem(0, count, item)
                count = 3
            if i >15:
                item = QStandardItem(day[0])
                item.setEditable(False)
                if day[1]=="-":
                    item.setBackground(QColor(200,100,100))
                self.model_heading_table.setItem(1, count, item)
                count+=1
                
    def settings_heading_table(self):
        # убираем нумерацию строк и столбцов
        self.heading_table.verticalHeader().setVisible(False)
        self.heading_table.horizontalHeader().setVisible(False)
        # self.heading_table.horizontalHeader().setMinimumSectionSize(30)
        self.heading_table.resizeColumnsToContents()

        # подгоняем таблицу по длине
        vwidth = self.heading_table.verticalHeader().width()
        hwidth = self.heading_table.horizontalHeader().length()
        scrollBarHeight = self.heading_table.horizontalScrollBar().width()
        self.heading_table.setFixedWidth(vwidth + hwidth - 14)
        self.heading_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # подгоняем таблицу по высоте
        vheight = self.heading_table.verticalHeader().length()
        fwidth = self.heading_table.frameWidth() 
        self.heading_table.setFixedHeight(vheight+fwidth)
        self.heading_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.vheight = vheight
        self.fwidth = fwidth
    
    def add_button_settings(self):
        self.button.setFixedHeight(self.vheight+self.fwidth*2)
        self.button.clicked.connect(self.add_button_action)

    def add_button_action(self):
        
        if self.count != 6:
            if self.count_table == 0:
                self.ferst_table()
                self.count+=1
                self.count_table+=1

            elif self.count_table == 1:
                self.second_table()
                self.count+=1
                self.count_table+=1

            elif self.count_table == 2:
                self.firth_table()
                self.count+=1
                self.count_table+=1

            elif self.count_table == 3:
                self.fouth_table()
                self.count+=1
                self.count_table+=1

            elif self.count_table == 4:
                self.fifthy_table()
                self.count+=1
                self.count_table+=1    
            
    def ferst_table(self):
        count = self.count
        height = self.vheight
        width = self.fwidth
        model_1 = QStandardItemModel()
        table_1 = QTableView()
        button_1 = QPushButton("Удалить")
        layout_1 = QHBoxLayout()
        main_layout = self.main_layout

        AIT = ADD_INPUT_TABLE(model = model_1,
                                   table=table_1,
                                   button=button_1,
                                   layout=layout_1,
                                   main_layout=main_layout,
                                   count=count,
                                   height=height,
                                   width=width)
    
    def second_table(self):
        count = self.count
        height = self.vheight
        width = self.fwidth
        self.model_2 = QStandardItemModel()
        self.table_2 = QTableView()
        self.button_2 = QPushButton("Удалить")
        layout_2 = QHBoxLayout()
        main_layout = self.main_layout

        self.AIT = ADD_INPUT_TABLE(model = self.model_2,
                                   table=self.table_2,
                                   button=self.button_2,
                                   layout=layout_2,
                                   main_layout=main_layout,
                                   count=count,
                                   height=height,
                                   width=width)
    
    def firth_table(self):
        count = self.count
        height = self.vheight
        width = self.fwidth
        model_3 = QStandardItemModel()
        table_3 = QTableView()
        button_3 = QPushButton("Удалить")
        layout_3 = QHBoxLayout()
        main_layout = self.main_layout

        self.AIT = ADD_INPUT_TABLE(model = model_3,
                                   table=table_3,
                                   button=button_3,
                                   layout=layout_3,
                                   main_layout=main_layout,
                                   count=count,
                                   height=height,
                                   width=width)

    def fouth_table(self):
        count = self.count
        height = self.vheight
        width = self.fwidth
        model_4 = QStandardItemModel()
        table_4 = QTableView()
        button_4 = QPushButton("Удалить")
        layout_4 = QHBoxLayout()
        main_layout = self.main_layout

        self.AIT = ADD_INPUT_TABLE(model = model_4,
                                   table=table_4,
                                   button=button_4,
                                   layout=layout_4,
                                   main_layout=main_layout,
                                   count=count,
                                   height=height,
                                   width=width)

    def fifthy_table(self):
        count = self.count
        height = self.vheight
        width = self.fwidth
        model_5 = QStandardItemModel()
        table_5 = QTableView()
        button_5 = QPushButton("Удалить")
        layout_5 = QHBoxLayout()
        main_layout = self.main_layout

        self.AIT = ADD_INPUT_TABLE(model = model_5,
                                   table=table_5,
                                   button=button_5,
                                   layout=layout_5,
                                   main_layout=main_layout,
                                   count=count,
                                   height=height,
                                   width=width)


        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MAIN_WORK_TABLE()
    main.show()
    sys.exit(app.exec_())
