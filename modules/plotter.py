import matplotlib.pyplot as plt
from matreader import MatFileReader

class MatPlotterTemp():
    def __init__(self, mfr) -> None:
        # set up plotter variables 
        self.mfr = mfr
        self.plottables = mfr.GCM_FIELDS[mfr.variable]
        self.annualmax = self.plottables["AnnualMax"]
        self.monthlymax = self.plottables["MonthlyMax"]
        self.decades_list = self.annualmax[:,0]

        # plt features
        self.BAR_WIDTH = 5
        self.BAR_COLOR = "orange"
        plt.figure(figsize=(10,4))

    def plot_annual(self):
        temps =self.annualmax[:,1]
        plt.title("Annual Max Temperature")
        plt.xlabel("Year")
        plt.ylabel("Temp " + f'({self.plottables["Unit"]})')
        plt.bar(self.decades_list, temps, color=self.BAR_COLOR, width=self.BAR_WIDTH)
        plt.show()

    def plot_monthly(self):
        decade_temps = self._sequence_decades(self.monthlymax)
        plt.ylim(0, 55)
        plt.title("Monthly Max by Decade")
        plt.xlabel("Year")
        plt.ylabel("Temp " + f'({self.plottables["Unit"]})')
        plt.boxplot(
            decade_temps, 
            positions=[int(year) for year in self.decades_list], 
            widths=self.BAR_WIDTH
        )
        plt.show()

    def _sequence_decades(self, monthlymax):
        ''' returns a list of sequences for each decade that contains data for boxplot '''
        decades = monthlymax[:,0] # 12 data points each decade
        temps = monthlymax[:,2]

        sequences = []
        for dec in range(0, len(monthlymax), 12): # every 12 months
            sequences.append(temps[dec:dec+12])

        return sequences

###################### TESTING #######################
mat_file_name = r"CMIP5_rcp85_tasmax.mat"
mfr = MatFileReader(mat_file_name)

plotter = MatPlotterTemp(mfr)
plotter.plot_monthly()
