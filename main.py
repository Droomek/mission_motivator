import os
import sqlite3
import kivy
from datetime import date, datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib import pyplot as plt
from kivy.core.window import Window
kivy.require ('1.4.0')

Window.size = (360, 640)

LOWEST_EARNING = 4110
MONTHS_DICT = {
    "Sty": 1, "Lut": 2, "Mar": 3, "Kwi": 4, "Maj": 5, "Cze": 6, 
    "Lip": 7, "Sie": 8, "Wrz": 9, "Paź": 10, "Lis": 11, "Gru": 12}

RANGE_DICT = {
    "szer.": 1.50, "st. szer.":1.55,"kpr.": 1.60,"st. kpr.": 1.65,"plut.": 1.70,
    "sierż.": 1.75,"st. sierż.": 1.80,"mł. chor.": 1.85,"chor.": 1.90,"st. chor.": 1.95,
    "st. chor. sztab.": 2.00,"ppor.": 2.10,"por.": 2.30,"kpt.": 2.70,"mjr": 3.10,
    "ppłk": 3.50,"płk": 3.80,"gen. bryg.": 5.00,"gen. dyw.": 5.50,"gen. bron.": 6.00
    }

# calculations ------------------------------------------------------------------------------------------

class MissionCalculations(ScreenManager):
    
    def start_date():
        if os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM mission_data")
            items = c.fetchall()
            s_date = datetime.strptime(items[0][4], '%Y-%m-%d').date()
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
            e_date = datetime.strptime(items[0][5], '%Y-%m-%d').date()
            conn.close()
        else:
             e_date = date.today()
        return e_date
    
    def whole_days():
        whole = MissionCalculations.end_date() - MissionCalculations.start_date()
        all_days = int(whole.days)
        if all_days > 0:
            return all_days
        else:
            return -1
    
    def remaning_days():
        rem_days = MissionCalculations.end_date() - date.today()
        r_days = int(rem_days.days)
        if r_days > 0:
            return  r_days
        else:
            return -1
    
    def mission_day():
        mis_day = date.today() - MissionCalculations.start_date()
        m_days = int(mis_day.days)
        if m_days > 0:
            return  m_days
        else:
            return -1
    
    def get_mission_days_out():
        if os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM mission_data")
            items = c.fetchall()
            days = items[0][6]
            conn.close()
        else:
            days = "0"
        return days

    def m_earning():
        benefit = 0
        doc_benefit = 0
        if os.path.isfile('mission_data.db'):
            conn = sqlite3.connect('mission_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM mission_data")
            items = c.fetchall()
            mission = items[0][0]
            range = items[0][1]
            spec = items[0][2]
            doc = items[0][3]
            
            multipiler = RANGE_DICT[range]
            
            if mission == "PKW EUTM RCA" or mission == "PKW Irak" or mission == "PKW IRINI":
                benefit = ((LOWEST_EARNING * 0.70) / 30) * MissionCalculations.mission_day()
            else:
                benefit = 0
            
            if spec == 1:
                doc_benefit = ((LOWEST_EARNING * 2.5) / 30) * MissionCalculations.mission_day()
            elif doc == 1: 
                doc_benefit = ((LOWEST_EARNING * 1.5) / 30) * MissionCalculations.mission_day()
            else:
                doc_benefit = 0

            earning = ((LOWEST_EARNING / 30) * multipiler * MissionCalculations.mission_day()) + benefit + doc_benefit

            conn.commit()
            conn.close()
        else:
            earning = 0

        return earning

# kivy bulider ------------------------------------------------------------------------------------------
Builder.load_file('motivator.kv')

# Main screen -------------------------------------------------------------------------------------------
class MainScreen(Screen):
    mission_type = StringProperty()
    today_data = StringProperty()
    mission_day = StringProperty()
    mission_earning = StringProperty()
    out_mission_days = StringProperty()
    

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.mission_type = MainScreen.m_type()
        self.today_data = f"{str(date.today())}"
        if MissionCalculations.whole_days() == -1:
            self.mission_day = "wybierz datę"
        else:
            self.mission_day = f"{str(MissionCalculations.mission_day())} dzień z {str(MissionCalculations.whole_days())} dni misji"
        self.mission_earning = "{:.2f} zł.".format(MissionCalculations.m_earning())
        
        if os.path.isfile('mission_data.db'):
            MainScreen.pie_chart()
            chart = self.ids.chart
            chart.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        self.out_mission_days = MissionCalculations.get_mission_days_out()
    
    def mission_out_days(self, sign, days):
        if sign == "-":
            if int(days) > 0:
                out_days =  str(int(days) -1)
            else:
                out_days = "0"
        else:
            if int(days) < MissionCalculations.whole_days():
                out_days =  str(int(days) +1)
            else:
                out_days = str(MissionCalculations.whole_days())
        
        self.ids.out_mission_label.text = out_days
        if os.path.isfile('mission_data.db'):
            MainScreen.save_out_days(out_days)
        
        print(MissionCalculations.get_mission_days_out())


    def save_out_days(days):
        conn = sqlite3.connect('mission_data.db')
        c = conn.cursor()
        c.execute("UPDATE mission_data SET out_mission = ?", (days))
        conn.commit()
        conn.close()


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
            mission = "wybierz misję"
        return mission

    def pie_chart():

        percent_remaning = int((MissionCalculations.remaning_days() * 100)/MissionCalculations.whole_days())
        percent_mission = int(100 - percent_remaning)
        rmd = str(MissionCalculations.remaning_days())
        
        khaki = (97/255, 131/255, 88/255, 1)
        grey =  (.06, .06, .06, 1)

        slices = [percent_mission, percent_remaning]
        labels = ["", f"{percent_remaning}%"]
        colors = [grey, khaki]
        

        if rmd == '1':
            days = "dzień"
        else:
            days = "dni"

        plt.figure(facecolor = grey)
        plt.title('pozostało:', color='white', fontsize=17)

        plt.pie(slices, labels=labels, textprops={'color': 'white', 'fontsize':15}, colors=colors, startangle= 90, counterclock=False, labeldistance=1.2)
        centre_circle =plt.Circle((0, 0), 0.80, fc=grey)
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.text(0, .1, rmd, ha='center', color='white', fontsize=18)
        plt.text(0, -.3, days, ha='center', color='white', fontsize=15)



# SettingScreen -----------------------------------------------------------------------------------------
class SettingScreen(Screen):
    message_text = StringProperty()
    
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
        if mission == "wybierz misję" or range == "wybierz stopień etatowy" or s_year == "R" or e_year == "R" or s_month == "M" or e_month == "M" or s_day == "D" or e_day == "D":
            if mission == "wybierz misję":
                mission = 0
            if range == "wybierz stopień etatowy":
                range = 0
            if s_year == "R" or s_month == "M" or s_day == "D":
                start_date = 0
            else:
                start_date = 1
            if e_year == "R" or e_month == "M" or e_day == "D":
                end_date = 0
            else:
                end_date = 1
        else:
            start_date = date(int(s_year), MONTHS_DICT[s_month], int(s_day))
            end_date = date(int(e_year), MONTHS_DICT[e_month], int(e_day))
            if not os.path.isfile('mission_data.db'):
                conn = sqlite3.connect('mission_data.db')
                c = conn.cursor()
                c.execute("""CREATE TABLE mission_data (
                        mission TEXT,
                        range TEXT,
                        specialist NUMERIC,
                        doctor NUMERIC,
                        start_date TEXT,
                        end_date TEXT,
                        out_mission TEXT
                    )""")
                c.execute("INSERT INTO mission_data VALUES (?, ?, ?, ?, ?, ?,?)", (mission, range, spec, doc, start_date, end_date, "0"))
                conn.commit()
                conn.close()
            else:
                conn = sqlite3.connect('mission_data.db')
                c = conn.cursor()
                c.execute("UPDATE mission_data SET mission = ?, range = ?, specialist = ?, doctor = ?, start_date = ?, end_date = ?", (mission, range, spec, doc, start_date, end_date))
                conn.commit()
                conn.close()
        
        self.manager.screens[1].ids.message_label.text  = SettingScreen.message(mission, range, start_date, end_date)

        self.manager.screens[0].ids.mission_label.text = "{}".format(MainScreen.m_type())
        self.manager.screens[0].ids.earning_label.text = "{:.2f} zł.".format(MissionCalculations.m_earning())
        
        MainScreen.pie_chart()
        chart = self.manager.screens[0].ids.chart
        chart.clear_widgets()
        chart.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        if MissionCalculations.whole_days() == -1:
            self.mission_day = "wybierz datę"
        else:
            self.manager.screens[0].ids.mission_day_label.text = f"{str(MissionCalculations.mission_day())} dzień z {str(MissionCalculations.whole_days())} dni misji"
        
        # TODO delete before production" 
        # print (start_date)
        # print(type(start_date))
        # print (end_date)
        # print(type(end_date))
    
    def message(mission, range, start_date, end_date):
        messages = []
        
        if mission == 0:
            messages.append("wybierz misję")
        if start_date == 0:
            messages.append("ustaw datę rozpoczęcia")
        if end_date == 0:
            messages.append("ustaw datę zakończenia")
        if start_date > end_date:
            messages.append("podaj prawidłowe daty")
        if range == 0:
            messages.append("wybierz stopień etatowy")

        
        if messages:
            message_text = ""
            for message in messages:
                message_text = f"{message_text} {message}\n"
            text = f"{message_text}"
        else:
            text = f"zapisano"
        return text
    
    def checkbox_clicked(self, instance, value):
        pass


    def range_clicked(self, range):
        pass

# Application  ------------------------------------------------------------------------------------------------

class Motivator(App):
    range_list = list(RANGE_DICT.keys())
    year = int(date.today().year)
    years_list = [str(x) for x in range(year-1, year+3)]
    months_list = list(MONTHS_DICT.keys())
    days_list = [str(x) for x in range(1, 32)]
    # TODO: change the list do to month
    days_list_29 = [str(x) for x in range(1, 30)]
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingScreen(name='settings'))
        return sm

if __name__ == '__main__':
    Motivator().run()