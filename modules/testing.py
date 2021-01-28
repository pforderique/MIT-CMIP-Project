'''
Testing

Piero Orderique
28 Jan 2021

Testing the mat file structure.
Purpose: to help design file reader class in matreader.py
'''

from scipy.io import loadmat

#############################################################
# testing 
#############################################################

filename = r"mat_files\CMIP5_historical_tasmax.mat"
file = loadmat(filename)

results = file["results"]
results_struct = {
    "Era": results["Era"][0][0][0], # str
    "Variable": results["Variable"][0][0][0], # str
    "Gcm": {
        # "Temp":
        "MonthlyMax": results["GCM"][0][0][0][0][13][0][0][0], # 2D array
        "AnnualMax": results["GCM"][0][0][0][0][13][0][0][1], # 2D array
        "Unit": results["GCM"][0][0][0][0][13][0][0][2], # str
    }
}


print(results["GCM"][0][0][0][0][13][0][0])