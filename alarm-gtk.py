#!/usr/bin/python

# laptop-alarm
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

import pygtk
pygtk.require('2.0')
import gtk
import dbus

import os, sys

import alarm, settings

class App:
    def __init__(self, ignore_battery=False):
        
        self.ignore_battery = ignore_battery
        self.alarm = alarm.Alarm()
        
        self.session_bus = dbus.SessionBus()
        self.dbus_object  = self.session_bus.get_object("org.theftalarm.Alarm","/")
        
        self.builder = gtk.Builder()
        self.builder.add_from_file("alarm.glade")
        self.builder.connect_signals(self)
        self.main_window = self.builder.get_object("main_window")
        
        self.set_button = self.builder.get_object("set_btn")
        self.unset_button = self.builder.get_object("unset_btn")
        
        self.main_window.show_all()
        
    def on_main_window_destroy(self, widget, *args):
        print "Destroy signal occurred"
        gtk.main_quit()
    
    def on_set_btn_clicked(self, widget):
        
        if (not self.ignore_battery and 
            self.dbus_object.IsOnBattery(dbus_interface="org.theftalarm.Alarm.Service")):
            print "error: can't set alarm when unplugged"
            dialog = gtk.MessageDialog(parent=self.main_window,
                                       flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                                       type=gtk.MESSAGE_ERROR,
                                       buttons=gtk.BUTTONS_CLOSE,
                                       message_format="Please plug in laptop before setting alarm")
            dialog.connect("response", self.close_dialog)
            dialog.set_title("Error: Cannot Set Alarm")
            dialog.show()

        else:
            widget.set_sensitive(False)
            self.unset_button.set_sensitive(True)
            
            self.alarm.initialize()
            
    def close_dialog(self, dialog, response_id):
        print "Dialog: {0}, ID: {1}".format(dialog, response_id )
        dialog.destroy()
        
    def on_unset_btn_clicked(self, widget):
        widget.set_sensitive(False)
        self.set_button.set_sensitive(True)
        
        self.alarm.unset()
    
    def on_prefs_btn_clicked(self, widget):
        pass
    
    def on_about_btn_clicked(self, widget):
        about_dialog = self.builder.get_object("about_dialog")
        about_dialog.show_all()
    
    def on_close_btn_clicked(self, widget):
        gtk.main_quit()
    
    def on_about_dialog_close(self, widget):
        print "About button close"
    
    def on_about_dialog_response(self, dialog, response_id):
        print "About Button Response"
        dialog.hide()

if __name__ == "__main__":
    battery_arg = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "--ignore-battery":
            battery_arg = True
        elif False:
            pass
        else:
            print "\nError please use following supported arguments:\n"
            print "alarm-gtk.py"
            print "alarm-gtk.py --ignore-battery"
            sys.exit()
    
    app = App(battery_arg)
    gtk.main()
    
    
