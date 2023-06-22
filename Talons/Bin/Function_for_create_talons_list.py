import json
import os
from PyQt5.QtCore import QSettings

class ALL_FUNCTION_TO_CREATE_TALONS_LIST():
    """функция, которая преобразует готовый Json файл из программы для 199
        в json файл для программы с талонами"""
    def __init__(self,start_data=1,final_data=31):
        super(ALL_FUNCTION_TO_CREATE_TALONS_LIST,self).__init__()
        self.start_data = start_data
        self.final_data = final_data
        self.main()
    
    def main(self):
        # фаил из которого получаем настройки для программы
        self.settings()
        # получаем путь, к файлу JSON для 199
        self.indiciation_path_199_json()
        # создаем словарь который определяет количество талонов
        self.create_list_with_names_talons()
        # функция, которая позволяет добаить в список человека, которого нет в табеле
        # self.add_a_person_who_is_not_in_the_json()
        # функция которая создает список талонов между выбранными датами
        self.to_sort_between_dates()
        # функция которая возвращает список, содержащий список дефектоскопистов на каждый день межжду выбранными датами
        self.create_list_with_lists_per_data()
    
    def settings(self):
        # количестов часов которое нужно для получения талона
        self.minimum_number_of_hours_to_receive_a_talon=4
        
    def indiciation_path_199_json(self):
        """функция которая определяет расположения файла JSON для 199"""
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("Talons_program")
        path = self.settings.value("json_file_path")
        
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
    
    def create_list_with_names_talons(self):
        """функция,которая создает  список [табельный,фамилия инициалы,[дни когда работник получает талон]]"""
        list_with_names_talons = []
        tabels = self.all_data["Табельный"]
        for tabel in tabels:
            sername = (self.all_data["Табельный"][tabel]["фамилия"])
            name = (self.all_data["Табельный"][tabel]["инициалы"])
            del self.all_data["Табельный"][tabel]["отработанные смены"][15]
            work_days = self.all_data["Табельный"][tabel]["отработанные смены"]
            talons_days = []
            for i,day in enumerate(work_days,1):
                # для каждой итерации создаем список дней, где положен талон
                
                # исключаем из списка дни которые нельзя преобразовать в INT(т.е больничные отгулы и т.д)
                try:
                    day = (day[0])
                except:
                    day = day
                # талоны положен только если рабочий день более заявленного в настройках количества часов
                try:
                    if int(day)>self.minimum_number_of_hours_to_receive_a_talon:
                        # добаляем этот день в список
                        talons_days.append(i)
                except ValueError:
                    continue
            list_with_names_talons.append([tabel,f"{sername} {name}", talons_days])    

        self.list_with_names_talons = list_with_names_talons
    
    def add_a_person_who_is_not_in_the_json(self):
        """функция, которая позваляет добавить в список человека которого небыло в файле JSON"""
        new_number = input("введите табельный \n")
        new_name = input("введите Фамилию И.О.\n")
        new_date = int(input("введите дату\n"))

        new_person = [new_number,new_name,[new_date]]

        self.list_with_names_talons.append(new_person)

    def to_sort_between_dates(self):
        """создаем функцию, которая выбирает даты из списка, который возвращает функция
        create_list_with_names_talons и сокращает список дат которые входят в заданный диапозон"""
        # конечный список который будет результатом функции
        list_with_sortet_by_data=[]

        for item in self.list_with_names_talons: #перебираем функцию со всеми датами с полным списком
            day_list = []
            for day in item[2]: #каждый итем перебираем по дням и сортируем между датами
                if day >= self.start_data and day <= self.final_data:
                    day_list.append(day)
            if day_list != []:   #исключаем попадание в список людей которые в этот период не получают талоны
                list_with_sortet_by_data.append([item[0],item[1],"Деф-ст РГГ",day_list])
        
        self.list_with_sortet_by_data=list_with_sortet_by_data
    
    def create_list_with_lists_per_data(self):
        self.final_list = []
        for day in range(self.start_data,self.final_data+1):
            day_list = []
            for personal in self.list_with_sortet_by_data:
                if day in personal[3]:
                    day_list.append([personal[0],personal[1],personal[2],day])
            self.final_list.append(day_list)
        self.final_list = list(filter(None, self.final_list))
        return self.final_list
       
                    
if __name__ == "__main__":
    CRJP=ALL_FUNCTION_TO_CREATE_TALONS_LIST
    CRJP()

