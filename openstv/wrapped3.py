#!/usr/bin/env python3.4
#-*- coding: utf-8 -*-

import subprocess
import os

def run(blt_path, output_path, num_seats):
    p = subprocess.Popen(['python2.7', 'myRunElection.py', blt_path, output_path, str(num_seats)], cwd=os.path.dirname(__file__))
    p.communicate()
