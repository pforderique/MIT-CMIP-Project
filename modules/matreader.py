'''
Mat Reader

Piero Orderique 
28 Jan 2021

Learning how to use scipy.io lib to open and read mat files
'''
from os import scandir
from scipy.io import loadmat

class FileReader():
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.extension = file_name[file_name.find("."):] # caution! error if '.' in name

    def get_file_name(self):
        return self.file_name

    def get_extension(self):
        return self.extension

class MatFileReader(FileReader):
    def __init__(self, mat_file_name) -> None:
        super().__init__(mat_file_name)
        pass

def create_files_list(directory):
    files_list = []
    with scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                files_list.append(entry.name)
    return files_list

def extract_info(filename):
    era, data_type = [], []
    start = 6 # CIMP5_---
    end = len(filename) - 4 # ---.mat
    _found = False
    for idx in range(start, end): 
        char = filename[idx]
        if char == '_': 
            _found = True
            continue
        if not _found: 
            era.append(char)
        else:
            data_type.append(char)

    return ''.join(era), ''.join(data_type)

################################ DRIVER CODE ################################
mat_files_directory = "mat_files/"
mat_file_names = create_files_list(mat_files_directory) # Comment out for testing rn
mat_file_name = r"mat_files\CMIP5_historical_tasmax.mat"

# use this to create multiple file reader objects
# for file_name in mat_file_names: 
#     print(file_name) # for degugging
#     era, data_type = extract_info(file_name)
#     print(era, data_type)

f1 = MatFileReader(mat_file_name)
print(f1.get_extension())