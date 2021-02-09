'''
User class for Mat File Reader and Plotter classes

Piero Orderique
04 Feb 2021

USER OPTIONS MANUAL
'''
from modules import create_files_list
from modules import matreader as mfr
from modules import plotter as pltr

############# INPUT INFORMATION ##############

# * INPUT: specify directory of mat files *
mat_files_directory = mfr.mat_files_directory

# * INPUT: specify filename of mat file *
mat_file = "CMIP5_historical_tasmax.mat"

# * INPUT: specify index (see show all models before changing) for gcm
gcm_index = 16

###### HOW TO: GET MAT FILE INFORMATION ######

# ? Show all the mat files in the mat file directory ?
def show_all_mat_files():
    all_mat_files = create_files_list(mat_files_directory)
    for matfile in all_mat_files:
        print(matfile)

# ? Show all the models in the file and their index values ?
def show_all_models():
    fr = mfr.MatDocumentReader(mat_file)
    print(fr.model_options())

# ? Show info summary for the mat file (specify model using index!) ?
def show_gcm_fields(index=gcm_index):
    fr = mfr.FileReader.create_file_reader(mat_file, index=index)
    print(fr.info())

########### HOW TO: PLOT MAT FILES ###########

# ? Create a plotter for the file and plot one of its fields
def plot_monthly():
    fr = mfr.FileReader.create_file_reader(mat_file, index=gcm_index)
    plotter = pltr.MatPlotter.create_plotter(fr)
    plotter.plot_monthly().show() 

# ? Each class has specific plot methods. Refer to plotter.py in modules
# ?     for more information on what attributes you can plot
def plot_precip_example():
    mat_file = "CMIP5_historical_pr.mat"
    fr = mfr.FileReader.create_file_reader(mat_file, index=3)

    plotter = pltr.MatPlotterPrecip(fr)
    plotter.plot_all().show() 

if __name__ == "__main__":
    '''your code here'''
    # show_all_models()
    # show_gcm_fields()
    plot_monthly()

    # plot_precip_example()