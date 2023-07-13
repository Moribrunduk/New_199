import configparser
import os

class CREATE_SETTINGS_DEFAULT():
    def main(self):
        if os.path.exists('Main\Settings_199\SETTINGS.ini') == False:
            self.create_file_SETTINGS()

    def create_file_SETTINGS(self):
        
        settings = configparser.ConfigParser()
        settings["87100"] = {"cv_three_tarif":0,
                                "cv_four_tarif":0,
                                "cv_five_tarif":0,
                                "cv_six_tarif":0,
                                "procent_text":0}
        settings["87200"] = {"cv_three_tarif":0,
                                "cv_four_tarif":0,
                                "cv_five_tarif":0,
                                "cv_six_tarif":0,
                                "procent_text":0}
        settings["08300"] = {"cv_three_tarif":0,
                                "cv_four_tarif":0,
                                "cv_five_tarif":0,
                                "cv_six_tarif":0,
                                "procent_text":0}
        settings["Days"] = {}                        
        settings["Days"]["days_keys"]=str(['"ИО" - ', '"О" - ', '"Э" - ', '"Р" - ', '"А" - ', '"Ж" - ', '"Д" - ', '"М" - ', '"Б" - ', '"К" - ','"Г" - '])
        settings["Days"]["days_values"]=str(['И.о.мастера', 'Отпуск очередной', 'Отпуск учебный', 'Отпуск по беремености', 'Отпуск за свой счет', 'Пенсионный день/уход за детьми', 'Донорский день', 'Медкомиссия', 'Больничный', 'Командировка','Головняк'])

        settings["Excell_data"] = {"Main_person_name_list":['Власов А.И.','Малыгин И.В.'],
                                   "Botiz_name_list":['Львова Н.А.','Михайлова В.А.'],
                                   "Current_profession_index":'Начальник НИТИЦ',
                                   "Current_main_name_index":'Власов А.И.',
                                   "Current_botiz_profession_index":'Начальник БОТиЗ',
                                   "Current_botiz_name_index":'Львова Н.А.',
                                   "vedomosti":{"42":"0","7":"0","50":"0","55":"0","foto":"0","PZRS":"0"}}
        
        with open("Main\Settings_199\SETTINGS.ini", "w", encoding="utf-8") as configfile:
            settings.write(configfile)


if __name__ == "__main__":
    CS = CREATE_SETTINGS_DEFAULT()
    CS.main()

