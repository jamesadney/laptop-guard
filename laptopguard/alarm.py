#!/usr/bin/env python

# Laptop Guard
# Copyright (C) 2011 James Adney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import dbus.mainloop.glib
import gobject

import sys, os, atexit, subprocess
from base64 import b64decode

import multimedia, mailer, preylock

from _settings import Settings

class Alarm:
    """
    Receives signal to trigger alarm and activates alarm
    """
    
    def __init__(self, working_directory=None):
        
        self.is_set = False
        self.working_directory = working_directory
        
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus()
        self.dbus_object  = self.session_bus.get_object("org.theftalarm.Alarm","/")
        self.gnome_session_manager = self.session_bus.get_object("org.gnome.SessionManager",
                                                                "/org/gnome/SessionManager")
        self.session_manager_iface = dbus.Interface(self.gnome_session_manager,
                                                    dbus_interface="org.gnome.SessionManager")
        
        # receive Unplugged signal
        self.dbus_object.connect_to_signal('TriggerAlarm', 
                                      self.handle_signals, 
                                      'org.theftalarm.Alarm.Service',
                                      arg0="Unplugged")
        
        # receive LidClosed signal
        self.dbus_object.connect_to_signal('TriggerAlarm', 
                                      self.handle_signals, 
                                      'org.theftalarm.Alarm.Service',
                                      arg0="LidClosed")
        
        # receive PowerButtonPressed signal
        self.dbus_object.connect_to_signal('TriggerAlarm', 
                                      self.handle_signals, 
                                      'org.theftalarm.Alarm.Service',
                                      arg0="PowerButtonPressed")
        
        atexit.register(self.__del__)
        
        
    def handle_signals(self, signal_string="Unidentified Signal"):
        """
        Receive signals from alarm-service and activate alarm when signal is
        received.
        """
        print "Received Signal: {0}".format(signal_string)
        self.activate()
       
    def initialize(self):
        """
        Start loop to wait for signal to activate alarm
        """ 
        if not self.is_set:
            
            #Get settings
            self.settings = Settings.get_instance()
            alarm_volume = int(self.settings.general["alarm_volume"])
            
            # make sure service sends a signal even if it previously sent some
            self.dbus_object.Reset(dbus_interface='org.theftalarm.Alarm.Service')
            
            self.cookie = self.session_manager_iface.Inhibit("Laptop Guard",
                                                        "0",
                                                        "Computer locked to let alarm trigger",
                                                        4|8)
            
            if self.working_directory:
                media_directory = os.path.join(self.working_directory, "media/")
            else:
                media_directory = self.settings.general["media_path"]
                
            audio_file = self.settings.general["audio_file"]
            audio_file_path = os.path.join(media_directory, audio_file)
            
            self.alarm_sound = multimedia.Sound(audio_file_path, 
                                                alarm_volume)
            try:
                self.camera = multimedia.Webcam()
            except:
                print "no camera detected"
                self.camera = None    
            
            self.is_set = True
            
            lockscreen_password = self.settings.general["lockscreen_password"]
            self.lock = preylock.Lock(lockscreen_password, 
                                      self.working_directory)
    
    def unset(self):
        """
        Stop looking for signal to activate alarm
        """
        try:
            del(self.alarm_sound)
            del(self.camera)
        except AttributeError:
            print "instances didn't need to be destroyed"
        
        self.session_manager_iface.Uninhibit(self.cookie)
        self.is_set = False
    
    def activate(self):
        """
        Start alarm sound and actions
        """
        if self.is_set:
            
            self.alarm_sound.play()
            pictures_directory = self.settings.general["pictures_directory"]
            
            self.pics_file_extension = self.settings.general["pictures_file_extension"]
            
            if self.camera:
                self.camera.take_pictures(dest_directory=pictures_directory,
                                      file_extension=self.pics_file_extension)
            else:
                pass
                
            self.__send_email()
        else:
            print "alarm must be set for it to be activated"
    
    def deactivate(self):
        """
        Stop alarm after it is activated
        """
        try:
            self.alarm_sound.stop()
        except AttributeError:
            print "No alarm to deactivate"
            
    def __send_email(self):
        """
        Use mailer package to send text message
        """
        message = mailer.Message()
        message.From = self.settings.general['from_address']
        message.To = self.settings.general['to_address']
        message.Subject = "Alarm"
        message.Body = self.settings.general['text_message']
        message.attach(os.path.join(self.settings.general['pictures_directory'] ,
                                    "alarmpic3.{0}".format(self.pics_file_extension)))
        
        sender = mailer.Mailer(settings.general["smtp_server"], 
                               int(settings.general["port"]), 
                               bool(settings.general["use_tls"]))
        sender.login(self.settings.general['username'], 
                     b64decode(self.settings.general["password"]))
        sender.send(message)
        
    def __del__(self):
        
        self.deactivate()
        
        if self.is_set:
            self.unset()
        
        #TODO: remove redundancies
        try:
            del(self.alarm_sound)
        except:
            pass
        
        #kill dbus service
        try:
            self.dbus_object.Exit(dbus_interface='org.theftalarm.Alarm.Service')
        except dbus.exceptions.DBusException:
            print "Not killing alarm service because it wasn't found"
    
if __name__ == "__main__":
    
    loop = gobject.MainLoop()
    alarm = Alarm()
    alarm.initialize()
    
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
        sys.exit()