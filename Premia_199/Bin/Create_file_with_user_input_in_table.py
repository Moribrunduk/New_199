import configparser
import json
import os
from PyQt5.QtCore import QSettings


class CREATE_FILE():
    def __init__(self, proffession_number):
        self.proffession_number = proffession_number
        super(CREATE_FILE, self).__init__()

    def Main(self):
        self.LoadPathInformation()
        self.MAIN_FINCTION()

    def LoadPathInformation(self):
        
        self.settings = QSettings("NITIC")
        self.settings.beginGroup("199_settings")
        self.path_with_json = self.settings.value(f"Path_with_json_{self.proffession_number}")
        self.path_with_input = self.settings.value(f"Path_with_input_{self.proffession_number}")
        self.settings.endGroup()
        self.SETINGS = configparser.ConfigParser()
        self.SETINGS.read("Main\Settings_199\SETTINGS.ini",encoding="utf-8")
        
        self.TEMP = configparser.ConfigParser()
        self.TEMP.read(f'{self.path_with_input}')

        # файл для записи
        self.substitutes = configparser.ConfigParser()
        self.substitutes.read('datalist of substitutes')

        with open(f'{self.path_with_json}', "r", encoding="utf-8") as file:
            self.all_data = json.load(file)

        self.tabels = self.all_data["шифр"][str(self.proffession_number)]["Табельный"]
        
    def ReasonBlock(self,tabel_for_function):

        # проверяем если нет смен отсутствия, сразу создаем список на выход
        if self.tabels[tabel_for_function]["Пропущенные смены"] == []:
            reason_list_x = []
            return reason_list_x
            
        else:
            # БЛОК 1
            print(f"[INFO]-блок-1")
            self.missed_working_days = list(self.tabels[tabel_for_function]["Причина пропуска смен"].keys())
            print("----Пропущенные дни(missed_working_days)-----")
            print(self.missed_working_days)
            self.reasons = list(self.tabels[tabel_for_function]["Причина пропуска смен"].values())
            print("----Причина пропуска этих смен(reasons)----")
            print(self.reasons)

            # убираем причины отстутсвия за которые не дается замещение
            self.new_missed_working_days = []
            self.new_reasons = []
            # задае общее число эдементов с отсчетом с 0
            count = 0
            for i,item in enumerate(self.reasons):
                if str(item) == "-":
                    continue
                elif str(item) in ("М",'м',"M"):
                    continue
                elif str(item) in self.SETINGS["Days"]["days_keys"]:
                    self.new_reasons.append(item)
                elif str(item)[1:3] in ("МН","мн","МВ","мв","МД","мд","м","М"):
                    self.new_reasons.append("ИО")
                elif int(str(item)[0]) not in range(0,25):
                    self.new_reasons.append(int(str(item)[0]))  
                else:
                    self.missed_working_days.pop(count+i)
                    count-=1
                   
        self.reasons = self.new_reasons
        print("----список причин отсутствия после чистки(reasons)----")
        print(self.reasons)

        # БЛОК-2
        print('[INFO] -блок-2')
        if self.reasons == []:
            reason_list_x = []
            return reason_list_x

        else:
            # print(self.reasons)
            ferst_day = self.missed_working_days[0]
            last_day = ferst_day
            count = 0
            reason_list_x = [()]
            main_reason = self.reasons[0]
            for i,reason in enumerate(self.reasons):
                try:
                    if main_reason == reason:
                            last_day = self.missed_working_days[i]
                            reason_list_x[count]=(ferst_day,last_day,reason)
                    else:
                        ferst_day = self.missed_working_days[i]
                        last_day = ferst_day
                        reason_list_x.append("")
                        main_reason=reason
                        count+=1
                        reason_list_x[count]=(ferst_day,last_day,reason)
                except: Exception
        
        print('----список пропущенных дней по причинам(не редактированный)(reason_list_x)----')
        print(reason_list_x)
        
        # БЛОК-3
        print('[INFO] -блок-3')
        not_missed_days = []
        wikend = self.all_data["шифр"][str(self.proffession_number)]["Рабочий календарь"]
        print(wikend)
        

        try:
            # создаем список дней которые человек работал
            for days in range(1,int(self.missed_working_days[-1])+1):
                    if str(days) not in self.missed_working_days and wikend[str(days)] != "-":
                        not_missed_days.append(days)
            print("---список отработанных дней(not_missed_days) ---")
            print(not_missed_days)
            
            if not_missed_days == []:
                return reason_list_x
            else:
                count = len(reason_list_x)
                new_reason_list_x = [()]
                new_count=0
                for i,reason in enumerate(reason_list_x):
                    for days in not_missed_days:
                        if int(days) in range(int(reason[0]),int(reason[1])+1):
                            new_reason_list_x[new_count]=(int(reason[0]),days,reason[2])
                            # new_reason.append(int(reason[0],days,reason[2]))
                            new_reason_list_x.append("")
                            new_count+=1
                            # print(new_reason_list_x)
                            break
                        else:
                            new_reason_list_x[new_count] = reason
                    new_count+=1
                    new_reason_list_x.append("")

                    for days in not_missed_days:
                        if int(days) in range(int(reason[0]),int(reason[1])+1):
                            new_reason_list_x[new_count]=(days+1,int(reason[1]),reason[2])
            
                
        except: IndexError

        while "" in new_reason_list_x:
            new_reason_list_x.remove("")
        print("----окончательный список на вывод----")
        print(new_reason_list_x)
        
        return new_reason_list_x
                
    def UserRework(self,tabel_for_function):
        """
        функция которая возвращает список (день начала замещения, последний день замещения, табельный замещающего)

        """
        # БЛОК-21
        print("[INFO] ----(Блок-21)----")
        print("----данные введенные пользователем(full_list_of_user_input)----")
        full_list_of_user_input = self.TEMP['General']['for_summ']
        full_list_of_user_input = eval(full_list_of_user_input)
        print(full_list_of_user_input)
        

        # преобразуем в словарь
        # {(табельный,число): замещающий табельный}
        list_of_user_input = {}
        for key, value in full_list_of_user_input.items():
            list_of_user_input[key[0:2]]=value
        print("----преобразуем данные в словарь{(табельный-дата)-замещающий}(list_of_user_input)----")
        print(list_of_user_input)

        # БЛОК22
        print("[INFO] ----(Блок-22)----")
        # задаем начальный день, когда первый раз идет замещение
        data_x = int(list(list_of_user_input.keys())[0][1])
        # print(data_x)

        # Приравниваем конечный день, к начальному, чтобы изменять в дальнейшем
        data_z = int(data_x)
        # print(data_z)
        # создаем лист замещения
        remoove_day_list = [()]
        item_namber = 0
        # print(data_x)
        personal_number = tabel_for_function
        #создаем словарь для того чтобы добавить в него "-" в дни, когда небыло замещений(новый, чтобы попорядку)
        list_of_user_input_selected_number = {}
        # создаем цикл в который добавляем дни где небыло замещения
        for day in range(1,32):
            # если ключа (табельный, день) нет в словаре
            if (personal_number,str(day)) not in list_of_user_input:
                # print((personal_number,str(day)))
                # print(list_of_user_input)
                # добавляем такой ключ со значением "-"
                list_of_user_input_selected_number[personal_number,str(day)] = "-"
            else:
                # если такой ключ есть добавляем его в новый словарь
                list_of_user_input_selected_number[personal_number,str(day)] = list_of_user_input[personal_number,str(day)]

        
        print("---список на весь месяц-замещающий-причина-или отсутствие замещения(list_of_user_input_selected_number)---")
        print(list_of_user_input_selected_number)

        # БЛОК23
        print("[INFO] ----(Блок-23)----")
        
        # первый заамещающий, чтобы потом изменять
        personal = list(list_of_user_input_selected_number.items())[0][1]

        # Пробегаемся по этому словарю, чтобы вычислить периоды замещения
        for key,value in list_of_user_input_selected_number.items():
                
                # if key[0] == personal_number:
                #     print(f' {key[1]}-----{value}')
                # если значение ключа равно предыдущему значению(значение personal первое выбрано в самом начале)
                if value == personal:
                    # то меняем дату окончания замещения
                    data_z = key[1]
                    # перезаписываем пару(ключ)=значение
                    remoove_day_list[item_namber] = (data_x,data_z,value)
                if value != personal:
                    # если в итерации поменялся табельный замещающего
                    # перезаписываем этот табельный
                    personal = value
                    # устанавливаем первый день замещения
                    data_x = key[1]
                    # устанавливаем последний день замещения
                    data_z = key[1]
                    # прибавляем к количеству элементов номер 1
                    item_namber+=1
                    # добавляем в лист новый элемент
                    remoove_day_list.append("")
                    # заполняем этот элемент
                    remoove_day_list[item_namber] = (data_x,data_z,value)
        for item in remoove_day_list:
            if item[2] == "-":
                remoove_day_list.remove(item)
        print(remoove_day_list)
        return remoove_day_list

    def WriteInFile(self,tabel_for_function):
        
        #список содержаший (первый день отсутсвия, последнйи,причина отсутствия)
        reasons = self.ReasonBlock(tabel_for_function)
        # print(reasons)
        
        #список содержащий(первй день замещения, последний день замещения, табельный замещающего)
        rework = self.UserRework(tabel_for_function)
        # print(rework)
        print("[INFO]----блок-31")
        if reasons ==[]:
            final_list=[]
        elif rework ==[]:
            final_list = []
        else:
            # создаем список, для печать в таблицу
            final_list = []
            # создаем переменную, количество значений в списке для печати
            count = 0
            reason_count = 0
            for reason in reasons:
                count+=reason_count
                final_list.append("")
                print(reason)
                #обьявляем начальный день
                Day_x = reason[0]
                #обьявляем конечный день
                Day_z = int(Day_x)
                #обьявляем первый табельный
                tabel_number = int(rework[0][2])
                
                # пробегаемся по элементам списка пропущенных смен
                for item in rework:
                    # проверяем изменился ли табельный
                    if tabel_number == int(item[2]):
                        # проверяем входят ли дни когда этот табельный замещает, в причину замещения
                        if int(reason[0])<=int(item[0])<=int(item[1])<=int(reason[1]): 
                            print(f"[INFO]{item} входит в {reason}")
                            # изменяем крайний день замещения
                            Day_z = int(item[1])
                            # заменяем этот элемент в списке на печать
                            print(tabel_for_function,reason[2],Day_x,Day_z,tabel_number)
                            final_list.append("")
                            final_list[count]=(tabel_for_function,reason[2],Day_x,Day_z,tabel_number)
                            print(final_list)
                        else:
                            print(f"[INFO]{item} не входит в {reason}")
                            if int(item[1]) > int(reason[1]):
                                Day_z = int(reason[1])
                            else:
                                Day_z = int(item[1])
                                
                            print(tabel_for_function,reason[2],Day_x,Day_z,tabel_number)
                            final_list.append("")
                            # исключаем вариант, когда дата замещения первая больше второй
                            if int(Day_x) < int(Day_z):
                                final_list[count]=(tabel_for_function,reason[2],Day_x,Day_z,tabel_number)
                            else:
                                continue

                    # если табельный поменялся
                    else:
                        if int(reason[0])<=int(item[0])<=int(item[1])<=int(reason[1]):
                            print(f"{item} входит в {reason}")
                            # увеличивем количество элементов в списке
                            count+=1
                            # меняем первый день замещения
                            Day_x = int(item[0])
                            # меняем второй день замещегия
                            Day_z = int(item[1])
                            # меняем табельный
                            tabel_number = int(item[2])
                            # добавляем в список пустое значение
                            final_list.append((""))
                            # заполняем это значение списком
                            final_list[count] = (tabel_for_function,reason[2],Day_x,Day_z,tabel_number)
                reason_count+=1
                final_list.append("")
                
            # удаляем из списка пустой элемент("откуда взялся хз")  
        while "" in final_list:              
            final_list.remove((""))
        print(final_list)
        

        self.substitutes['DEFAULT'][f'{self.proffession_number},{tabel_for_function}'] = str(final_list)
        with open(f'{self.path_with_input[:-9]}for_excell.ini', 'w', encoding="utf-8") as configfile: 
            self.substitutes.write(configfile)
        self.settings.beginGroup("199_settings")
        self.settings.setValue(f"Path_for_excell_{self.proffession_number}",f'{self.path_with_input[:-9]}for_excell.ini')
        self.settings.endGroup()

    def MAIN_FINCTION(self):

        for tabel in self.tabels:
                self.WriteInFile(tabel_for_function=str(tabel))
                self.ReasonBlock(tabel_for_function=str(tabel))
        # tabel =  441
        # # self.ReasonBlock(tabel_for_function=str(tabel))
        # # self.UserRework(tabel_for_function=str(tabel))
        # self.WriteInFile(tabel_for_function=str(tabel))
                
if __name__ == '__main__':
        CF = CREATE_FILE("87100")
        CF.Main()
