#!/usr/bin/env python2
import os
import sys
import subprocess
import commands
directory = os.path.dirname(os.path.abspath(__file__))
extension = ".ui"
list_of_files = [file for file in os.listdir(
    directory) if file.lower().endswith(extension)]
for f in list_of_files:
    dest_name_pyqt4 = os.path.splitext(f)[0] + '_ui_pyqt4.py'
    try:
        commands.getoutput('pyuic4 %s > %s' % (f, dest_name_pyqt4))
        print(f, 'has been compiled for pyqt4')
    except Exception as e:
        print('PyQt4')
        print(e.message)
sys.exit()
