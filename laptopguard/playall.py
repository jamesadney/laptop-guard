#!/usr/bin/python

# [SNIPPET_NAME: Playing a Pipeline]
# [SNIPPET_CATEGORIES: GStreamer]
# [SNIPPET_DESCRIPTION: Construct and play a pipeline]
# [SNIPPET_AUTHOR: Tiago Boldt Sousa <tiagoboldt@gmail.com>]
# [SNIPPET_LICENSE: GPL]

# Modified by James Adney for alarm program

import pygst
pygst.require("0.10")
import gst
import gobject

#Create a player

class Player:
	def __init__(self, file, repeat=True):
		#Element playbin automatic plays any file
		self.player = gst.element_factory_make("playbin2", "player")
		#Set the uri to the file
		self.player.set_property("uri", "file://" + file)
		#Enable message bus to check for errors in the pipeline
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_message)
		self.repeat = repeat
	
	def run(self):
		self.player.set_state(gst.STATE_PLAYING)
		
	def stop(self):
		self.player.set_state(gst.STATE_NULL)

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			
			#FIXME: repeat not working
			if self.repeat:
				print "repeating"
				# go back to beginning
				#self.player.set_state(gst.STATE_NULL)
				#self.player.set_state(gst.STATE_PLAYING)
				self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 0)
			else:
				print "stopping"
				#file ended, stop
				self.player.set_state(gst.STATE_NULL)
				
		elif t == gst.MESSAGE_ERROR:
			#Error ocurred, print and stop
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug


#Execution starts here
if __name__ == "__main__":
	
	audio_file = "/home/james/workspace/laptop-guard/media/caralarm.ogg"
	player = Player(audio_file)
	player.run()
	loop = gobject.MainLoop()
	loop.run()

