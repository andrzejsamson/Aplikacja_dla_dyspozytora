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
newzbior = sorted(newzbior)
newzbior.remove('A')
newzbior.remove('B')
newzbior.remove('C')
newzbior.remove('D')
newzbior.remove('E')
newzbior.remove('F')

class PanelOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(400,100))
        self.quote = wx.StaticText(self,label="Witaj w aplikacji:", pos=(30,30))

class PanelZlecDodaj(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(400,200), pos=(0,110))
        self.miejscA = str()
        self.miejscB = str()
        self.ciezar = str()
        self.kierowca = str()
        self.quote = wx.StaticText(self, label="Trwa dodawanie zlecenia...", pos=(10, 10))
        self.sampleList = newzbior
        self.lblhear1 = wx.StaticText(self, label="Miejscowosc poczatkowa:", pos=(10, 40))
        self.edithear1 = wx.ComboBox(self, pos=(150, 40), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.MiejscA, self.edithear1)
        self.lblhear2 = wx.StaticText(self, label="Miejscowosc koncowa:", pos=(10, 70))
        self.edithear2 = wx.ComboBox(self, pos=(150, 70), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.MiejscB, self.edithear2)
        waga = ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000']
        self.sampleList2 = waga
        self.lblhear3 = wx.StaticText(self, label="Waga:", pos=(10, 100))
        self.edithear3 = wx.ComboBox(self, pos=(150, 100), choices=self.sampleList2, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.Ciezar, self.edithear3)
        self.buttonZlec = wx.Button(self, label="Dodaj", pos=(250,170))
        self.Bind(wx.EVT_BUTTON, self.OnClickZlec, self.buttonZlec)

    def MiejscA(self, event):
        self.miejscA = event.GetString()

    def MiejscB(self, event):
        self.miejscB = event.GetString()

    def Ciezar(self, event):
        self.ciezar = event.GetString()

    def OnClickZlec(self, event):
        if self.miejscA == '' or self.miejscB == '' or self.ciezar == '':
            bladZlec = wx.MessageDialog(self, "Wybierz wszystkie pozycje", "Błąd wyboru", wx.OK)
            bladZlec.ShowModal()
            bladZlec.Destroy()
        else:
            # można dodać info czy jestes pewny
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            task = (self.miejscA, self.miejscB, self.ciezar, now)
            sql = """ INSERT INTO Zlecenia(skad,dokad,masa,data_przyjscia) VALUES(?,?,?,?) """
            kursor.execute(sql, task)
            db.commit()
            
            kursor.execute(
                """
                SELECT ID_zlecenia FROM zlecenia
                """)
            zlecenia = kursor.fetchall()
            for ID_zlecenia in zlecenia:
                aktualne = ID_zlecenia
            sql2 = """ INSERT INTO Wykonania(ID_zlecenia,ID_samochodu,data_wykonania) VALUES(?,NULL,NULL) """
            kursor.execute(sql2, aktualne)
            db.commit()
            potwierdzenie = wx.MessageDialog(self, "Dodano zlecenie do bazy", "Potwierdzenie", wx.OK)
            potwierdzenie.ShowModal()
            potwierdzenie.Destroy()
            self.Destroy()

