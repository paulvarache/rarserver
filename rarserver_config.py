#!/usr/bin/python
#-*- coding: ISO-8859-1 -*-

import ConfigParser
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep

class RarServerConfig():
	def __init__(self):
		self.config = ConfigParser.ConfigParser()

	def getPortNumber(self):
		self.config.read(BASE_DIR+"config.ini")
		return int(self.config.get("Port", "port"))

	def savePortNumber(self, portNumber):
		cfgfile = open(BASE_DIR+'config.ini','w')
		self.config = ConfigParser.ConfigParser()
		self.config.add_section("Port")
		self.config.set("Port", "port", portNumber)
		self.config.write(cfgfile)
		cfgfile.close()
