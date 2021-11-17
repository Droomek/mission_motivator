from datetime import date
import os
import sqlite3
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
        earning = MainScreen.m_earning()
        self.mission_earning = "{:.2f} zł.".format(earning)

        chart = self.ids.chart
        chart.add_widget(FigureCanvasKivyAgg(plt.gcf()))
      
   
    def m_earning():
        benefit = 0
        doc_benefit = 0
        multipiler_list = [1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00, 2.10, 2.30, 2.70, 3.10, 3.50, 3.80, 5.00, 5.50, 6.00]
        if os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM mission_data")
            items = c.fetchall()
            for m_mission, m_range, m_spec, m_doc in items:
                mission = m_mission
                range = m_range
                spec = m_spec
                doc = m_doc
            
            if range == "szer.":
                multipiler = multipiler_list[0]
            elif range == "st. szer.":
                multipiler  = multipiler_list[1]
            elif range == "kpr.":
                multipiler = multipiler_list[2]
            elif range == "st. kpr.":
                multipiler = multipiler_list[3]
            elif range == "plut.":
                multipiler = multipiler_list[4]
            elif range == "sierż.":
                multipiler = multipiler_list[5]
            elif range == "st. sierż.":
                multipiler = multipiler_list[6]
            elif range == "mł. chor.":
                multipiler = multipiler_list[7]
            elif range == "chor.":
                multipiler = multipiler_list[8]
            elif range == "st. chor.":
                multipiler = multipiler_list[9]
            elif range == "st. chor. sztab.":
                multipiler = multipiler_list[10]
            elif range == "ppor.":
                multipiler = multipiler_list[11]
            elif range == "por.":
                multipiler = multipiler_list[12]
            elif range == "kpt.":
                multipiler = multipiler_list[13]
            elif range == "mjr":
                multipiler = multipiler_list[14]
            elif range == "ppłk":
                multipiler = multipiler_list[15]
            elif range == "płk":
                multipiler = multipiler_list[16]
            elif range == "gen. bryg.":
                multipiler = multipiler_list[17]
            elif range == "gen. dyw.":
                multipiler = multipiler_list[18]
            else:
                multipiler = multipiler_list[19]
            
            if mission == "PKW EUTM RCA" or mission == "PKW Irak" or mission == "PKW IRINI":
                benefit = ((LOWEST_EARNIG * 0.70) / 30) * mission_days.days
            else:
                benefit = 0
            
            if spec == 1:
                doc_benefit = ((LOWEST_EARNIG * 2.5) / 30) * mission_days.days
            elif doc == 1: 
                doc_benefit = ((LOWEST_EARNIG * 1.5) / 30) * mission_days.days
            else:
                doc_benefit = 0

            earning = ((LOWEST_EARNIG / 30) * multipiler * mission_days.days) + benefit + doc_benefit

            conn.commit()
            conn.close()
        else:
            earning = 0

        return earning


# SettingScreen -----------------------------------------------------------------------------------------
class SettingScreen(Screen):
    
    def mission_clicked(self, mission):
        pass
    
    def safe_clicked(self, mission, range, spec, doc):
        if not os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("""CREATE TABLE mission_data (
                    mission TEXT,
                    range TEXT,
                    specialist NUMERIC,
                    doctor NUMERIC
                )""")
            c.execute("INSERT INTO mission_data VALUES (?, ?, ?, ?)", (mission, range, spec, doc) )
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("UPDATE mission_data SET mission = ?, range = ?, specialist = ?, doctor = ?", (mission, range, spec, doc) )
            conn.commit()
            conn.close()
        
        self.manager.screens[0].ids.earning_label.text = "{:.2f} zł.".format(MainScreen.m_earning())
        print("{:.2f} zł".format(MainScreen.m_earning()))

    
    def checkbox_clicked(self, instance, value):
        pass


    def range_clicked(self, range):
        pass
        

class Motivator(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingScreen(name='settings'))
        return sm


if __name__ == '__main__':
    Motivator().run()