class PanelZlecPrzydziel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(400,200), pos=(0,110))
        self.wiadomosc = wx.StaticText(self, label="Lista wolnych zleceń:", pos=(10, 10))
        kursor.execute(
        """
        SELECT ID_zlecenia, skad, dokad, masa, data_przyjscia FROM Zlecenia NATURAL JOIN Wykonania WHERE ID_samochodu IS NULL ORDER BY data_przyjscia
        """)
        wykonania = kursor.fetchall()
        self.pier = list()
        self.dwa = list()
        self.trzy = list()
        lista = list()
        
        for i in wykonania:
            self.pier.append(i['skad'])
            self.dwa.append(i['dokad'])
            self.trzy.append(i['ID_zlecenia'])
            lista.append(i['skad'] + ":" + i['dokad'] + ":" + str(i['masa']) + ":" + i['data_przyjscia'])
        if len(lista) == 0:
            self.napis = wx.StaticText(self, label="0", pos=(150,10))
        else:
            self.listbox = wx.ListBox(self, pos=(10, 30), size=(360, 100))
            self.Bind(wx.EVT_LISTBOX, self.skad, self.listbox) 
            self.listbox.InsertItems(lista,0)
            self.buttonPrzydziel = wx.Button(self, label="Przydziel kierowcę", pos=(10,170))
            self.Bind(wx.EVT_BUTTON, self.PrzydzielKier, self.buttonPrzydziel)

    def skad(self, event):
        self.skad = self.listbox.GetSelection()
        self.pier1 = self.pier[self.skad]
        self.dwa1 = self.dwa[self.skad]
        self.trzy1 = self.trzy[self.skad]

    def PrzydzielKier(self, event):
        self.listbox.Hide()
        self.buttonPrzydziel.Hide()
        self.ppaarr11 = wx.StaticText(self, label="Miejscowosc poczatkowa:", pos=(10, 40))
        self.par1 = wx.StaticText(self, label="%s" %self.pier1, pos=(150, 40))
        self.ppaarr22 = wx.StaticText(self, label="Miejscowosc koncowa:", pos=(10, 70))
        self.par2 = wx.StaticText(self, label="%s" %self.dwa1, pos=(150, 70))
        kursor.execute(
                """
                SELECT id_samochodu, miejsce_przebywania FROM SAMOCHODY WHERE miejsce_przebywania IS NOT NULL
                """)
        kierowcy = kursor.fetchall()
        k = list()
        m = list()
        for SAMOCHODY in kierowcy:
            k.append(SAMOCHODY['miejsce_przebywania'])
            m.append(SAMOCHODY['id_samochodu'])
        w = {}
        e = {}
        for i in range(len(k)):
            w[m[i]],e[m[i]] = dij.shortest_path(graph, str(k[i]), self.pier1)
        lista = sorted(w.items(), key=lambda x: x[1])
        lista2 = []
        self.idkierowcy = list()
        for elem in lista:
            self.idkierowcy.append(int(elem[0]))
            lista2.append(str(elem[0]) + "::" + str(elem[1]) + "min")
        self.sampleList3 = lista2
        self.edithear4 = wx.ComboBox(self, pos=(150,130), choices=self.sampleList3, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.Kierowca, self.edithear4)
        self.buttonEnd1 = wx.Button(self, label="Zaakceptuj", pos=(250,170))
        self.Bind(wx.EVT_BUTTON, self.OnClickAccept, self.buttonEnd1)

    def Kierowca(self, event):
        self.kierowca = event.GetSelection()
        self.kierowcaID = self.idkierowcy[self.kierowca]

    def OnClickAccept(self, event):
        if self.kierowca == '':
            bladZlec2 = wx.MessageDialog(self, "Wybierz kierowcę", "Błąd wyboru kierowcy", wx.OK)
            bladZlec2.ShowModal()
            bladZlec2.Destroy()
        else:
            kursor.execute(
                """
                UPDATE Wykonania
                SET ID_samochodu = ?
                WHERE ID_zlecenia = ?
                """, (self.kierowcaID, self.trzy1))
            db.commit()
            kursor.execute(
                """
                UPDATE Samochody
                SET miejsce_przebywania = ?
                WHERE ID_samochodu = ?
                """, (None, self.kierowcaID))
            db.commit()

            potwierdzenie2 = wx.MessageDialog(self, "Przydzielono kierowcę do zlecenia", "Potwierdzenie", wx.OK)
            potwierdzenie2.ShowModal()
            potwierdzenie2.Destroy()
            self.Destroy()            
        
