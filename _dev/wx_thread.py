import wx
import threading
import time

# Define your wxPython application
class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        
        self.panel = wx.Panel(self)
        self.status_bar = self.CreateStatusBar()

        # Create a button to start the separate thread
        self.button = wx.Button(self.panel, label="Start Task")
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.button, 0, wx.ALL, 10)
        self.panel.SetSizer(sizer)

    def on_button_click(self, event):
        # Start a new thread for your non-GUI code
        thread = threading.Thread(target=self.perform_task)
        thread.start()

    def perform_task(self):
        # Simulate a long-running task
        for i in range(1, 11):
            time.sleep(1)  # Simulate some work being done
            wx.CallAfter(self.update_status, f"Task progress: {i * 10}%")
        
        wx.CallAfter(self.update_status, "Task completed")

    def update_status(self, message):
        self.status_bar.SetStatusText(message)


def main():
    app = wx.App(False)
    frame = MyFrame(None, title='Separate Thread Example', size=(300, 200))
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
