import configparser
import os
class CREATE_EMPTY_INPUT_FILE():
        def __init__(self,path,profession_number):
                self.path = path
                self.proffession_number = profession_number
                self.main()
        def main(self):
            self.INPUT = configparser.ConfigParser()
            if not os.path.isfile(f'{self.path}\\{self.proffession_number}_input.ini'):
                self.INPUT.add_section("General")
                self.INPUT.add_section("For_summ")
                self.INPUT["General"]["input_user"] = "{}"
                self.INPUT["General"]["for_summ"] = "{}"
                with open(f'{self.path}\\{self.proffession_number}_input.ini', "w", encoding="utf-8") as configfile:
                        self.INPUT.write(configfile)
if __name__ == "__main__":
      CE = CREATE_EMPTY_INPUT_FILE(path = f"Premia_199\\data\\ц.42\\2023\\июнь",
                                   profession_number="87100")
      CE.main()

            