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

def sequence_decades(monthlymax):
    ''' returns a list of sequences for each decade that contains data for boxplot '''
    decades = monthlymax[:,0] # 12 data points each decade
    temps = monthlymax[:,2]

    sequences = []
    for dec in range(0, len(monthlymax), 12): # every 12 months
        sequences.append(temps[dec:dec+12])

    return sequences

class MatPlotterTemp():
    def __init__(self, mfr:MatFileReader) -> None:
        # set up plotter variables 
        self.mfr = mfr
        self.plottables = mfr.GCM_FIELDS[mfr.variable]
        self.annualmax = self.plottables["AnnualMax"]
        self.monthlymax = self.plottables["MonthlyMax"]
        self.decades_list = annualmax[:,0]

        # plt features
        self.BAR_WIDTH = 5
        plt.figure(figsize=(10,4))

    def plot_annual(self):
        temps = annualmax[:,1]

        plt.title("Annual Max Temperature")
        plt.xlabel("Year")
        plt.ylabel("Temp " + f'({self.plottables["Unit"]})')
        plt.bar(self.decades_list, temps, width=self.BAR_WIDTH)
        plt.show()

# plot_monthly()
decade_sequences = sequence_decades(monthlymax)
decades = annualmax[:,0]

# plt.figure(figsize=(10,4))
# plt.ylim(0, 55)
# plt.boxplot(decade_sequences, positions=[int(year) for year in decades], widths=5)
# plt.show()

plotter = MatPlotterTemp(mfr)
plotter.plot_annual()
