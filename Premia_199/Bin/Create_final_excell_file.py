import json
import os
import xlwt
import configparser
import math
from create_form import create_file
from create_form import set_style
from Create_file_with_user_input_in_table import CREATE_FILE
from PyQt5.QtCore import QSettings

class CREATE_EXCELL():
    def __init__(self, proffession_number):
        self.proffession_number = str(proffession_number)
        super(CREATE_EXCELL, self).__init__()
        self.Main()

    def Main(self):
        self.CF = CREATE_FILE(self.proffession_number)
        self.CF.Main()
        self.LoadAllInformation()
        self.write_to_file_string()

    def LoadAllInformation(self):

        self.SETINGS  = configparser.ConfigParser()
        self.SETINGS.read('Main\Settings_199\SETTINGS.ini', encoding="utf-8")
    
        self.SETINGS_tarif = {self.proffession_number:
                                {
                                    3:self.SETINGS[self.proffession_number]["cv_three_tarif"],
                                    4:self.SETINGS[self.proffession_number]["cv_four_tarif"],
                                    5:self.SETINGS[self.proffession_number]["cv_five_tarif"],
                                    6:self.SETINGS[self.proffession_number]["cv_six_tarif"]}}

        self.SETINGS_procent = {self.proffession_number : self.SETINGS[self.proffession_number]["procent_text"] }

        self.settings = QSettings("NITIC")
        self.settings.beginGroup("199_settings")
        self.path_with_json = self.settings.value(f"Path_with_json_{self.proffession_number}")
        self.path_for_excell = self.settings.value(f"Path_for_excell_{self.proffession_number}")
        self.settings.endGroup()
        self.SETINGS_current_place = self.path_with_json.partition("\\")[-1].partition("\\")[-1].split("\\")[0]
        self.SETINGS_current_data = self.path_with_json.partition("\\")[-1].partition("\\")[-1].partition("\\")[-1]
        self.SETINGS_current_month = self.SETINGS_current_data.split("\\")[1]
        self.SETINGS_current_year = self.SETINGS_current_data.split("\\")[0]
     
        Year = {"01":"январь",
                "02":"февраль",
                "03":"март",
                "04":"апрель",
                "05":"май",
                "06":"июнь",
                "07":"июль",
                "08":"август",
                "09":"сентябрь",
                "10":"октябрь",
                "11":"ноябрь",
                "12":"декабрь"}
        for key,vallue in Year.items():
            try:
                if vallue == self.SETINGS_current_month:
                    self.month = key
            except Exception as ex:
                print(ex)
                self.month = "00"
        self.year = self.SETINGS_current_year[2:4]

        with open(self.path_with_json, "r", encoding="utf-8") as file:
                self.all_data = json.load(file)

        self.substitutes = configparser.ConfigParser()
        self.substitutes.read(f"{self.path_for_excell}",encoding='utf-8')


    def LoadDataAndCreateList(self):

        """
        функция которая загружает данные из файла datalist of subtitutes.ini
        (Замещаемый, причина отсутствия, дата начала отсутствия, замещающий)
        и приводит в список (("Воронов Е.М., табельный 479",
                            "Дефектоскопист РГГ",
                            "Отпуск",
                            "7.11-31.11.2020",
                            "тариф(10988)",
                            "Илюхин Ю.В., табельный 473",
                            "Дефектоскопист РГГ")

        """

        self.tabels = self.all_data["шифр"][str(self.proffession_number)]["Табельный"]

        # задаем название професии
        profession_name = ""
        if str(self.proffession_number) == "87100":
            profession_name = "Дефектоскопист РГГ"
        elif str(self.proffession_number) == "87200":
            profession_name = "Дефектоскопист ПЗРС"
        elif str(self.proffession_number) == "08300":
            profession_name = "Фотолаборант"
        else:
            profession_name = "Неизвестный код"

        def PrintName(tabel):
            information = self.all_data["шифр"][str(self.proffession_number)]["Табельный"]
            name = F'{information[tabel]["фамилия"]} {information[tabel]["инициалы"]}'
            return name
        
        def PrintReason(reason):

            if reason == "ИО":
                print_reason = "И.о. мастера"
            elif reason == "О":
                print_reason = "Отпуск очередной"
            elif reason == "Э":
                print_reason = "Отпуск учебный"
            elif reason == "Р":
                print_reason = "Отпуск по беремености"
            elif reason == "А":
                print_reason = "Отпуск за свой счет"
            elif reason == "Ж":
                print_reason = "Пенсионный/уход за детьми"
            elif reason == "Д":
                print_reason = "Донорский день"
            elif reason == "М":
                print_reason = "Медкомиссия"
            elif reason == "Б":
                print_reason = "Больничный"
            elif reason == "К":
                print_reason = "Командировка"
            else:
                print_reason ="неизвестная причина"

            return print_reason
        
        def PrintPeriod(start_day, final_day):

            if int(start_day) != int(final_day):
                period = f"{int(start_day):02.0f}.{int(self.month):02.0f}-{int(final_day):02.0f}.{int(self.month):02.0f}.{int(self.year)}"
                
            elif int(start_day) == int(final_day):
                period = f"{int(final_day):02.0f}.{int(self.month):02.0f}.{int(self.year)}"
            
            else:
                period = f"Неизвестный период"
            
            return period
        
        def PrintCvalification(tabel): 
            cvalification = self.all_data["шифр"][str(self.proffession_number)]["Табельный"][tabel]["разряд"]
            return cvalification
        
        def CreateListForWriteXls():
            list_for_write_xls = []

            for personal_number in self.tabels:
                substitutes_list = eval(self.substitutes["DEFAULT"][f"{self.proffession_number},{personal_number}"])

                for item in substitutes_list:
                    list_for_write_xls.append((
                        (f"{PrintName(item[0])} таб. {item[0]}"),
                        (f"{profession_name},{PrintCvalification(item[0])} разряд"),
                        (f"{PrintReason(item[1])}"),
                        (f"{PrintPeriod(item[2],item[3])}"),
                        (f"{PrintName(str(item[4]))}, таб {item[4]}"),
                        (f"{profession_name},{PrintCvalification(str(item[4]))} разряд"),
                        (f"{self.SETINGS_tarif[str(self.proffession_number)][PrintCvalification(item[0])]} ")
                                        ))

            return list_for_write_xls

        return CreateListForWriteXls()


    def write_to_file_string(self):
        workbook =xlwt.Workbook()
        # Получать рабочий лист
        worksheet = workbook.add_sheet('form')
        # считаем количество строк которые требуется создать
        number_of_rows = len(self.LoadDataAndCreateList())
        # считаем количество строк которые нужно создать в документе
        # количество строк в замещении делим на 15(количество позиций возможные в документе)
        # округляем до большего
        count = math.ceil(number_of_rows/11)*40
        create_file(worksheet=worksheet,count=count,month = self.SETINGS_current_month, year = self.SETINGS_current_year)
        
        # передаем информацию для записи
        list_for_write = self.LoadDataAndCreateList()
        
        def write_row(start_row,start_column,count,value):
            #sheet.merge(top_row, bottom_row, left_column, right_column)

            # записываем порядковый номер:
            worksheet.merge(start_row,start_row+1,start_column,start_column, set_style(bordleft=2, bordright=2,bordtop=2,bordbottom=2))
            worksheet.write(start_row, start_column,str(count), set_style(ahorz=0x02,bordleft=2, bordright=2,bordtop=2,bordbottom=2))

            # записываем фамилию имя замещаемого:
            worksheet.merge(start_row,start_row,start_column+1,start_column+2, set_style(bordleft=2,bordright=2,bordtop=2))
            worksheet.write(start_row, start_column+1,value[0], set_style(ahorz=0x02,bordleft=2,bordtop=2))

            # записываем профессию и разряд
            worksheet.merge(start_row+1,start_row+1,start_column+1,start_column+2, set_style(bordleft=2, bordright=2,bordbottom=2))
            worksheet.write(start_row+1, start_column+1,value[1], set_style(ahorz=0x02,bordleft=2, bordright=2,bordbottom=2))

            # записываем причину отсутствия
            worksheet.merge(start_row,start_row,start_column+3,start_column+4, set_style(bordleft=2,bordright=2,bordtop=2))
            worksheet.write(start_row, start_column+3,value[2], set_style(ahorz=0x02,bordleft=2,bordtop=2))

            # записываем период отсутствия
            worksheet.merge(start_row+1,start_row+1,start_column+3,start_column+4, set_style(bordleft=2, bordright=2,bordbottom=2))
            worksheet.write(start_row+1, start_column+3,value[3], set_style(ahorz=0x02,bordleft=2, bordright=2,bordbottom=2))

            # записываем тариф
            worksheet.merge(start_row,start_row+1,start_column+5,start_column+5, set_style(bordleft=2, bordright=2,bordtop=2,bordbottom=2))
            worksheet.write(start_row, start_column+5,value[-1], set_style(ahorz=0x02,bordleft=2, bordright=2,bordtop=2,bordbottom=2))

            # записываем фамилию замещающего
            worksheet.merge(start_row,start_row,start_column+6,start_column+8, set_style(bordleft=2, bordright=2,bordtop=2))
            worksheet.write(start_row, start_column+6,value[4], set_style(ahorz=0x02,bordleft=2,bordtop=2))

            # записываем профессию и разряд
            worksheet.merge(start_row+1,start_row+1,start_column+6,start_column+8, set_style(bordleft=2, bordright=2,bordbottom=2))
            worksheet.write(start_row+1, start_column+6,value[5], set_style(ahorz=0x02,bordleft=2, bordright=2,bordbottom=2))
            
            # записываем процент оплаты от тарифа
            worksheet.merge(start_row,start_row+1,start_column+9,start_column+9, set_style(bordleft=2, bordright=2,bordtop=2,bordbottom=2))
            worksheet.write(start_row, start_column+9,f"{self.SETINGS_procent[str(self.proffession_number)]}%", set_style(ahorz=0x02,bordleft=2, bordright=2,bordtop=2,bordbottom=2))

            # согласие на исполнение(обьединение ячеек)
            worksheet.merge(start_row,start_row+1,start_column+10,start_column+10, set_style(bordleft=2, bordright=2,bordtop=2,bordbottom=2))
            worksheet.write(start_row, start_column+10,"", set_style(ahorz=0x02,bordleft=2, bordright=2,bordtop=2,bordbottom=2))
            
            # окончательный размер оплаты(обьединение ячеек)
            worksheet.merge(start_row,start_row+1,start_column+11,start_column+11, set_style(bordleft=2, bordright=2,bordtop=2,bordbottom=2))
            worksheet.write(start_row, start_column+11,"", set_style(ahorz=0x02,bordleft=2, bordright=2,bordtop=2,bordbottom=2))
            
        def write_file():
            # Информация для заполнения первой строниы(13 строка на ней заканчивается форма)
            start_row = 13
            start_column = 1
            # считаем количество строк
            end_of_count = len(list_for_write)
            row_count = 0
            for count in range(0,end_of_count):
                if count >10 and count%11==0:
                    start_row+=18
                    value = list_for_write[count]
                    write_row(start_row+row_count,start_column,count+1,value)
                    row_count+=2
                else:
                    value = list_for_write[count]
                    write_row(start_row+row_count,start_column,count+1,value)
                    row_count+=2
            if not os.path.exists(f'ведомости\\{self.SETINGS_current_place}\\{self.SETINGS_current_year}\\{self.SETINGS_current_month}'):
                os.makedirs(os.path.join(("ведомости"),(f"{self.SETINGS_current_place}"),(f"{self.SETINGS_current_year}"),(f"{self.SETINGS_current_month}")))
            workbook.save(f'ведомости\\{self.SETINGS_current_place}\\{self.SETINGS_current_year}\\{self.SETINGS_current_month}\\{self.proffession_number}_199_{self.month}_{self.year}.xls')
        write_file()
    
if __name__ == "__main__":
    CE = CREATE_EXCELL("87100")
    CE = ()
   
    



