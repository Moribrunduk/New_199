import sys
from PyQt5 import Qt 
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QGridLayout, QLabel,QLineEdit,QPushButton,QWidget, QApplication, QMessageBox,QShortcut,QCheckBox, QGroupBox
from PyQt5.QtCore import QSettings,QCoreApplication



def function_after_avtorization():
    print('авторизовался')


class AVTORIZATION_WINDOW(QWidget):
    def __init__(self,function):
        super(AVTORIZATION_WINDOW,self).__init__()
        self.function = function
        self.initUI()
        self.Main()
    
        
    def initUI(self):
        
        self.layout = QGridLayout()
        self.setWindowTitle("Авторизация")
        self.label_name = QLabel("Имя")
        self.label_password = QLabel("Пароль")
        self.text_name = QLineEdit()
        self.text_name.setFixedHeight(20)
        self.text_password = QLineEdit()
        self.text_password.setFixedHeight(20)
        self.text_password.setEchoMode(QLineEdit.Password)
        
        self.button_ok = QPushButton("ОК")
        self.button_ok.setFixedHeight(20)
        self.button_ok.clicked.connect(self.Verification)

        self.button_exit = QPushButton("Выход")
        self.button_exit.setFixedHeight(20)
        self.button_exit.clicked.connect(self.ExitProgramm)

        self.button_new_user = QPushButton("Новый пользователь")
        self.button_new_user.setFixedHeight(20)
        self.button_new_user.clicked.connect(self.NewUser)

        self.layout.addWidget(self.label_name,0,0,1,4)
        self.layout.addWidget(self.label_password,1,0,1,4)

        self.layout.addWidget(self.text_name,0,1,1,4)
        self.layout.addWidget(self.text_password,1,1,1,4)

        self.layout.addWidget(self.button_ok,2,3,1,1)
        self.layout.addWidget(self.button_exit,2,4,1,1)
        self.layout.addWidget(self.button_new_user,3,0,1,5)

        self.setFixedSize(320,130)
        self.setLayout(self.layout)

    def Main(self):
        self.Qset()
        self.HotkeyKeybord()
        self.show()
    
    def Qset(self):
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("GOD_parameters")
        self.settings.setValue("Password", "19921128Qe")
        self.settings.beginGroup("Users_passwords")
    
    def HotkeyKeybord(self):
        self.text_password.returnPressed.connect(self.button_ok.click)
    
    def Verification(self):
       
        
        user_name = self.text_name.text()
        password = self.text_password.text()

        control_name = self.settings.value(f"{user_name}")
        print(control_name)

        if control_name == None:
            QMessageBox.warning(
                self, 'Ошибка', 'Ошибка: такого пользователя не существует')
        elif control_name != password:
            QMessageBox.warning(
                self, 'Ошибка', 'Ошибка: неверный пароль')
        else:
            self.success_avtorization_function = self.function
            self.success_avtorization_function()
            self.close()

    def ExitProgramm(self):
        sys.exit()

    def NewUser(self):
        self.hide()
        self.CNU = CREATE_NEW_USER()
        
    
