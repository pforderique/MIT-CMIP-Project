'''
Testing

Piero Orderique
28 Jan 2021

Testing the mat file structure.
Purpose: to help design file reader class in matreader.py
'''
from os import scandir
from matplotlib import pyplot as plt
from matreader import MatFileReader, mat_files_directory

def create_files_list(directory):
    files_list = []
    with scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                files_list.append(entry.name)
    return files_list

mat_file_names = create_files_list(mat_files_directory) 
mat_file_name = r"CMIP5_rcp45_tasmax.mat"

################################ DRIVER CODE ################################
mfr = MatFileReader(mat_file_name)

annualmax = mfr.GCM_FIELDS["Temp"]["AnnualMax"] # len = 16 (# of decades captured)
monthlymax = mfr.GCM_FIELDS["Temp"]["MonthlyMax"] # len = 192 (16 * 12 months in a year)

def plot_annual():
    decades = annualmax[:,0] # remember, matlab idxing starts at 1!
    temps = annualmax[:,1]

def plot_monthly():
    decades = monthlymax[:,0] # 12 data points each decade
    temps = monthlymax[:,2]

    plt.title("Matplotlib demo") 
    plt.xlabel("x axis caption") 
    plt.ylabel("y axis caption") 
    plt.plot(decades, temps, 'bo')
    plt.show()

# plot_monthly()

# plt.figure(figsize=(10,4))
# plt.ylim(0, 55)
# plt.boxplot(decade_sequences, positions=[int(year) for year in decades], widths=5)
# plt.show()