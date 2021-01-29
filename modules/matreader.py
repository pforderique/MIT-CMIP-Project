'''
Mat Reader

Piero Orderique 
28 Jan 2021

Learning how to use scipy.io lib to open and read mat files
'''
from os import scandir
from scipy.io import loadmat
from numpy import ndarray

def create_files_list(directory):
    files_list = []
    with scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                files_list.append(entry.name)
    return files_list

mat_files_directory = "mat_files/"
mat_file_names = create_files_list(mat_files_directory) # Comment out for testing rn
mat_file_name = r"CMIP5_rcp45_tasmin.mat"

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
    def __init__(self, mat_file_name, directory=mat_files_directory) -> None:

        # initialize data from just file name string
        super().__init__(mat_file_name, directory)
        self.era, self.variable = self.__extract_info_from_file_name(self.file_name)
        
        # handle HDDCDD files by asking to use a different class
        if self.era == "HDDCDD": 
            print("PLEASE USE HDDCDD READER FOR THIS FILE")
            return

        # setup rest of mat file information and attributes
        self.file = loadmat(self.path)
        self.__setup()

    def __setup(self):
        # main results variable where info is stored
        self.results = self.file["results"]

        # variable lookup: maps file name -> special field name
        self.supported_vars = {
            "pr"     : "Precip",
            "tasmax" : "Temp",
            "tasmin" : "?",          # supported, but these files don't have a sub struct?
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

        self.__read_to_gcm()


    def get_gcm_fields(self):
        res = '''GCM FIELDS:\n'''
        res += 'Ex: Use mfr.GCM_FIELDS["Temp"]["AnnualMax"] to get the 2D ndarray of values\n'
        return res + self.__get_dict_items(self.GCM_FIELDS)

    def __get_dict_items(self, d):
        res = '\n'
        for key, val in d.items():
            if isinstance(val, dict):
                res += str(key).ljust(9) + " :" + self.__get_dict_items(val)
            elif isinstance(val, ndarray) and val.ndim > 1:
                res += str(key) + " :\n" + str(val) + "\n"
            else:
                res += str(key).ljust(9) + " : " + str(val) + "\n"
        return res

    def __read_to_gcm(self):
        ''' fills in the gcm attribute with the mat file data '''

        # fills in the generic information
        for field, result in zip(self.GCM_FIELDS, self.results["GCM"][0][0][0][0]): 
            if isinstance(result[0], str) or len(result[0]) > 1:
                value = result[0]
            else:
                value = result[0][0]
            self.GCM_FIELDS[field] = value

        # overwrites that last special field with dict of its subfields 
        if self.variable in self.supported_vars: 
            self.variable = self.supported_vars[self.variable]
            
            # handles each case:
            if self.variable == "Precip":
                self.GCM_FIELDS[self.variable] = {
                    "MonthlyMean": self.results["GCM"][0][0][0][0][13][0][0][0], # 2D array
                    "AnnualMean": self.results["GCM"][0][0][0][0][13][0][0][1], # 2D array
                    "AnnualMax": self.results["GCM"][0][0][0][0][13][0][0][2], # 2D array
                    "Unit": self.results["GCM"][0][0][0][0][13][0][0][3][0], # str
                }
            elif self.variable == "Temp":
                self.GCM_FIELDS[self.variable] = {
                    "MonthlyMax": self.results["GCM"][0][0][0][0][13][0][0][0], # 2D array
                    "AnnualMax": self.results["GCM"][0][0][0][0][13][0][0][1], # 2D array
                    "Unit": self.results["GCM"][0][0][0][0][13][0][0][2][0], # str
                }
        else:
            raise self.VaribleNotSupported("\n\nPlease check file name.")

    def __extract_info_from_file_name(self, filename):
        '''Extracts the era and variable type from filename'''
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


################################ DRIVER CODE ################################

f1 = MatFileReader(mat_file_name)
print(f1.get_gcm_fields())

# use this to create multiple file reader objects
# for file_name in mat_file_names: 
#     print(file_name) # for degugging
#     era, variable = extract_info(file_name)
#     print(era, variable)