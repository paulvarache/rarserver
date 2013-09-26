#!/usr/bin/python
#-*- coding: ISO-8859-1 -*-
# This script is inspired by : http://www.navarin.de/projects/rbox/
# Website ans repository : https://github.com/paulvarache/rarserver

#Copyright (C) 2013 Varache Paul

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO :
	# Repeat : Not available with mpris interfaces
	# Library sync : Not yet implemented

from rarserver_core import RarServerCore
from rarserver_config import RarServerConfig
from rarserver_options import RarServerOptions_wx
import threading
import pynotify
import sys
import os
import time

try:
	import wx
except ImportError:
	raise ImportError, "The wxPython module is required to run this program. "

#Global vars
BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep
TRAY_TOOLTIP = 'RarServer'
TRAY_ICON = 'icon.png'
TRAY_ICON_LISTEN = 'icon-listen.png'
TRAY_ICON_CONNECT = 'icon-connect.png'
TRAY_ICON_ERROR = 'icon-error.png'

class RarTrayIcon_wx(wx.TaskBarIcon):
	def __init__(self):
		wx.TaskBarIcon.__init__(self)

		self.setIcon(TRAY_ICON)

		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnLeftClick)
		self.Bind(wx.EVT_MENU, self.OnOptions, id=1)
		self.Bind(wx.EVT_MENU, self.OnReconnect, id=2)
		self.Bind(wx.EVT_MENU, self.OnClose, id=3)

		self.timer = wx.Timer(self)		
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		self.timer.Start(1000)

		self.initCore()
		self.status = ""
		self.updateIcon()
		pynotify.init("icon-summary-body")

	def setIcon(self, path):
		self.tbIcon = wx.IconFromBitmap(wx.Bitmap(BASE_DIR+path))		
		self.SetIcon(self.tbIcon, TRAY_TOOLTIP)

	def CreatePopupMenu(self):
		menu = wx.Menu()
		messageItem = menu.Append(0, self.core.message)
		menu.AppendSeparator()
		menu.Append(1, 'Options')
		menu.Append(2, 'Reconnect')
		menu.AppendSeparator()
		menu.Append(3, 'Exit')
		messageItem.Enable(False)
		return menu

	def OnReconnect(self, event):
		self.core.Destroy()
		self.initCore()

	def initCore(self):
		self.config = RarServerConfig()
		self.core = RarServerCore()
		self.core.port = self.config.getPortNumber()
		self.listeningThread = threading.Thread(None, self.core.listen)
		self.listeningThread.setDaemon(True)
		self.listeningThread.start()

	def OnClose(self, event):
		self.close()

	def close(self):
		self.core.Destroy()
		self.tbIcon.Destroy()
		self.Destroy()
		sys.exit(0)

	def OnOptions(self, event):
		self.options = RarServerOptions_wx(None, -1, 'Options', self.config)
		self.options.Centre()

	def OnLeftClick(self, event):
		self.PopupMenu(self.CreatePopupMenu())
	
	def OnTimer(self, event):
		self.updateIcon()
		if self.core.status == "error":
			self.notifyError()
		else:
			t = threading.Thread(None, self.core.manageAction)
			t.setDaemon(True)
			t.start()
		self.status = self.core.status

	def updateIcon(self):
		if self.status != self.core.status:
			if self.core.status == "listen":
				self.setIcon(TRAY_ICON_LISTEN)
			elif self.core.status == "connect":
				self.setIcon(TRAY_ICON_CONNECT)
			elif self.core.status == "error":
				self.setIcon(TRAY_ICON_ERROR)

	def notifyError(self):
		if self.status != self.core.status:
			n = pynotify.Notification("RarServer",self.core.message);
			n.show()

if __name__ == "__main__":
	app = wx.App()
	frame = RarTrayIcon_wx()
	app.MainLoop()

