#!/bin/bash

cwd=$(pwd)
target_path="$cwd/data/input/from_Zoom/"

cd data
#make an archived folder if it doesn't exists
[ ! -d data/ ] && mkdir archived
#try making an archived folder, catching the error if it exists and doing nothing about it
# mkdir archived || :

#move old attendance files to archives
mv input/from_Zoom/* archived
cd ..

#TODO(later): call a function that automates the (albeit brief) task of downloading attendance files

#get files in ~/Downloads in the last 3 days that go like 
#"participants_ ... .csv" and copy ^those to $(cwd)+data/input/from_Zoom
cd ~/Downloads
find . -name 'participants_*.csv' -type f -mtime -3 -exec cp {} $target_path \;
cd $cwd