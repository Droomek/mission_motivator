from datetime import date
from os import name
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib import pyplot as plt
kivy.require ('1.4.0')

# calculations
start_mission_date = date(2021, 7, 24)
today = date.today()
end_mission_date = date(2022, 1, 27)

whole_mission_days = end_mission_date - start_mission_date
remaining_mission_days = end_mission_date - today
mission_days = today - start_mission_date

percent_remaning = int((remaining_mission_days.days * 100)/whole_mission_days.days)
percent_mission = int(100 - percent_remaning)

base_rate = 2.0
multiplier = 4110 / 30

earning = base_rate * multiplier * mission_days.days

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
    def mission_clicked(self, value):
        print(f"{value}")
    #     self.ids.mission_label.txt = f"{value}"
        

class Motivator(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingScreen(name='settings'))
        return sm


if __name__ == '__main__':
    Motivator().run()
