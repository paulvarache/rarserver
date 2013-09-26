#!/usr/bin/python
#-*- coding: ISO-8859-1 -*-

import ConfigParser
from rarserver_config import RarServerConfig

try:
	import wx
except ImportError:
	raise ImportError, "The wxPython module is required to run this program. "

class RarServerOptions_wx(wx.Frame):
	def __init__(self, parent, id, title, config):
		wx.Frame.__init__(self, parent, id, title)
		self.parent = parent
		self.config = config
		self.initialize()
		
	def initialize(self):
		portNumber = self.config.getPortNumber()
		sizer = wx.GridBagSizer()

		self.portEntry = wx.TextCtrl(self, -1, value=str(portNumber))
		self.label = wx.StaticText(self, -1, label="Port number:")

		button = wx.Button(self, -1, label="Save")		

		sizer.Add(self.label, (0,0), (1,2), wx.EXPAND)

		sizer.Add(self.portEntry, (1,0), (1,1), wx.EXPAND)
		sizer.Add(button, (1,1))

		self.Bind(wx.EVT_BUTTON, self.OnSave, button)

		self.SetSizerAndFit(sizer)
		self.Show()

	def OnSave(self, event):
		self.config.savePortNumber(self.portEntry.GetValue())
		wx.MessageBox('You will need to restart RarServer to apply the new values', 'Info', wx.OK | wx.ICON_INFORMATION) 
		self.Destroy()
