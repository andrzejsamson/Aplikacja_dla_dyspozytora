import os
import wx
from collections import defaultdict, deque
import sqlite3
from datetime import datetime
import dijkstra as dij

graph = dij.Graph()
db = sqlite3.connect('ASJW.db')
db.row_factory = sqlite3.Row
kursor = db.cursor()
kursor.execute(
        """
        SELECT miejscowosc_A, miejscowosc_B, czas FROM PUNKTY_MAPY
        """)
punkty = kursor.fetchall()
zbior = list()
z = list()
s = list()
t = list()
for PUNKTY_MAPY in punkty:
    z.append(PUNKTY_MAPY['miejscowosc_A'])
    s.append(PUNKTY_MAPY['miejscowosc_B'])
    t.append(PUNKTY_MAPY['czas'])
    zbior = z + s
        
for node in zbior:
    graph.add_node(node)

i = 0
while i < len(z):
    graph.add_edge(str(z[i]), str(s[i]), int(t[i]))
    i = i + 1

newzbior = list(dict.fromkeys(zbior))

class PanelOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(400,100))
        self.quote = wx.StaticText(self,label="Witaj w aplikacji:", pos=(30,30))

class PanelTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(400,200), pos=(0,110))
        self.quote = wx.StaticText(self, label="Trwa dodawanie zlecenia...", pos=(10, 10))
        self.sampleList = newzbior
        self.lblhear = wx.StaticText(self, label="Miejscowosc poczatkowa:", pos=(10, 40))
        self.edithear = wx.ComboBox(self, pos=(150, 40), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.lblhear = wx.StaticText(self, label="Miejscowosc koncowa:", pos=(10, 70))
        self.edithear = wx.ComboBox(self, pos=(150, 70), choices=self.sampleList, style=wx.CB_DROPDOWN)
        waga = ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000']
        self.sampleList2 = waga
        self.lblhear = wx.StaticText(self, label="Waga:", pos=(10, 100))
        self.edithear = wx.ComboBox(self, pos=(150, 100), choices=self.sampleList2, style=wx.CB_DROPDOWN)
        
class Okno(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(400,400))
        self.panel_one = PanelOne(self)
        self.panel_two = PanelTwo(self)
        self.panel_two.Hide()
        self.CreateStatusBar()

        menubar = wx.MenuBar()
        
        menu1 = wx.Menu()
        DodajZlec = menu1.Append(wx.ID_ANY, "Dodaj", "Dodaje zlecenie")
        PrzegladajZlec = menu1.Append(wx.ID_ANY, "Przegladaj", "Przeglądaj zlecenia")

        menubar.Append(menu1,"Zlecenia")
        self.SetMenuBar(menubar)
        
        menu2 = wx.Menu()
        DodajKier = menu2.Append(wx.ID_ANY, "Dodaj", "Dodaje kierowców")
        PrzegladajKier = menu2.Append(wx.ID_ANY, "Przegladaj", "Przeglądaj kierowców")

        menubar.Append(menu2,"Kierowcy")
        self.SetMenuBar(menubar)
        
        menu3 = wx.Menu()
        Pomoc = menu3.Append(wx.ID_ABOUT, "Pomoc", "Menu pomocy")
        Wyjscie = menu3.Append(wx.ID_EXIT, "Zamknij", "Zamyka okno")

        menubar.Append(menu3,"Opcje")
        self.SetMenuBar(menubar)

        # EVENTS

        self.Bind(wx.EVT_MENU, self.DodZlec, DodajZlec)
        #self.Bind(wx.EVT_MENU, self.PrzegZlec, PrzegladajZlec)

        #self.Bind(wx.EVT_MENU, self.DodKier, DodajKier)
        #self.Bind(wx.EVT_MENU, self.PrzegKier, PrzegladajKier)
        
        self.Bind(wx.EVT_MENU, self.OnHelp, Pomoc)
        self.Bind(wx.EVT_MENU, self.OnExit, Wyjscie)
        
    def DodZlec(self, e):
            self.panel_two.Show()
    
    def OnHelp(self, e):
        dialog = wx.MessageDialog(self, "W celu uzyskania pomocy pisz do jedrekwisniewski@wp.pl", "Okno Pomocy", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        
    def OnExit(self,e):
        self.Close()
        

app = wx.App(False)
frame = Okno(None, "Aplikacja dyspozytora")
frame.Show()
app.MainLoop()
