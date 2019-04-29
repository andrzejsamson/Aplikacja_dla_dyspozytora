import wx

class App(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)
        self.InitFrame()

    def InitFrame(self):
        frame = MyFrame(parent=None, title="Aplikacja dyspozytora")
        frame.Show()

class MyFrame(wx.Frame):
    def __init__(self,parent,title):
        super().__init__(parent = parent, title = title)
        self.OnInit()
        self.Listwa()
        
    def OnInit(self):
        panel = MyPanel(parent=self)

    def Listwa(self):
        menu = wx.MenuBar()
        button = wx.Menu()
        zlec1 = button.Append(wx.ID_ANY,"Dodaj","Dodaj zlecenie")
        zlec2 = button.Append(wx.ID_ANY,"Przegladaj","Przegladaj zlecenia")

        menu.Append(button,"Zlecenia")

        button = wx.Menu()
        kier1 = button.Append(wx.ID_ANY,"Dodaj","Dodaj kierowcę")
        kier2 = button.Append(wx.ID_ANY,"Przegladaj","Status kierowców")

        menu.Append(button,"Kierowcy")

        button = wx.Menu()
        opcje1 = button.Append(wx.ID_ANY,"Pomoc","Menu pomocy")
        opcje2 = button.Append(wx.ID_EXIT,"Wyjście","Wyjście z aplikacji")
        menu.Append(button,"Opcje")
        
        self.SetMenuBar(menu)
        self.Show()
    
class MyPanel(wx.Panel):
    def __init__(self,parent):
        super().__init__(parent=parent)


if True:
    App().MainLoop()
    
        
