'''
Mat Reader

Piero Orderique 
28 Jan 2021

Learning how to use scipy.io lib to open and read mat files
'''
from os import scandir
from scipy.io import loadmat

def create_files_list(directory):
    files_list = []
    with scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                files_list.append(entry.name)
    return files_list

######################## DRIVER CODE ################################
mat_files_directory = "mat_files/"
mat_files = create_files_list(mat_files_directory)

for file in mat_files: print(file)