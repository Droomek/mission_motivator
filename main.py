from datetime import date
from os import name
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib import pyplot as plt
from kivy.core.window import Window
kivy.require ('1.4.0')

Window.size = (360, 640)

# calculations ---------------------------------------------------------------------------------------
start_mission_date = date(2021, 7, 24)
today = date.today()
end_mission_date = date(2022, 1, 27)

whole_mission_days = end_mission_date - start_mission_date
remaining_mission_days = end_mission_date - today
mission_days = today - start_mission_date

percent_remaning = int((remaining_mission_days.days * 100)/whole_mission_days.days)
percent_mission = int(100 - percent_remaning)

LOWEST_EARNIG = 4110
base_rate = LOWEST_EARNIG / 30
mission_multiplier = 2.0 

earning = base_rate * mission_multiplier * mission_days.days

# pie chart ----------------------------------------------------------------------------------------
khaki = (97/255, 131/255, 88/255, 1)
grey =  (.06, .06, .06, 1)

slices = [percent_mission, percent_remaning]
labels = ["", f"{percent_remaning}%"]
colors = [grey, khaki]
rmd = str(remaining_mission_days.days)

if rmd == '1':
    days = "dzień"
else:
    days = "dni"

plt.figure(facecolor= grey)
plt.title('Pozostało:', color='white', fontsize=17)

plt.pie(slices, labels=labels, textprops={'color': 'white', 'fontsize':15}, colors=colors, startangle= 90, counterclock=False, labeldistance=1.1)
centre_circle =plt.Circle((0, 0), 0.80, fc=grey)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.text(0, .1, rmd, ha='center', color='white', fontsize=18)
plt.text(0, -.3, days, ha='center', color='white', fontsize=15)

# kivy bulider ------------------------------------------------------------------------------------------
Builder.load_file('motivator.kv')

# Main screen -------------------------------------------------------------------------------------------
class MainScreen(Screen):
    today_data = StringProperty()
    mission_day = StringProperty()
    mission_earning = StringProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.today_data = f"{str(today)}"
        self.mission_day = f"{str(mission_days.days)} dzień z {str(whole_mission_days.days)} dni misji"
        self.mission_earning = "{:.2f} zł".format(earning)

        chart = self.ids.chart
        chart.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    

# SettingScreen -----------------------------------------------------------------------------------------
class SettingScreen(Screen):
    pass
    def mission_clicked(self, mission):
        if mission == "PKW EUTM RCA" or mission == "PKW Irak" or mission == "PKW IRINI":
            self.benefit = (LOWEST_EARNIG * 0.70) / 30
        else:
            self.benefit = 0
        print (self.benefit)
    def range_clicked(self, range):
        multipiler = [1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00, 2.10, 2.30, 2.70, 3.10, 3.50, 3.80, 5.00, 5.50, 6.00]
        if range == "szer.":
            self.multipiler = multipiler[0]
        elif range == "st. szer.":
            self.multipiler  = multipiler[1]
        elif range == "kpr.":
            self.multipiler = multipiler[2]
        elif range == "st. kpr.":
            self.multipiler = multipiler[3]
        elif range == "plut.":
            self.multipiler = multipiler[4]
        elif range == "sierż.":
            self.multipiler = multipiler[5]
        elif range == "st. sierż.":
            self.multipiler = multipiler[6]
        elif range == "mł. chor.":
            self.multipiler = multipiler[7]
        elif range == "chor.":
            self.multipiler = multipiler[8]
        elif range == "st. chor.":
            self.multipiler = multipiler[9]
        elif range == "st. chor. sztab.":
            self.multipiler = multipiler[10]
        elif range == "ppor.":
            self.multipiler = multipiler[11]
        elif range == "por.":
            self.multipiler = multipiler[12]
        elif range == "kpt.":
            self.multipiler = multipiler[13]
        elif range == "mjr":
            self.multipiler = multipiler[14]
        elif range == "ppłk":
            self.multipiler = multipiler[15]
        elif range == "płk":
            self.multipiler = multipiler[16]
        elif range == "gen. bryg.":
            self.multipiler = multipiler[17]
        elif range == "gen. dyw.":
            self.multipiler = multipiler[18]
        else:
            self.multipiler = multipiler[19]
        print ((self.multipiler * base_rate * mission_days.days) + (mission_days.days * self.benefit))


class Motivator(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingScreen(name='settings'))
        return sm


if __name__ == '__main__':
    Motivator().run()
