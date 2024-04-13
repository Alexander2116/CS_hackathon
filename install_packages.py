# -*- coding: utf-8 -*-
"""
Created on Sat Apr 4  2024

script to install needed packages for this project

@author: Alex Kedziora
"""

import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyqt5'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'manim']) # you need to install FFmpeg for this to work
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'json'])
