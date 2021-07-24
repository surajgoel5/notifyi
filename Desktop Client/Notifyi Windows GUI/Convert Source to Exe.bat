cd pyinstaller_builds
pyinstaller --onefile --clean --windowed --distpath ..\SetupFiles\ --icon ..\imagefiles\notifyi_icon.ico ..\Source\Notifyi.py
pyinstaller --onefile --clean --windowed --distpath ..\SetupFiles\ --icon ..\imagefiles\notifyi_icon.ico ..\Source\NotifyiUserManager.py