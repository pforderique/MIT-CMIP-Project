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
    "Gcm": { # results["Gcm"]
        # "Temp":
        "MonthlyMax": results["GCM"][0][0][0][0][13][0][0][0], # 2D array
        "AnnualMax": results["GCM"][0][0][0][0][13][0][0][1], # 2D array
        "Unit": results["GCM"][0][0][0][0][13][0][0][2], # str
    }
}

GCM_FIELDS = {
    'File': None,
    'Lat': None,
    'Lon': None,
    'IdxLat': None,
    'IdxLon': None,
    'Values': None,
    'Calendar': None,
    'Unit': None,
    'Years': None,
    'StartYear': None,
    'EndYear': None,
    'Months': None,
    'Trim': None,
    'Temp': None,
}

# gets all strings in this gcm structure
for field, result in zip(GCM_FIELDS, results["GCM"][0][0][0][0]): 
    console_string = "-"*30 + "\n"
    if not isinstance(result[0], str):
        value = str(result[0][0])
    else:
        value = str(result[0])
    GCM_FIELDS[field] = value
    print(console_string + value)

for key, val in GCM_FIELDS.items():
    print(key, ":", val)