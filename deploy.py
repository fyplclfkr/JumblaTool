# -*- coding: utf-8 -*-
import os
from JumblaLib.Common.setting import DEBUG
if not DEBUG:
    #os.system('nuitka --standalone --windows-disable-console --include-package=sqlite3,http.cookies --plugin-enable=pyqt5 --include-qt-plugins=sensible,styles --mingw64 --show-memory --show-progress --output-dir=output --windows-icon-from-ico=JumblaLib/Resources/images/logo.ico jumbla.py')
    os.system('nuitka --standalone --include-package=sqlite3,http.cookies --plugin-enable=pyqt5 --include-qt-plugins=sensible,styles --mingw64 --show-memory --show-progress --output-dir=output --windows-icon-from-ico=JumblaLib/Resources/images/logo.ico jumbla.py')
