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
    mission_type = StringProperty()
    today_data = StringProperty()
    mission_day = StringProperty()
    mission_earning = StringProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.mission_type = MainScreen.m_type()
        self.today_data = f"{str(today)}"
        self.mission_day = f"{str(mission_days.days)} dzień z {str(whole_mission_days.days)} dni misji"
        self.mission_earning = "{:.2f} zł.".format(MainScreen.m_earning())

        chart = self.ids.chart
        chart.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def m_type():
        if os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM mission_data")
            items = c.fetchall()
            mission = items[0][0]
            
            conn.commit()
            conn.close()
        else:
            mission = "Wybierz misję"
        return mission

    def start_date():
        if os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM mission_data")
            items = c.fetchall()
            months_dict = {
                "Sty": 1, "Lut": 2, "Mar": 3, "Kwi": 4, "Maj": 5, "Cze": 6, 
                "Lip": 7, "Sie": 8, "Wrz": 9, "Paź": 10, "Lis": 11, "Gru": 12}
            year = int(items[0][4])
            month = months_dict[items[0][5]]
            day = int(items[0][6])
            s_date = (year, month, day)

            conn.commit()
            conn.close()
        else:
            s_date = date.today()
        return s_date
    
    def end_date():
        if os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM mission_data")
            items = c.fetchall()
            months_dict = {
                "Sty": 1, "Lut": 2, "Mar": 3, "Kwi": 4, "Maj": 5, "Cze": 6, 
                "Lip": 7, "Sie": 8, "Wrz": 9, "Paź": 10, "Lis": 11, "Gru": 12}
            year = int(items[0][7])
            month = months_dict[items[0][8]]
            day = int(items[0][9])
            e_date = (year, month, day)

            conn.commit()
            conn.close()
        else:
            e_date = date.today()
        return e_date
   
    def m_earning():
        benefit = 0
        doc_benefit = 0
        range_dict = {
            "szer.": 1.50, "st. szer.":1.55,"kpr.": 1.60,"st. kpr.": 1.65,"plut.": 1.70,
            "sierż.": 1.75,"st. sierż.": 1.80,"mł. chor.": 1.85,"chor.": 1.90,"st. chor.": 1.95,
            "st. chor. sztab.": 2.00,"ppor.": 2.10,"por.": 2.30,"kpt.": 2.70,"mjr": 3.10,
            "ppłk": 3.50,"płk": 3.80,"gen. bryg.": 5.00,"gen. dyw.": 5.50,"gen. bron.": 6.00
            }
        if os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM mission_data")
            items = c.fetchall()
            mission = items[0][0]
            range = items[0][1]
            spec = items[0][2]
            doc = items[0][3]
            
            multipiler = range_dict[range]
            
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

    def start_year_clicked(self, year):
        pass

    def start_month_clicked(self, month):
        pass

    def start_day_clicked(self, day):
        pass

    def end_year_clicked(self, year):
        pass

    def end_month_clicked(self, month):
        pass

    def end_day_clicked(self, day):
        pass
    
    def safe_clicked(self, mission, range, spec, doc, s_year, s_month, s_day, e_year, e_month, e_day):
        if not os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("""CREATE TABLE mission_data (
                    mission TEXT,
                    range TEXT,
                    specialist NUMERIC,
                    doctor NUMERIC,
                    start_year TEXT,
                    start_month TEXT,
                    start_day TEXT,
                    end_year TEXT,
                    end_month TEXT,
                    end_day TEXT
                )""")
            c.execute("INSERT INTO mission_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (mission, range, spec, doc, s_year, s_month, s_day, e_year, e_month, e_day))
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("UPDATE mission_data SET mission = ?, range = ?, specialist = ?, doctor = ?, start_year = ?, start_month = ?, start_day = ?, end_year = ?, end_month = ?, end_day = ?", (mission, range, spec, doc, s_year, s_month, s_day, e_year, e_month, e_day))
            conn.commit()
            conn.close()
        
        self.manager.screens[0].ids.mission_label.text = "{}".format(MainScreen.m_type())
        self.manager.screens[0].ids.earning_label.text = "{:.2f} zł.".format(MainScreen.m_earning())
        print(MainScreen.start_date())
        print(MainScreen.end_date())
    
    def checkbox_clicked(self, instance, value):
        pass


    def range_clicked(self, range):
        pass


class Motivator(App):
    years_list = [str(x) for x in range(2020, 2026)]
    months_list = ["Sty", "Lut", "Mar", "Kwi", "Maj", "Cze", "Lip", "Sie", "Wrz", "Paź", "Lis", "Gru"]
    days_list = [str(x) for x in range(1, 32)]
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingScreen(name='settings'))
        return sm


if __name__ == '__main__':
    Motivator().run()
