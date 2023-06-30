import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QPushButton, \
							QHBoxLayout, QVBoxLayout,QMessageBox
from PyQt5.QtCore import Qt,QDate,QSettings
from PyQt5.QtGui import QPalette, QTextCharFormat, QIcon



class CalenderX(QCalendarWidget):
	def __init__(self):
		super(CalenderX,self).__init__()
		
		self.from_date = None
		self.to_date = None
		self.highlighter_format = QTextCharFormat()
		self.highlighter_format.setBackground(self.palette().brush(QPalette.Highlight))
		self.highlighter_format.setForeground(self.palette().color(QPalette.HighlightedText))
		self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader) # Отключаем счетчик недель
		self.clicked.connect(self.select_range)
		# self.select_date()# выбор года и месяца календаря, при запуске, в зависимости, от выбранного файла

		super().dateTextFormat()

	def highlight_range(self, format):
		if self.from_date and self.to_date:
			d1 = min(self.from_date, self.to_date)
			d2 = max(self.from_date, self.to_date)
			while d1 <= d2:
				self.setDateTextFormat(d1, format)
				d1 = d1.addDays(1)

	def select_range(self, date_value):
		self.highlight_range(QTextCharFormat())
		if QApplication.instance().keyboardModifiers() & Qt.ShiftModifier and self.from_date:
			self.to_date = date_value
			self.highlight_range(self.highlighter_format)
		else:
			self.from_date = date_value	
			self.to_date = None
	def select_date(self):
			self.settings = QSettings("NITIC")
			self.settings.beginGroup("Talons_program")
			self.data_month = int(self.settings.value("current_month"))
			self.data_year = int(self.settings.value("current_year"))
			date = QDate(self.data_year,self.data_month, 1)
			self.setSelectedDate(date)
		
class MyApp(QWidget):
	def __init__(self):
		super(MyApp,self).__init__()
		self.window_width, self.window_height = 400, 300
		self.setMinimumSize(self.window_width, self.window_height)
		self.setWindowTitle('Календарь')
		# self.setWindowIcon(QIcon('Calendar.ico'))
		self.setStyleSheet('''
			QWidget {
				font-size: 15px;
			}
		''')	
		self.layout = QHBoxLayout()
		self.calendar = CalenderX()
		self.layout.addWidget(self.calendar)
		self.setLayout(self.layout)
		

	def print_days_selected(self):
		"""Функция которая возвращает список дат для выбора периода, в которых хотим дать талоны"""
		self.period = []#список дат, от какого тадоны получаем, до какого талоны получаем

		if self.calendar.from_date and self.calendar.to_date:
			start_date = min(self.calendar.from_date.toPyDate(), self.calendar.to_date.toPyDate())
			end_date = max(self.calendar.from_date.toPyDate(), self.calendar.to_date.toPyDate())
			if int(str(start_date)[8:10]) > int(str(end_date)[8:10]):
				QMessageBox.warning(
                self, 'Ошибка', 'ОШИБКА: Выберите даты в пределах одного месяца')
			else:
				self.period = [str(start_date),str(end_date)]
				print(self.period)
		elif self.calendar.from_date:
			start_date = self.calendar.from_date.toPyDate()
			self.period = [str(start_date)]
			print(self.period)
		else:
			QMessageBox.warning(
                self, 'Ошибка', 'ОШИБКА: Не выбран ни один день')
		
		return self.period 
if __name__ == '__main__':
	app = QApplication(sys.argv)
	myApp = MyApp()
	myApp.show()
	try:
		sys.exit(app.exec_())
	except SystemExit:
		print('Closing Window...')
