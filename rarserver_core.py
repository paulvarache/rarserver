#!/usr/bin/python
#-*- coding: ISO-8859-1 -*-

import socket
import dbus
import errno

PORT_NUMBER = 8484

class RarServerCore:
	def __init__(self):

		#DBus
		self.playerPath = 'org.mpris.MediaPlayer2.Player'
		bus = dbus.SessionBus()
		rbox = bus.get_object('org.gnome.Rhythmbox3', '/org/mpris/MediaPlayer2')
		self.player = dbus.Interface(rbox, self.playerPath)
		self.playerPr = dbus.Interface(rbox, 'org.freedesktop.DBus.Properties')
		self.status = ""
		self.port = PORT_NUMBER
	
	def Destroy(self):
		self.server_socket.close()

	def listen(self):
		# Server socket
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.settimeout(None)
		try:
			self.server_socket.bind(("", self.port))
			self.server_socket.listen(5)
			self.status = "listen"	
			self.message = "Listening on "+self.getIp()+":"+str(self.port)
		except socket.error, v:
			errorcode = v[0]
			self.status = "error"
			if errorcode == errno.EADDRINUSE:
				self.message = "Error: Address already in use"

	def getIp(self):
		# Get current IP
		ipsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ipsocket.connect(('www.google.com',0))
		ip = ipsocket.getsockname()[0]
		ipsocket.close();
		return ip
		
	def manageAction(self):
		# Get self.action from device
		self.client_socket, address = self.server_socket.accept()
		self.status = "connect"
		self.message = "Client connected"
		received = self.client_socket.recv(512)
		self.action, var = received.split('/')
		
		# Set new position
		if self.action == "seek" :
			current = self.playerPr.Get(self.playerPath,"Position")
			new = int(var)*1000000
			seekVal = new - current
			self.player.Seek(seekVal)
		
		# Enable/Disable shuffle mode
		elif self.action == "shuffle" :
			current = self.playerPr.Get(self.playerPath, "Shuffle")
			if current == 0 :
				self.playerPr.Set(self.playerPath, "Shuffle", True)
			else :
				self.playerPr.Set(self.playerPath, "Shuffle", False)
		
		# Volume Up
		elif self.action == "volumeUp" :
			current = self.playerPr.Get(self.playerPath, "Volume")
			self.playerPr.Set(self.playerPath, "Volume", current + 0.1)
		
		# Volume Down
		if self.action == "volumeDown" :
			current = self.playerPr.Get(self.playerPath, "Volume")
			self.playerPr.Set(self.playerPath, "Volume", current - 0.1)
		
		# Cover request
		elif self.action ==  "coverImage" :
			meta = self.playerPr.Get(self.playerPath,"Metadata")
			if meta.has_key("mpris:artUrl") :
				path = str(meta["mpris:artUrl"])
				path = path[7:len(path)]
				cover = open(path)
				reply=cover.read()
				cover.close()
				self.client_socket.send(reply)
		
		# All informations about current song
		elif self.action == "all": 
			status = self.playerPr.Get(self.playerPath,"PlaybackStatus")
			meta = self.playerPr.Get(self.playerPath,"Metadata")
			position = self.playerPr.Get(self.playerPath,"Position")/1000000
			artExists = "false";
			
			if meta.has_key("mpris:artUrl") :
				artExists = "true";
		
				ret = ""
				ret += status.lower() + "/"
				ret += meta["xesam:album"] + "/"
				ret += meta["xesam:artist"][0] + "/"
				ret += meta["xesam:title"] + "/"
				ret += str(position) + "/"
				ret += str(meta["mpris:length"] / 1000000) + "/"
				ret += str(artExists)
			
				self.client_socket.send(ret.encode('utf-8'))
		
		# Previous track
		elif self.action == "prev":
			self.player.Previous()
		# Play/Pause self.action
		elif self.action == "playPause":
			self.player.PlayPause()
		# Next track
		elif self.action == "next":
			self.player.Next()
		
		self.client_socket.close()
