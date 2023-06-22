import os
import xlrd
import json

from PyQt5.QtCore import QSettings



class CREATE_JSON_DATA():
    def __init__(self):
        super().__init__()
    def main(self):
        self.get_data_personal()

    def get_data_personal(self):

        # загружаем рабочий файл 
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("Talons_program")

        work_book = xlrd.open_workbook(self.settings.value("file_path"))
        # загружаем рабочий лист
        self.work_sheet = work_book.sheet_by_name("Табель")
        work_sheet = self.work_sheet

        all_data = {}

        all_data = {"Табельный":[]}
        all_data ["Табельный"]={}
        print(all_data)

        # ищем ячейку с которой начинается шифр профессии
        for row in range(0,work_sheet.nrows):
            x = work_sheet.cell(row,4).value
            if x == "87100":
                start_row = row
                print(start_row)
                break
        self.start_row = start_row
        # ищем последнюю ячейку для данного шифра профессии
        for row in range(start_row,work_sheet.nrows,2):
            x = str(work_sheet.cell(row,4).value)
            x = x.partition(".")[0]
            if str(x) == str("87100"):
                # +2 чтобы цеплял последнего человека([TEST])
                final_row = row+2
        self.final_row = final_row
        
        # # заполняем нашу базу данных из файла, по каждому табельному

        # #ГЛАВНЫЙ СКРИПТ

        for row in (range(start_row,final_row,2)):
        
            sername = work_sheet.cell(row,2).value
            name = work_sheet.cell(row+1,2).value.replace(" ","")
            tabel_number = int(work_sheet.cell(row,1).value)


            #создаем список выработанных дней по табелю(обновляем с каждой итерацией)
            calendar_time = []
            
            # первая строка в календаре
            for cell in range(6,22):
                
                try:
                    #первый символ переводим в число
                    calendar_time.append(int(work_sheet.cell(row,cell).value))
                    # TODO
                    # calendar_time.append(int(work_sheet.cell(row,cell).value[0]))
                except:
                    # тип float вылетает тоже в ексепт, поэтому переводим его в число
                    if type(work_sheet.cell(row,cell).value) == float:
                        calendar_time.append(int(work_sheet.cell(row,cell).value))
                    else:
                    # остальное все оставляем как есть
                        calendar_time.append(work_sheet.cell(row,cell).value)
                
            # вторая строка в календаре
            for cell in range(6,22):
                try:
                    #первый символ переводим в число
                    # calendar_time.append(int(work_sheet.cell(row+1,cell).value[0]))
                    # TODO
                    calendar_time.append(int(work_sheet.cell(row+1,cell).value))
                except:
                    # тип float вылетает тоже в ексепт, поэтому переводим его в число
                    if type(work_sheet.cell(row+1,cell).value) == float:
                        calendar_time.append(int(work_sheet.cell(row+1,cell).value))
                    else:
                    # остальное все оставляем как есть
                        calendar_time.append(work_sheet.cell(row+1,cell).value)
            
            all_data["Табельный"][tabel_number] = {
                    "фамилия":sername,
                    "инициалы":name,
                    "отработанные смены":calendar_time}
        print(all_data)
        self.data_year = work_sheet.cell(1,0).value.replace(" ","")
        self.data_month = work_sheet.cell(1,2).value
        self.data_place = work_sheet.cell(0,17).value
        print(self.data_place)
        
       
        self.file_path = (f"Talons\\Data\\{self.data_place}\\{self.data_year}\\{self.data_month}\\")
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        with open(f"{self.file_path}\\{self.data_month}_{self.data_year}.json", "w", encoding="utf-8") as file:
                json.dump(all_data,file, ensure_ascii=False, indent=4)
        
        self.file_path_for_settings = f"{self.file_path}\{self.data_month}_{self.data_year}.json"
        
        self.settings.setValue("json_file_path",self.file_path_for_settings)
        self.settings.endGroup()

if __name__ == "__main__":
    m = CREATE_JSON_DATA()
    m.main()