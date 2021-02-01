'''
Mat Reader

Piero Orderique 
28 Jan 2021

Mat File Reader class to help access and format the GCM data contained in several mat files
'''
from scipy.io import loadmat
from numpy import ndarray

mat_files_directory = "mat_files/"

class FileReader():
    def __init__(self, filename, directory="") -> None:
        self.path = directory + filename
        self.file_name = filename
        self.extension = filename[filename.find("."):] # caution! error if '.' in name
        self._SCREEN_WIDTH = 40

    def get_file_info(self):
        ''' Return information on file path, extension, and name '''
        res = "FILE INFO".center(self._SCREEN_WIDTH, "*")
        return res + f"\nFile: {self.file_name}\nExtension: {self.extension}\nPath: {self.path}\n"

    def get_path(self):
        return self.path

    def get_file_name(self):
        return self.file_name

    def get_extension(self):
        return self.extension

    # for mat files / HDDCDD subtype files only
    def _extract_info_from_file_name(self, filename):
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

class MatFileReader(FileReader):
    def __init__(self, mat_file_name, directory=mat_files_directory) -> None:
        # initialize data from just file name string
        super().__init__(mat_file_name, directory)
        self.era, self.variable = self._extract_info_from_file_name(self.file_name)

        # setup rest of mat file information and attributes
        self.file = loadmat(self.path)
        self._setup()

    def _setup(self):
        # handle HDDCDD files by asking to use a different class
        if self.variable == "HDDCDD": 
            raise TypeError(
                "\n" + '*' * self._SCREEN_WIDTH + 
                "\nPLEASE USE HDDCDD READER FOR THIS FILE\n" + 
                '*' * self._SCREEN_WIDTH
            )

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

        self._read_to_gcm()

    def info(self):
        ''' Return important, stored information in the file including the GCM '''
        return self.get_file_info() + "\n" + self.get_results() + "\n" + self.get_gcm_fields()

    def get_results(self):
        ''' return a summary of the results field '''
        res = "RESULTS".center(self._SCREEN_WIDTH,"*")
        return res + f"\nEra: {self.era}\nVariable: {self.variable}\nGCM: ({len(self.GCM_FIELDS)} fields)\n"

    def get_gcm_fields(self):
        res = "GCM FIELDS".center(self._SCREEN_WIDTH, "*")
        res += '\nEx: Use mfr.GCM_FIELDS["Temp"]["AnnualMax"] to get the 2D ndarray of values\n'
        return res + self._get_dict_items(self.GCM_FIELDS)

    def _get_dict_items(self, d):
        ''' returns 1 str of formatted items in a dictionary'''
        res = '\n'
        LEFTSPACE = 9
        for key, val in d.items():
            if isinstance(val, dict):
                res += str(key).ljust(LEFTSPACE) + " :" + self._get_dict_items(val)
            elif isinstance(val, ndarray) and val.ndim > 1:
                res += str(key) + " :\n" + str(val) + "\n"
            else:
                res += str(key).ljust(LEFTSPACE) + " : " + str(val) + "\n"
        return res

    def _read_to_gcm(self):
        ''' fills in the gcm attribute with the mat file data '''

        # fills in the generic information
        for field, result in zip(self.GCM_FIELDS, self.results["GCM"][0][0][0][0]): 
            if isinstance(result[0], str) or len(result[0]) > 1:
                value = result[0]
            else:
                value = result[0][0]
            self.GCM_FIELDS[field] = value

        self._read_in_special_fields()

    def _read_in_special_fields(self):
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
            raise self.VariableNotSupported(
                "\n\nPlease check file name. Unsupported varaible: " + self.variable
            )

    # exception classes
    class VariableNotSupported(Exception): pass

class HDDCDDReader(MatFileReader): 
    def __init__(self, mat_file_name, directory=mat_files_directory) -> None:     
        super().__init__(mat_file_name, directory)

    def _setup(self):
        # main results variable where info is stored
        self.results = self.file["results"]

        # initialize GCM_fields
        self.GCM_FIELDS = {
            'Name'          : None,
            'HDD'           : None,
            'CDD'           : None,
            'StartYear'     : None,
            'EndYear'       : None,
            'Unit'          : None,
            'HDDMonthlyMean': None,
            'CDDMonthlyMean': None,
            'Decades'       : None,
        }

        self._read_to_gcm()

    def _read_in_special_fields(self):
        # override this method from parent. No special subfields that require dicts
        pass
