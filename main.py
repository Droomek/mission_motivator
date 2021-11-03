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

# calculations
start_mission_date = date(2021, 7, 24)
today = date.today()
end_mission_date = date(2022, 1, 27)

whole_mission_days = end_mission_date - start_mission_date
remaining_mission_days = end_mission_date - today
mission_days = today - start_mission_date

percent_remaning = int((remaining_mission_days.days * 100)/whole_mission_days.days)
percent_mission = int(100 - percent_remaning)

base_rate = 4110 / 30
mission_multiplier = 2.0 

earning = base_rate * mission_multiplier * mission_days.days

# pie chart
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

# kivy bulider
Builder.load_file('motivator.kv')


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
    


# SettingScreen
class SettingScreen(Screen):
    pass
    def mission_clicked(self, mission):
        print(f"{mission}")
    def range_clicked(self, range):
        multipiler = [1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00, 2.10, 2.30, 2.70, 3.10, 3.50, 3.80, 5.00, 5.50, 6.00]
        if range == "szer.":
            print(multipiler[0] * base_rate * mission_days.days)
        elif range == "st. szer.":
            print(multipiler[1] * base_rate * mission_days.days)
        elif range == "kpr.":
            print(multipiler[2] * base_rate * mission_days.days)
        elif range == "st. kpr.":
            print(multipiler[3] * base_rate * mission_days.days)
        elif range == "plut.":
            print(multipiler[4] * base_rate * mission_days.days)
        elif range == "sierż.":
            print(multipiler[5] * base_rate * mission_days.days)
        elif range == "st. sierż.":
            print(multipiler[6] * base_rate * mission_days.days)
        elif range == "mł. chor.":
            print(multipiler[7] * base_rate * mission_days.days)
        elif range == "chor.":
            print(multipiler[8] * base_rate * mission_days.days)
        elif range == "st. chor.":
            print(multipiler[9] * base_rate * mission_days.days)
        elif range == "st. chor. sztab.":
            print(multipiler[10] * base_rate * mission_days.days)
        elif range == "ppor.":
            print(multipiler[11] * base_rate * mission_days.days)
        elif range == "por.":
            print(multipiler[12] * base_rate * mission_days.days)
        elif range == "kpt.":
            print(multipiler[13] * base_rate * mission_days.days)
        elif range == "mjr":
            print(multipiler[14] * base_rate * mission_days.days)
        elif range == "ppłk":
            print(multipiler[15] * base_rate * mission_days.days)
        elif range == "płk":
            print(multipiler[16] * base_rate * mission_days.days)
        elif range == "gen. bryg.":
            print(multipiler[17] * base_rate * mission_days.days)
        elif range == "gen. dyw.":
            print(multipiler[18] * base_rate * mission_days.days)
        else:
            print(multipiler[19] * base_rate * mission_days.days)


class Motivator(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingScreen(name='settings'))
        return sm


if __name__ == '__main__':
    Motivator().run()
