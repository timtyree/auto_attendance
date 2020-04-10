#!/usr/bin/env python3
import pandas as pd
import numpy as np
# import click #command line interface

#import tkinter for simple gui
from tkinter import filedialog, Tk
#automate the boring stuff
import time, os, sys, re, warnings, shutil

#define localfile system
if not 'nb_dir' in globals():
    nb_dir = os.getcwd()
data_dir   = f"{nb_dir}/data/"
output_dir = f"{data_dir}output/"
roster_dir = f"{data_dir}input/from_Student_Roster/"
zoom_dir   = f"{data_dir}input/from_Zoom/"
dict_dir   = 'students_email_dictionary_for_zoom_data.xlsx'

#TODO: add dialogue so ta's don't need to manually enter files and change personal settings
#TODO: check that all entries of student attendence are summed from original data (see pd.concat line)
#  i.e. check that if a student leaves and then comes back, both entries are accounted for

##################################
##### local file accessability ###
##################################
def get_output_fn():
    '''get save_fn from section data'''
    sc_lst = list(get_sections()['SecCode'].values)
    sc_lst.reverse()
    assert(len(sc_lst)>0)#assert at least one section is entered
    save_fn = f'attendence of {sc_lst.pop()}'
    while len(sc_lst)>0:
        save_fn = save_fn + f' and {sc_lst.pop()}'
    save_fn = save_fn + '.xlsx'
    return save_fn

def get_roster_fn():
    os.chdir(roster_dir)
    fn_pattern = re.compile(f'''(
    [a-zA-Z0-9_%+-]+.xlsx
    )''',re.VERBOSE)
    roster_fn = None
    for string in os.listdir():
        ml = fn_pattern.match(string)
        if ml is not None:
            roster_fn = ml
    assert(roster_fn is not None)
    return roster_fn.string

def get_zoom_fn_list():
    os.chdir(zoom_dir)
    zoom_fn_list = []
    for string in os.listdir():
        boo = string.split('.')[-1]=='csv'
        if boo:
            zoom_fn_list.append(string)
    return zoom_fn_list

def get_tutor_no():
    return int(get_ta().size/2)

############################################
##### print current sections and ta list ###
############################################
def get_sections(
    fn  = "my_sections.csv"):
    return pd.read_csv(data_dir+fn)
def print_sections(fn  = "my_sections.csv"):
    print(get_sections(fn=fn))
def add_section(sec_id, sec_code, 
    fn  = "my_sections.csv"):
    df = pd.DataFrame({'Sec ID':[sec_id],'SecCode':[sec_code]})
    df = pd.concat([get_sections(fn=fn),df])
    df.to_csv(fn, index=False)
    return True

def get_ta(
    fn  = "my_ta_list.csv"):
    os.chdir(data_dir)
    return pd.read_csv(fn)
def add_ta(name, email, 
    fn  = "my_ta_list.csv"):
    df = pd.DataFrame({'name':[name],'email':[email]})
    df = pd.concat([get_ta(fn=fn),df])
    df.to_csv(fn, index=False)
    return True
    return pd.concat([get_sections(fn=fn),df])
def print_ta(fn  = "my_ta_list.csv"):
    print(get_ta(fn=fn))

def print_state(fn_ta  = "my_ta_list.csv", fn_sec = "my_sections.csv"):
    print('Your current discussion sections:')
    print_sections(fn=fn_ta)
    print('\nYour current teaching assistants:')
    print_ta(fn=fn_sec)

###################################
##### file search gui interface ###
###################################
#setup user interface for file selection
def search_for_file_path (currdir = os.getcwd()):
    root = Tk()
    tempdir = filedialog.askopenfilename(parent=root,initialdir=currdir, title="Please select desired file.")                                
    root.destroy()
    if len(tempdir) > 0: print ("Frames: %s" % tempdir)
    return tempdir

#file update user interface for from_Student_Roster and from_Zoom
def search_for_roster():
    '''move data_file_name to correct input folder'''
    data_file_name = search_for_file_path()
    assert(os.path.exists(data_file_name))
    #move data_file_name to 
    shutil.move(data_file_name, roster_dir)
def search_for_zoom_file():
    '''move data_file_name to correct input folder'''
    data_file_name = search_for_file_path()
    assert(os.path.exists(data_file_name))
    shutil.move(data_file_name, zoom_dir)

