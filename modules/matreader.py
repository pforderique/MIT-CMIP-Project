'''
Mat Reader

Piero Orderique 
28 Jan 2021

Learning how to use scipy.io lib to open and read mat files
'''
from os import scandir
from scipy.io import loadmat

class FileReader():
    def __init__(self, filename, directory="") -> None:
        self.path = directory + filename
        self.file_name = filename
        self.extension = filename[filename.find("."):] # caution! error if '.' in name

    def get_path(self):
        return self.path

    def get_file_name(self):
        return self.file_name

    def get_extension(self):
        return self.extension

class MatFileReader(FileReader):
    def __init__(self, mat_file_name, directory="mat_files/") -> None:

        # initialize data from just file name string
        super().__init__(mat_file_name, directory)
        self.era, self.variable = self.__extract_info_from_file_name(self.file_name)
        self.file = loadmat(self.path)

        # setup rest of mat file information and attributes
        self.__setup()

    def __setup(self):
        # main results variable where info is stored
        self.results = self.file["results"]

        # variable lookup: maps file name -> field name (ONLY 2 SUPPORTED RIGHT NOW)
        self.supported_variables = {
            "pr"     : "Precip",
            "tasmax" : "Temp",
        }

        # initialize GCM_fields
        self.GCM_FIELDS = {
            'File'      : None,
            'Lat'       : None,
            'Lon'       : None,
            'IdxLat'    : None,
            'IdxLon'    : None,
            'Values'    : None,
            'Calendar'  : None,
            'Unit'      : None,
            'Years'     : None,
            'StartYear' : None,
            'EndYear'   : None,
            'Months'    : None,
            'Trim'      : None,
        }
        try: 
            self.GCM_FIELDS[self.supported_variables[self.variable]] = None
        except KeyError: 
            raise self.VaribleNotSupported("\n\nPlease check file name.")

    def __extract_info_from_file_name(self, filename):
        era, var = [], []
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
                var.append(char)

        return ''.join(era), ''.join(var)

    # exception classes
    class VaribleNotSupported(Exception): pass

def create_files_list(directory):
    files_list = []
    with scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                files_list.append(entry.name)
    return files_list

################################ DRIVER CODE ################################
mat_files_directory = "mat_files/"
mat_file_names = create_files_list(mat_files_directory) # Comment out for testing rn
mat_file_name = r"CMIP5_historical_tasma.mat"

# use this to create multiple file reader objects
# for file_name in mat_file_names: 
#     print(file_name) # for degugging
#     era, variable = extract_info(file_name)
#     print(era, variable)

f1 = MatFileReader(mat_file_name)
print(f1.variable)