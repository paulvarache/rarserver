# WHAT IS RHYTHMBOX ANDROID REMOTE ?
	
	This script allows you to control your rhythmbox player 
	with an android device.

# DOES IT WORKS WITH ALL VERSIONS OF RHYTHMBOX ?

	NO.
	Only with Rhythmbox 2.95 and above.
	If you have a previous version, take a look here : 
		http://www.navarin.de/projects/rbox/

# HOW DOES IT WORKS ?
 
 	It's simple.
 	1) Run the script "rarserver.py"
 	2) Install "Banshee Remote" app to your android device
 	3) You can now control your music player :)
 	
# WHAT CAN I CONTROL ?
	
	For now, you can control :
	- Volume (up/down)
	- Play/Pause
	- Previous/Next
	- Shuffle
	- Seek
	- Cover / Meta

# OPTIONS
	
	You can change the listening port via the option menu.

# AND ABOUT PROGRAMMING ?

	This script is inspired by this one : http://www.navarin.de/projects/rbox/.
	Written in python using mpris dbus interfaces. 
	The goal is to make the Banshee Remote app working with Rhythmbox 2.95+
	
# WHAT IS PLANNED FOR THE FUTURE ?
	
	1) Add support of library, to choose a song/artist/album to play from the device.
	2) Create a rhythmbox plugin for this script
	
# Additional informations

	Not tested in rhythmbox 2.95
	Works with Rhythmbox 2.96
	You might not see the tray icon, in this case, you'll need to add this app to the ubuntu tray icon whitelist:
		http://askubuntu.com/questions/30742/how-do-i-access-and-enable-more-icons-to-be-in-the-system-tray
