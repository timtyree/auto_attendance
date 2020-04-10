#!/usr/bin/env python3
import pandas as pd
import os
##################################
##### setup local file system  ###
##################################
def setup_file_system():
    '''check that directory tree exists as desired and make it if it doesn't exist'''
    nb_dir = os.getcwd()
    os.chdir(f'{nb_dir}/')
    if not os.path.exists('data/'):
        os.mkdir('data/')
    os.chdir('data/')
    if not os.path.exists('output/'):
        os.mkdir('output/')
    if not os.path.exists('input/'):
        os.mkdir('input/')
    os.chdir('input/')
    if not os.path.exists('from_Student_Roster/'):
        os.mkdir('from_Student_Roster/')
    if not os.path.exists('from_Zoom/'):
        os.mkdir('from_Zoom/')
    os.chdir(nb_dir)
    return True

if __name__ == "__main__":
	setup_file_system()
	print("A local file system has been set up.")
	print("\nNow, fill out the following:")
	print("my_ta_list.csv  - your TAs and tutors")
	print("my_sections.csv - your discussion sections")
	print("\nIf you have the relevant data located in from_Student_Roster and from_Zoom,")
	print("Then you may proceed with $ ./take_attendance.sh.\n")