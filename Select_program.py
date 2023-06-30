import sys
import xlrd
import xlwt
import json
import openpyxl
from win32com.client import Dispatch

sys.path.append("Talons")
sys.path.append("Premia_199")

from PyQt5 import Qt 
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QGridLayout, QLabel,QLineEdit,QPushButton,QWidget, QApplication, QMessageBox,QShortcut,QCheckBox, QGroupBox
from PyQt5.QtCore import QSettings,QCoreApplication


from PyQt5.QtGui import QFont,QPixmap
from PyQt5.QtWidgets import QVBoxLayout,QLabel,QPushButton,QWidget, QApplication,QMainWindow
from PyQt5.QtCore import QTimer, Qt







class MAIN_WINDOW(QWidget):
    def __init__(self):
        super().__init__()
        self.show_picture()
        

    def show_picture(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.8)
        self.label = QLabel(self)
        pixmap = QPixmap('Premia_199\Bin\\1.jpg')
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())  # fit window to the image
        self.version_number = QLabel("VERSION:0.1.2",self)
        self.version_number.setStyleSheet("font: 15pt arial;"
                                           " color: Orange;")
        self.timer_close = QTimer()

        self.timer_close.timeout.connect(self.close)
        self.timer_close.timeout.connect(self.show_choose_window)
        self.timer_close.start(3000)
        self.show()
    
    def show_choose_window(self):
        self.timer_close.stop()
        self.CW = CHOOSE_WINDOW()
        self.CW.InitUI()
        self.close()

class CHOOSE_WINDOW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()
    
    def InitUI(self):
        self.widget = QWidget()
        self.Main_layout = QVBoxLayout()
        self.setWindowTitle("Выбор программы")
        
        self.Button_sellect_199 = QPushButton("Премия шифр №199")
        self.Button_sellect_199.setFont((QFont('Timez New Roman', 15)))
        self.Button_sellect_199.setFixedSize(280,100)
        self.Button_sellect_199.clicked.connect(self.Button_199_action)

        self.Button_sellect_Talons = QPushButton("Талоны")
        self.Button_sellect_Talons .setFont((QFont('Timez New Roman', 15)))
        self.Button_sellect_Talons.setFixedSize(280,100)
        self.Button_sellect_Talons.clicked.connect(self.Button_Talons_action)
        self.Main_layout.addWidget(self.Button_sellect_199)
        self.Main_layout.addWidget(self.Button_sellect_Talons)

        self.widget.setLayout(self.Main_layout)
        self.setCentralWidget(self.widget)

        self.setFixedSize(300,220)
        self.show()
    
    def Button_Talons_action(self):

        sys.path.insert(0,"Talons")
        from Bin import Main_2
        
        self.close()
        self.MW = Main_2.MainWindow()
        self.MW.initUI()
    
    def Button_199_action(self):
        sys.path.insert(1,"Premia_199")
        from Bin import Content

        self.close()
        self.CONT = Content.MAIN_WINDOW()
       




if __name__ == "__main__":
    app = QApplication(sys.argv)
    MW = MAIN_WINDOW()
    sys.exit(app.exec_())
    
