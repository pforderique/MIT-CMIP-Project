import matplotlib.pyplot as plt
from matreader import MatFileReader

# OOD Factory Method:
class MatPlotter():
    def __init__(self, mfr) -> None:
        # set up plotter variables 
        self.mfr = mfr
        self.plottables = mfr.GCM_FIELDS[mfr.variable]

        # plt features
        self.BOX_WIDTH = 5
        self.PT_COLOR = "orange"
        self.BG_COLOR = "darkblue"
        plt.figure(figsize=(5,2))
        plt.xlabel("Year")
        plt.ylabel(mfr.variable + " " + f'({self.plottables["Unit"]})')

    def show(self):
        plt.show()

    def plot_monthly(self):
        decade_temps = self._sequence_decades(self.monthly)
        plt.boxplot(
            decade_temps, 
            positions=[int(year) for year in self.decades_list], 
            widths=self.BOX_WIDTH,
        )

    def _sequence_decades(self, monthlydata):
        ''' returns a list of sequences for each decade that contains data for boxplot '''
        decades = monthlydata[:,0] # 12 data points each decade
        temps = monthlydata[:,2]

        sequences = []
        for dec in range(0, len(monthlydata), 12): # every 12 months
            sequences.append(temps[dec:dec+12])

        return sequences

    @staticmethod
    def create_plotter(mfr):
        if mfr.variable == "Temp": 
            return MatPlotterTemp(mfr=mfr)
        elif mfr.variable == "Precip":
            return MatPlotterPrecip(mfr=mfr)
        else:
            raise NotImplementedError("PLOTTER DOES NOT SUPPORT " + mfr.variable)

class MatPlotterTemp(MatPlotter):
    def __init__(self, mfr) -> None:
        # set up plotter variables 
        super().__init__(mfr=mfr)
        self.annualmax = self.plottables["AnnualMax"]
        self.monthly = self.plottables["MonthlyMax"]
        self.decades_list = self.annualmax[:,0]

    def plot_annual(self):
        temps = self.annualmax[:,1]
        plt.title("Annual Max Temperature")
        plt.plot(self.decades_list, temps, 'o', color=self.PT_COLOR)
        return self

    def plot_monthly(self):
        super().plot_monthly()
        plt.ylim(0, 55)
        plt.title("Monthly Max by Decade")
        return self

    def plot_all(self):
        self.plot_annual().plot_monthly()
        return self

class MatPlotterPrecip(MatPlotter):
    def __init__(self, mfr) -> None:
        # set up plotter variables 
        super().__init__(mfr=mfr)
        self.monthly = self.plottables["MonthlyMean"]
        self.annualmean = self.plottables["AnnualMean"]
        self.annualmax = self.plottables["AnnualMax"]
        self.decades_list = self.annualmax[:,0]

    def plot_monthly(self):
        super().plot_monthly()
        plt.ylim(0, 4)
        plt.title("Monthly Mean by Decade")
        return self 

    def plot_annual(self, type="mean"):
        if type == "mean":
            temps = self.annualmean[:,1]
            plt.title("Annual Mean Precipitation")
        elif type == "max":
            temps = self.annualmax[:,1]
            plt.title("Annual Max Precipitation")
        else: 
            raise AttributeError("Please select either 'mean' or 'max'.")
        plt.ylim(0, 4)
        plt.plot(self.decades_list, temps, '-',  color=self.PT_COLOR)
        return self

    def plot_all(self):
        # override all the plt data we just made my closing that window
        plt.close()
        
        # create subplots for multiple plots in one
        fig, ax1 = plt.subplots(1, 1, figsize=(5,2))

        # first plot the monthly mean
        self.plot_monthly()
        plt.title("Precipitation Over the Decades")
        ax1.set_xlabel('Year')
        ax1.set_ylabel(
            'Monthly Mean Precip ' + f'({self.plottables["Unit"]})' + " By Decade",
        )

        # now plot the annual mean
        color = 'tab:cyan'
        temps = self.annualmean[:,1][:] # copy to avoid changing data
        ax1.set_ylim(0, 4)
        ax1.plot(self.decades_list, temps, 'o', color=color, label="Annual Mean")
        ax1.tick_params(axis='y', labelcolor=color)

        # make a second axis that shares x-axis with ax1
        ax2 = ax1.twinx()

        # now plot the annual max
        temps = self.annualmax[:,1][:] # copy to avoid changing data
        color = 'darkorange'
        ax2.set_ylabel(
            'Annual Max Precip ' + f'({self.plottables["Unit"]})',
            color=color,
        )
        ax2.set_ylim(0, 150)
        ax2.plot(self.decades_list, temps, 'o', color=color, label="Annual Max")
        ax2.tick_params(axis='y', labelcolor=color)

        # add a legend
        ax1.legend(loc="upper left")
        ax2.legend()

        return self

###################### TESTING #######################
mat_file_name = r"CMIP5_rcp85_pr.mat"
mfr = MatFileReader(mat_file_name)

plotter = MatPlotter.create_plotter(mfr)
# plotter.plot_all().show()

plotter.plot_all().show()

# TODO: change back fig size to (10,4) on main comp.