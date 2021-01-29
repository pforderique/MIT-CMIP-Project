% open mat file in program to get "results" data

% take a look at gcm's fields
gcm = results.gcm;
disp(gcm);

% get the annual maxes for each decade
annuals = gcm.AnnualMax;
disp(annuals);

% get data point by data point - 1.85000 is 1850!
annuals(1);