import matplotlib.pyplot as plt
from matreader import MatFileReader

# OOD Factory Method:
class MatPlotter():
    def __init__(self, mfr) -> None:
        # set up plotter variables 
        self.mfr = mfr
        self.plottables = mfr.GCM_FIELDS[mfr.variable]

        # plt features
        self.BAR_WIDTH = 5
        self.BAR_COLOR = "orange"
        self.BG_COLOR = "darkblue"
        plt.figure(figsize=(5,2))

    def show(self):
        plt.show()

    def plot_monthly(self):
        decade_temps = self._sequence_decades(self.monthly)
        plt.xlabel("Year")
        plt.ylabel(mfr.variable + " " + f'({self.plottables["Unit"]})')
        plt.boxplot(
            decade_temps, 
            positions=[int(year) for year in self.decades_list], 
            widths=self.BAR_WIDTH,
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
        plt.xlabel("Year")
        plt.ylabel("Temp " + f'({self.plottables["Unit"]})')
        plt.plot(self.decades_list, temps, 'o', color=self.BAR_COLOR)
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


###################### TESTING #######################
mat_file_name = r"CMIP5_rcp85_tasmax.mat"
mfr = MatFileReader(mat_file_name)

plotter = MatPlotter.create_plotter(mfr)
# plotter.plot_all().show()

plotter.plot_monthly().show()

# TODO: change back fig size to (10,4) on main comp.