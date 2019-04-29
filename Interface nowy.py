import os
import wx

class Okno(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(400,-1))
        panel = wx.Panel(self)
        self.quote = wx.StaticText(panel,label="Witaj w aplikacji", pos=(30,30))
        self.Show()
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

app = wx.App(False)
frame = Okno(None, "Aplikacja dyspozytora")
app.MainLoop()
        
