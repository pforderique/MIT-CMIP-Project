'''
Plotter

Piero Orderique 
30 Jan 2021

Plotter classes take in MatFileReaders and plot relevant info
'''

import matplotlib.pyplot as plt

# I keep having to change figsize bc of different resolution screens
# *change back fig size to (10,4) on main comp.
FIGSIZE1 = (10,4)
FIGSIZE2 = (7,8)

# OOD Factory Method:
class MatPlotter():
    def __init__(self, mfr) -> None:
        # set up plotter variables 
        self.mfr = mfr
        self.mfr_info = f"({self.mfr.model}, {self.mfr.variable}, {self.mfr.era})"
        self.plottables = mfr.GCM_FIELDS[mfr.variable]

        # plt features
        self.BOX_WIDTH = 5
        self.PT_COLOR = "orange"
        self.BG_COLOR = "darkblue"
        plt.figure(figsize=FIGSIZE1)
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
        elif mfr.variable == "HDDCDD":
            return HDDCDDPlotter(mfr=mfr)
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
        plt.title("Annual Max Temperature " + self.mfr_info)
        plt.plot(self.decades_list, temps, 'o', color=self.PT_COLOR)
        return self

    def plot_monthly(self):
        super().plot_monthly()
        plt.ylim(0, 55)
        plt.title(f"Monthly Max by Decade " + self.mfr_info)
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
        fig, ax1 = plt.subplots(1, 1, figsize=FIGSIZE1)

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

# special HDDCDD mat files
class HDDCDDPlotter():
    def __init__(self, mfr) -> None:
        # set up plotter variables 
        self.mfr = mfr
        self.plottables = mfr.GCM_FIELDS
        self.months = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]

        # plt features
        self.BOX_WIDTH = 0.5
        self.PT_COLOR = "orange"
        self.BG_COLOR = "darkblue"
        plt.figure(figsize=FIGSIZE2)
        plt.xlabel("Month")
        plt.ylabel(mfr.variable + " " + f'({self.plottables["Unit"]})')

    def show(self):
        plt.show()

    def plot_HDD_monthly(self):
        monthly_temps = self._sequence_data(self.plottables["HDDMonthlyMean"])
        plt.title(
            f"{self.plottables['Name']}\n" +
            f"HDD, By Month ({self.plottables['StartYear']}-{self.plottables['EndYear']})"
        )
        plt.ylim(0, 1500)
        plt.ylabel(f"Unit: {self.plottables['Unit']}")
        plt.boxplot(
            monthly_temps, 
            labels=self.months, 
            widths=self.BOX_WIDTH,
        )
        return self

    def plot_CDD_monthly(self):
        monthly_temps = self._sequence_data(self.plottables["CDDMonthlyMean"])
        plt.title(
            f"{self.plottables['Name']}\n" +
            f"CDD, By Month ({self.plottables['StartYear']}-{self.plottables['EndYear']})"
        )
        plt.ylim(0, 800)
        plt.ylabel(f"Unit: {self.plottables['Unit']}")
        plt.boxplot(
            monthly_temps, 
            labels=self.months, 
            widths=self.BOX_WIDTH,
        )
        return self

    def plot_monthly(self):
        ''' plot both HDD monthly and CDD monthly side by side ''' 
        # override all the plt data we just made my closing that window
        plt.close()

        # create subplot
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle(self.plottables["Name"])
        fig.set_size_inches(11.5, 7)

        # plot HDD monthly mean
        color = 'tab:blue'
        monthly_temps = self._sequence_data(self.plottables["HDDMonthlyMean"])
        ax1.set_title(f"HDD, By Month ({self.plottables['StartYear']}-{self.plottables['EndYear']})")
        ax1.set_ylim(0, 1500)
        ax1.boxplot(
            monthly_temps,
            labels=self.months,
            widths=self.BOX_WIDTH
        )
        ax1.tick_params(axis='x', labelcolor=color)
        ax1.tick_params(axis='y', labelcolor=color)

        # plot CDD monthly mean next to it
        color = 'tab:orange'
        monthly_temps = self._sequence_data(self.plottables["CDDMonthlyMean"])
        ax2.set_title(f"CDD, By Month ({self.plottables['StartYear']}-{self.plottables['EndYear']})")
        ax2.set_ylim(0, 800)
        ax2.boxplot(
            monthly_temps,
            labels=self.months,
            widths=self.BOX_WIDTH,
        )
        ax2.tick_params(axis='x', labelcolor=color)
        ax2.tick_params(axis='y', labelcolor=color)

        return self

    def _sequence_data(self, monthlyarray):
        ''' returns list of months with of lists containing yearly means of data '''
        res = []
        for idx in range(len(monthlyarray)):
            month = monthlyarray[idx]
            res.append(list(month))
        return res

###################### TESTING #######################
# if __name__ == "__main__":
#     mat_file_name = r"CMIP5_rcp85_HDDCDD.mat"
#     fr = FileReader.create_file_reader(mat_file_name, index=4)
#     # print(hfr.get_gcm_fields())

#     plotter = MatPlotter.create_plotter(fr)
#     plotter.plot_monthly().show() 