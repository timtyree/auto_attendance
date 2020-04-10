#!/usr/bin/env python3
import pandas as pd
import os
import sys
# sys.path.append('python/')
from class_file_clerk import *


# data_dir   = f"{nb_dir}/../data/input/"
data_dir = 'data'
os.chdir(data_dir)
assert(get_sections() is not None)
assert(get_ta() is not None)
print_state()

my_sections = list(get_sections()['Sec ID'].values)
roster_fn   = get_roster_fn()
my_tutors   = list(get_ta()['email'].values)

#take attendance
print(f'\ngetting roster data from {roster_fn}')
df = get_my_students(roster_fn=roster_fn, 
                my_sections = my_sections,
                my_tutors = my_tutors,
                skiprows = 14)
print('')
df_attendence = get_attendence(df)
print(f"\nsaved output as '{get_output_fn()}' in data/output/.")