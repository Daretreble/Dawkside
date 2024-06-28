import wx

class PanelOne(wx.Panel):
    def __init__(self, parent):
        super(PanelOne, self).__init__(parent)
        text = wx.StaticText(self, label="Panel One")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL, 10)
        self.SetSizer(sizer)

class PanelTwo(wx.Panel):
    def __init__(self, parent):
        super(PanelTwo, self).__init__(parent)
        text = wx.StaticText(self, label="Panel Two")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL, 10)
        self.SetSizer(sizer)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        
        # Create a notebook (tabs container)
        self.notebook = wx.Notebook(self)
        
        # Create panels for each tab
        self.panel_one = PanelOne(self.notebook)
        self.panel_two = PanelTwo(self.notebook)
        
        # Add panels to the notebook with labels
        self.notebook.AddPage(self.panel_one, "Tab 1")
        self.notebook.AddPage(self.panel_two, "Tab 2")
        
        # Bind the notebook tab change event
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_change, self.notebook)
        
        # Create a sizer for the frame
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Center()
    
    def on_tab_change(self, event):
        # Get the index of the current tab
        selected_tab = event.GetSelection()
        if selected_tab == 0:
            print("Panel One selected")
            # Do something when Tab 1 is selected
        elif selected_tab == 1:
            print("Panel Two selected")
            # Do something when Tab 2 is selected
        event.Skip()

def main():
    app = wx.App()
    frame = MyFrame(None, title="Tabbed Panels Example", size=(400, 300))
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()