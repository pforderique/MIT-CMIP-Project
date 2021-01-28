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

mat_files_directory = "mat_files/"
# mat_files = create_files_list(mat_files_directory)

##############################################################################
# testing 
##############################################################################
filename = r"mat_files\CMIP5_historical_tasmax.mat"
file = loadmat(filename)

results = file["results"]
results_struct = {
    "rra": results["Era"][0][0][0],
    "variable": results["Variable"][0][0][0],
    "big_data": results["GCM"][0][0][0][0][13][0][0][0],
    "temps_by_date": results["GCM"][0][0][0][0][13][0][0][1]
}

print(results["GCM"][0][0][0][0][13][0][0][1])