class CREATE_NEW_USER(QWidget):
    
    def __init__(self):
        super(CREATE_NEW_USER,self).__init__()
        self.initUI()
        self.Main()
    
    def initUI(self):

        self.layout = QGridLayout()
        self.setWindowTitle("Новый пользователь")
        self.label_name = QLabel("Имя")
        self.label_password = QLabel("Пароль")
        self.text_name = QLineEdit()
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.Password)
        self.text_control_password = QLineEdit()
        self.text_control_password.setEchoMode(QLineEdit.Password)
        
        self.button_ok = QPushButton("ОК")
        self.button_ok.setFixedHeight(20)
        self.button_ok.clicked.connect(self.SaveUserInputLoadAvtorization)


        self.button_exit = QPushButton("Выход")
        self.button_exit.setFixedHeight(20)
        self.button_exit.clicked.connect(self.ExitProgramm)

        self.layout.addWidget(self.label_name,0,0,1,4)
        self.layout.addWidget(self.label_password,1,0,1,4)

        self.layout.addWidget(self.text_name,0,1,1,4)
        self.layout.addWidget(self.text_password,1,1,1,4)
        self.layout.addWidget(self.text_control_password,2,1,1,4)
        
        self.layout.addWidget(self.button_ok,3,3,1,1)
        self.layout.addWidget(self.button_exit,3,4,1,1)

       

        self.setFixedSize(300,150)
        self.setLayout(self.layout)

    def Main(self):
        self.Qset()
        self.HotkeyKeybord()
        self.show()

    def Qset(self):
        self.settings = QSettings("NITIC")

    def HotkeyKeybord(self):
        self.shortcut = QShortcut(QKeySequence("Ctrl+g"), self)
        self.shortcut.activated.connect(self.ShowGodVerification)
    
    def ShowGodVerification(self):
        self.god_label_password = QLabel("Пароль  ")
        self.god_text_password = QLineEdit()
        self.god_text_password.setEchoMode(QLineEdit.Password)
        self.god_text_password.setFixedHeight(20)

        self.layout.addWidget(self.god_label_password,4,0,1,4)
        self.layout.addWidget(self.god_text_password,4,1,1,4)
        
        self.god_ok_button = QPushButton("Верифицировать")
        self.god_ok_button.clicked.connect(self.ControlPassword)
        self.layout.addWidget(self.god_ok_button,5,0,1,5)

        self.Group_box_loyout = QGroupBox()
        self.layout_in_group_box = QGridLayout()
        self.Chech42 = QCheckBox("Ц 42")
        self.ChechKSP = QCheckBox("КСП")
        self.ChechSSP_1 = QCheckBox("ССП-Э1")
        self.ChechSSP_2 = QCheckBox("ССП-Э2")
        self.Chech_woman_print = QCheckBox("Женские ведомости")
        self.Talons = QCheckBox("Печать талонов")

        self.layout_in_group_box.addWidget(self.Chech42,1,0)
        self.layout_in_group_box.addWidget(self.ChechKSP,1,1)
        self.layout_in_group_box.addWidget(self.ChechSSP_1,2,0)
        self.layout_in_group_box.addWidget(self.ChechSSP_2,2,1)
        self.layout_in_group_box.addWidget(self.Chech_woman_print,3,0)
        self.layout_in_group_box.addWidget(self.Talons,3,1)

        self.Group_box_loyout.setLayout(self.layout_in_group_box)
        self.layout.addWidget(self.Group_box_loyout,6,0,1,5)
        

        self.setFixedSize(300,260)
    
   
    def print_1(self):
        print("включен")

    def ControlPassword(self):

        self.settings.beginGroup("GOD_parameters")
        god_password_input = self.god_text_password.text()
        print(god_password_input)
        print(self.settings.value("Password"))
        if god_password_input == self.settings.value("Password"):
            self.god_ok_button.setText("Верифицировано")
            self.god_ok_button.setEnabled(False)
            
        else:
            print("Неверифицирован")
        self.settings.endGroup()
        
            
    def SaveUserInputLoadAvtorization(self):
        # ОПЕРАЦИИ С ЛОГИНОМ
        user_name = self.text_name.text()
        self.settings.beginGroup("GOD_parameters")
        self.settings.beginGroup("Users_passwords")
        
        # Проверяем есть ли в реестре такой пользователь
        control_name = self.settings.value(f"{user_name}")
        self.settings.endGroup()
        self.settings.endGroup()
        
        if user_name =="":
            QMessageBox.warning(
                self, 'Ошибка', 'Ошибка: введите имя пользователя')
        elif control_name != None:
            QMessageBox.warning(
                self, 'Ошибка', 'Пользователь с таким именем уже существует')
        else:
            # Проверяем введенные пароли
            password = self.text_password.text()
            control_password = self.text_control_password.text()
            if password != control_password:
                QMessageBox.warning(
                self, 'Ошибка', 'Пароли не совпадают')
            else:
                try:
                    if self.god_ok_button.text() == "Верифицировано":
                        self.settings.beginGroup("GOD_parameters")
                        self.settings.beginGroup("Users_passwords")
                        self.settings.setValue(user_name,password)
                        self.settings.endGroup()
                        self.settings.beginGroup("Users_access")

                        self.access_list = []
                        if self.Chech42.isChecked():
                            self.access_list.append("ц.42")
                        if self.ChechKSP.isChecked():
                            self.access_list.append("КСП")
                        if self.ChechSSP_1.isChecked():
                            self.access_list.append("ССП Э1")
                        if self.ChechSSP_2.isChecked():
                            self.access_list.append("ССП Э2")
                        if self.Chech_woman_print.isChecked():
                            self.access_list.append("Woman")
                        if self.Talons.isChecked():
                            self.access_list.append("Talons")

                            
                        self.settings.setValue(user_name,self.access_list)
                        print(self.settings.value(user_name))
                        self.close()
                        self.AW = AVTORIZATION_WINDOW()
                    else:
                        QMessageBox.warning(
                self, 'Ошибка', 'Ошибка: требуется верификация')
                except AttributeError:
                    QMessageBox.warning(
                self, 'Ошибка', 'Ошибка: требуется верификация')

        self.settings.endGroup()


    def ExitProgramm(self):
            sys.exit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    QCoreApplication.setApplicationName("NITIC")
    QCoreApplication.setApplicationName("GOD_PROGRAMM")
    AW = AVTORIZATION_WINDOW(function_after_avtorization)
    # CNU = CREATE_NEW_USER()
    sys.exit(app.exec_())