###################################
##### attendance functionality  ###
###################################
def get_my_students(roster_fn, my_sections = [4850, 4852, 4858],  
                   my_tutors = ['y7pan@ucsd.edu', 'tan005@ucsd.edu', 'xis115@ucsd.edu'],
                   skiprows = 14):
    # nb_dir = os.getcwd()
    os.chdir(roster_dir)
    assert(os.path.exists(roster_fn))
    df = pd.read_excel(roster_fn, skiprows=skiprows)
    col = df.columns[0]
    print(f"matching section ID's with the column, '{col}'.")
    df['mine'] = False
    for si in my_sections:
        boo = df[col] == si
        df.loc[boo, 'mine'] = True
    df_mine = df.query('mine').copy()
    email_col = df_mine.columns[-2]
    print(f"email columns taken to be '{email_col}'.")

    #to .txt file
    save_fn = 'my_students.txt'
    s_out = pd.concat([pd.Series(my_tutors),df_mine[email_col].dropna()])
    s_out.to_csv(save_fn, index=False, header=False)
    ns = df_mine[email_col].dropna().size
    print(f"printed {ns} students to '{save_fn}'.")
    os.chdir(nb_dir)
    return df_mine
    # return df_mine[email_col].dropna()

def get_attendence(df,
    time_thresh = 35,
    email_col = 'User Email',
    name_col = 'Name (Original Name)',
    skiprows=2):
    '''
    get_attendence() converts Zoom attendence data to Canvas course roster data.
     attendence_dir is the relative directory holding only Zoom attendence 
     '.csv' files. attendence_dir is given relative to this file's directory.
     get_attendence() returns a pandas dataframe of the desired attendence 
     data and saves it in save_fn. df is the dataframe returned by get_my_students().'''
    #get file names
    save_fn = get_output_fn()
    attendance_dir = zoom_dir

    #get tutor number
    tutor_no = get_tutor_no()

    #import attendence spreadsheet
    print('inputted attendance files:')
    att_fns = get_zoom_fn_list()
    print(att_fns)

    d = pd.concat([pd.read_csv(fn, skiprows=skiprows) for fn in att_fns], sort=False)
    d = d[d.index>0]#drop the TA in charge of discussion (assumed to be at index position 0)
    d.reindex()

    #import dictionary and update any student emails from Zoom contained therein
    os.chdir(data_dir)
    if os.path.exists(dict_dir):
        dse = pd.read_excel(dict_dir)
        d3 = d.set_index(name_col, drop=False)
        # d3[email_col] = dse.set_index(name_col)
        for n,e in dse.values:
            d3.loc[n,email_col] = e
        d = d3.reset_index(drop=True).copy()
        del d3, dse

    #take attendence 
    # for each student present for at least time_thresh=35 minutes, change their attendence to 1
    time_attended_col = d.columns[-1]
    attendedQ = (d[time_attended_col]>time_thresh).astype('uint8')
    d['Attendence'] = attendedQ
    print(f"{sum(attendedQ)-tutor_no} out of {len(attendedQ)-tutor_no} students attended this time.")
    # index by email, and then set the attendence field
    email_dict = dict(d[[email_col,'Attendence']].dropna().values)
    out = df.set_index('Email')
    out['Attendence'] = pd.Series(email_dict)
    match_no = len(out[~out['Attendence'].isna()])
    print(f"{match_no} students matched by email listed in Zoom.")
    # set attendence values that are still NaN to zero
    out.loc[out['Attendence'].isna(),'Attendence'] = 0
    out['Attendence'] = out['Attendence'].astype('uint8')

    #save attendence sheet
    os.chdir(output_dir)
    out = out.reset_index()[['Sec ID', 'PID', 'Student', 'Pronoun', 'Credits', 'College', 'Major', 'Level', 'Email', 'Attendence']]
    out.to_excel(save_fn, index=False)
    os.chdir(nb_dir)

    ##Record the set of students not matched
    #emails matched/not matched as true or false (--> attendence is NaN) according to Roster data
    matched = set(out[~out['Attendence'].isna()].index)
    not_matched = set(out[out['Attendence'].isna()].index)
    #show students that attended but were not matched according to the Roster data
    # attended according to Zoom data
    d2 = d[d['Attendence']==1].set_index(email_col)
    # select Zoom data that has emails matched to Roster data
    boo = [i in matched for i in d2.index]
    # take the compliment of ^that selection to get attending students not yet accounted for
    d2 = d2[~np.array(boo)]
    d2[d2.index.name] = d2.index.values
    #record my match of Zoom names to emails so I don't need to do this over
    # save a list of students and emails from Roster that were not matched
    os.chdir(data_dir)
    out.loc[not_matched]['Student'].to_csv('students_not_matched_in_roster_dataset.csv', header=True)
    #save a list of students that attended the Zoom meeting that were not matched with a Roster email
    d2.set_index(name_col)[email_col].to_excel(dict_dir, header=True)
    return out