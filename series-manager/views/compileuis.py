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
    dest_name_pyside = os.path.splitext(f)[0] + '_ui_pyside.py'
    try:
        commands.getoutput('pyside-uic %s > %s' % (f, dest_name_pyside))
        print(f, 'has been compiled for pyside')
    except Exception as e:
        print('PySide')
        print(e.message)
sys.exit()