class Okno(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(400,400))
        self.panel_one = PanelOne(self)
        self.panel_zlec_dodaj = PanelZlecDodaj(self)
        self.panel_zlec_dodaj.Hide()
        self.panel_zlec_przydziel = PanelZlecPrzydziel(self)
        self.panel_zlec_przydziel.Hide()
        self.CreateStatusBar()

        menubar = wx.MenuBar()
        
        menu1 = wx.Menu()
        DodajZlec = menu1.Append(wx.ID_ANY, "Dodaj", "Dodaje zlecenie")
        PrzydzielZlec = menu1.Append(wx.ID_ANY, "Przydziel pojazd", "Przydziela kierowcę do zlecenia")
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
        self.Bind(wx.EVT_MENU, self.PrzydzZlec, PrzydzielZlec)
        #self.Bind(wx.EVT_MENU, self.PrzegZlec, PrzegladajZlec)

        #self.Bind(wx.EVT_MENU, self.DodKier, DodajKier)
        #self.Bind(wx.EVT_MENU, self.PrzegKier, PrzegladajKier)
        
        self.Bind(wx.EVT_MENU, self.OnHelp, Pomoc)
        self.Bind(wx.EVT_MENU, self.OnExit, Wyjscie)
        
    def DodZlec(self, e):
        #self.panel_zlec_przydziel = PanelZlecPrzydziel(self)
        if self.panel_zlec_przydziel is not None:
            self.panel_zlec_przydziel.Hide()
        self.panel_zlec_dodaj = PanelZlecDodaj(self)
        self.panel_zlec_dodaj.Show()

    def PrzydzZlec(self, e):
        #self.panel_zlec_dodaj = PanelZlecDodaj(self)
        if self.panel_zlec_dodaj is not None:
            self.panel_zlec_dodaj.Hide()
        self.panel_zlec_przydziel = PanelZlecPrzydziel(self)
        self.panel_zlec_przydziel.Show()
    
    def OnHelp(self, e):
        dialog = wx.MessageDialog(self, "W celu uzyskania pomocy pisz do jedrekwisniewski@wp.pl", "Okno Pomocy", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        
    def OnExit(self,e):
        db.close()
        self.Close()
        
app = wx.App(False)
frame = Okno(None, "Aplikacja dyspozytora")
frame.Show()
app.MainLoop()

'''
self.par1 = wx.StaticText(self, label="%s" %self.miejscA, pos=(150, 40))
            self.par2 = wx.StaticText(self, label="%s" %self.miejscB, pos=(150, 70))
            self.par3 = wx.StaticText(self, label="%s" %self.ciezar, pos=(150, 100))
            self.lblhear4 = wx.StaticText(self, label="Lista kierowcow:", pos=(10,130))

            kursor.execute(
                """
                SELECT id_samochodu, miejsce_przebywania FROM SAMOCHODY WHERE miejsce_przebywania IS NOT NULL
                """)
            kierowcy = kursor.fetchall()
            k = list()
            m = list()
            for SAMOCHODY in kierowcy:
                k.append(SAMOCHODY['miejsce_przebywania'])
                m.append(SAMOCHODY['id_samochodu'])
            w = {}
            e = {}
            for i in range(len(k)):
                w[m[i]],e[m[i]] = dij.shortest_path(graph, str(k[i]), self.miejscA)
            lista = sorted(w.items(), key=lambda x: x[1])
            lista2 = []
            for elem in lista:
                lista2.append(str(elem[0]) + "::" + str(elem[1]) + "min")
            self.sampleList3 = lista2
            self.edithear4 = wx.ComboBox(self, pos=(150,130), choices=self.sampleList3, style=wx.CB_DROPDOWN)
            self.Bind(wx.EVT_COMBOBOX, self.Kierowca, self.edithear4)
            self.buttonEnd1 = wx.Button(self, label="Accept", pos=(250,170))
            #self.Bind(wx.EVT_BUTTON, self.OnClickAccept, self.buttonEnd1)

    def Kierowca(self, event):
        self.kierowca = event.GetString()
'''
