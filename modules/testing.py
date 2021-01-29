'''
Testing

Piero Orderique
28 Jan 2021

Testing the mat file structure.
Purpose: to help design file reader class in matreader.py
'''
from os import scandir
from matreader import MatFileReader, mat_files_directory

def create_files_list(directory):
    files_list = []
    with scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                files_list.append(entry.name)
    return files_list

mat_file_names = create_files_list(mat_files_directory) 
mat_file_name = r"CMIP5_historical_tasmax.mat"

################################ DRIVER CODE ################################
mfr = MatFileReader(mat_file_name)

annualmax = mfr.GCM_FIELDS["Temp"]["AnnualMax"]
decades = annualmax[:,0]
temps = annualmax[:,1]

print(decades, temps)
