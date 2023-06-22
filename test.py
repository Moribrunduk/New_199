from PyQt5.QtCore import QSettings
settings = QSettings("NITIC")
settings.beginGroup("199_settings")
path_with_input = settings.value(f"Path_with_json_87100")
access_path = path_with_input.split("\\")[1]
print(access_path)
access_path = "ц.42"
settings.endGroup()

settings.beginGroup("GOD_parameters")
Current_user = settings.value("Current_user")
print(Current_user)


settings.beginGroup('Users_access')
user_access = settings.value(Current_user)
print(user_access)

if [access_path] in user_access:
    print("Доступ получен")

