pyinstaller --noconsole --noconfirm --onefile --icon=logo.ico -n "אוצרות או צרות" game.py
pyinstaller --noconsole --noconfirm --onefile --add-data "dist/אוצרות או צרות.exe;." --add-data "אוצרות או צרות.html;." -n "אוצרות או צרות installer" installer.py
rd /S /Q "build"