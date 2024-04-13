# -*- coding: utf-8 -*-
"""
Created on Sat Apr 4  2024

script to install needed packages for this project

@author: Alex Kedziora
"""

import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyqt5'])
