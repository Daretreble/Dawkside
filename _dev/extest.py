import wx

class MyFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=(300, 150))

		self.panel = wx.Panel(self)
		self.vbox = wx.BoxSizer(wx.VERTICAL)

		self.setup_panel_content()

	def setup_panel_content(self):
		# Create a label for the pull-down menu
		label_choice = wx.StaticText(self.panel, label="Select an option:")
		self.vbox.Add(label_choice, 0, wx.EXPAND | wx.ALL, 10)

		# Create a pull-down menu
		menu_choices = ["Option 1", "Option 2", "Option 3"]
		self.choice = wx.Choice(self.panel, choices=menu_choices)
		self.vbox.Add(self.choice, 0, wx.EXPAND | wx.ALL, 10)

		# Create a label for the input field
		label_text_ctrl = wx.StaticText(self.panel, label="Enter some text:")
		self.vbox.Add(label_text_ctrl, 0, wx.EXPAND | wx.ALL, 10)

		# Create an input field
		self.text_ctrl = wx.TextCtrl(self.panel)
		self.vbox.Add(self.text_ctrl, 0, wx.EXPAND | wx.ALL, 10)

		# Create a submit button
		submit_button = wx.Button(self.panel, label="Submit")
		submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
		self.vbox.Add(submit_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

		self.panel.SetSizer(self.vbox)

	def on_submit(self, event):
		selected_option = self.choice.GetStringSelection()
		input_text = self.text_ctrl.GetValue()
		wx.MessageBox(f"Selected option: {selected_option}\nInput text: {input_text}", "Submission Result", wx.OK | wx.ICON_INFORMATION)

		# Reset the panel to clear its contents
		self.reset_panel()

	def reset_panel(self):
		# Destroy the current panel
		self.panel.Destroy()
		# Recreate an empty panel
		self.panel = wx.Panel(self)
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.panel.SetSizer(self.vbox)
		self.Refresh()

if __name__ == '__main__':
	app = wx.App()
	frame = MyFrame(None, -1, 'Simple wxPython GUI')
	frame.Show()
	app.MainLoop()