import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QMessageBox,QMainWindow

sys.path.insert(0,"Talons\Bin")
from Calendar import MyApp
from Calendar_interface import Interface
from Print_to_xlsx import PRINT_TO_XLS



 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.widget = QWidget()

        self.main_layout = QHBoxLayout()
        self.calendar_widget = MyApp()
        self.calenar_interface_widget = Interface()
        
        self.main_layout.addWidget(self.calendar_widget)
        self.main_layout.addWidget(self.calenar_interface_widget)
        self.calenar_interface_widget.button_print.clicked.connect(self.button)

        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)
        self.setFixedSize(620,420)
        self.show()
        
    def button(self):
        if self.calenar_interface_widget.brigadir_input.text() == "Введите Фамилию И.О.":
            QMessageBox.warning(
                self, 'Ошибка', 'Введите Фамилию И.О. бригадира')
        elif self.calenar_interface_widget.tabel_label.text() == "Табель не подключен":
            QMessageBox.warning(
                self, 'Ошибка', 'Подключите табель')
        else:
            period_list = self.calendar_widget.print_days_selected()
            try: 
                if len(period_list) == 1:
                    self.start_date = self.final_date = int(period_list[0][8:10])
                    self.month = int(period_list[0][5:7])
                    self.year = int(period_list[0][0:4])
                    self.print = PRINT_TO_XLS(start_data=self.start_date,
                                                final_data=self.final_date,
                                                brigadir=self.calenar_interface_widget.brigadir_input.text(),
                                                month=self.month,
                                                year=self.year).main()
                elif len(period_list) == 2:
                    self.month = int(period_list[0][5:7])
                    self.year = int(period_list[0][0:4])
                    self.start_date = int(period_list[0][8:10])
                    self.final_date = int(period_list[1][8:10])
                    self.month = int(period_list[0][5:7])
                    self.year = int(period_list[0][0:4])
                    self.print = PRINT_TO_XLS(start_data=self.start_date,
                                                final_data=self.final_date,
                                                brigadir=self.calenar_interface_widget.brigadir_input.text(),
                                                month=self.month,
                                                year=self.year).main()
            except AttributeError:
                print("ощибка")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
