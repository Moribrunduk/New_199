import sys
import os
sys.path.insert(1,"Bin")
from PyQt5.QtWidgets import QWidget, QApplication,QPushButton,QHBoxLayout,QFileDialog,QVBoxLayout,QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt,QSettings
import xlrd

from Create_json_file import CREATE_JSON_DATA
from Create_empty_init_file import CREATE_EMPTY_INPUT_FILE

class Change_profession(QWidget):
    def __init__(self,profession_number):
        super(Change_profession,self).__init__()
        self.profession_number = str(profession_number)
        self.initUI()
        
    def initUI(self):

        self.setWindowTitle("Выбор Файла")
        self.setFixedSize(450,150)
        self.main_layout = QHBoxLayout()
        self.main_button = QPushButton(self.ButtonText())
        self.main_button.clicked.connect(self.get_file_directory)
        self.main_button.setStyleSheet("font: 14pt")
        self.main_button.setFixedSize(250,130)
        

        self.right_layout = QVBoxLayout()
        self.file_label = QLineEdit("Выберите файл")
        self.file_label.setReadOnly(True)
        self.file_label.setStyleSheet("font: 10pt")
        self.file_label.setAlignment(Qt.AlignCenter)

        self.right_layout_for_button = QHBoxLayout()
        self.OK_button = QPushButton("OK", clicked=self.Ok_batton_action)
    

        self.change_button = QPushButton("Изменить")
        self.change_button.clicked.connect(self.get_file_directory)

        self.right_layout_for_button.addWidget(self.OK_button)
        self.right_layout_for_button.addWidget(self.change_button)

        self.right_layout.addWidget(self.file_label)
        self.right_layout.addLayout(self.right_layout_for_button)

        self.main_layout.addWidget(self.main_button)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)
    
    def ButtonText(self):
        # текст который будет выводится на кнопке выбора файла в зависимости от професии
        if self.profession_number == "87100":
            text = f"Выберите файл для \n дефектоскопистов РГГ \n ({self.profession_number})"
        elif self.profession_number == "87200":
            text = f"Выберите файл для \n дефектоскопистов ПЗРС \n ({self.profession_number})"
        elif self.profession_number == "08300":
            text = f"Выберите файл для \n фотолаборантов \n ({self.profession_number})"
        else:
            text = f"Выберите файл для \n киборгов убийц \n ({self.profession_number})"
        return text


    def get_file_directory(self):
        # функция которая записывает в файл путь к последнему выбранному файлу
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("199_settings")
        self.filepath, filetype = QFileDialog.getOpenFileName(self,
                            "Выбрать файл",
                            ".",
                            "Text Files(*.xls)")
        self.settings.setValue(f'Path_{self.profession_number}',self.filepath)
        if self.filepath: 
            work_book = xlrd.open_workbook(self.filepath)
            work_sheet = work_book.sheet_by_name("Табель")
            self.data_year = work_sheet.cell(1,0).value.replace(" ",'')
            print(self.data_year)
            self.data_month = work_sheet.cell(1,2).value
            print(self.data_month)
            self.data_place = work_sheet.cell(0,17).value
            print(self.data_place.replace(" ","_"))
            self.file_label.setText(f"{self.data_month} {self.data_year}")
        else:
            pass
        # файл куда сохраняюся все, что ввел пользователь
    
    def Ok_batton_action(self):
        if self.filepath:

            self.settings.setValue(f'Path_with_input_{self.profession_number}',f"Premia_199\\data\\{self.data_place}\\{self.data_year}\\{self.data_month}\\{self.profession_number}_input.ini")
            if not os.path.exists(f"Premia_199\\data\\{self.data_place}\\{self.data_year}\\{self.data_month}"):
                os.makedirs(f"Premia_199\\data\\{self.data_place}\\{self.data_year}\\{self.data_month}")
            self.CREATE_INPUT_FILE = CREATE_EMPTY_INPUT_FILE(path = f"Premia_199\\data\\{self.data_place}\\{self.data_year}\\{self.data_month}",
                                                                    profession_number=self.profession_number)
            self.CREATE_INPUT_FILE.main()
            self.CREATE_JSON_FILE = CREATE_JSON_DATA(self.profession_number)
            self.CREATE_JSON_FILE.main()
        
        else:
            pass
    
    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    CP = Change_profession("87200")
    CP.showMaximized()
    sys.exit(app.exec_())