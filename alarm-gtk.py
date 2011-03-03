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

class Application:
    def __init__(self, ignore_battery=False):
        
        self.ignore_battery = ignore_battery
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(10)
        self.window.set_title("Laptop Alarm")
    
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
    
        self.set_alarm_button = gtk.Button("Set Alarm")
        self.set_alarm_button.connect("clicked", self.set_alarm)
        self.unset_alarm_button = gtk.Button("Unset Alarm")
        self.unset_alarm_button.connect("clicked", self.unset_alarm)
    
        self.window.add(self.set_alarm_button)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_default_size(200, -1)
        
        #get icon from theme
#        icon_theme = gtk.icon_theme_get_default()
#        try:
#            pixbuf = icon_theme.load_icon("changes-prevent", 48, 0)
#        except gobject.GError, exc:
#            print "can't load icon", exc     
#        self.window.set_icon(pixbuf)
        
        icon_path = os.path.join(os.getcwd(), "system-lock-screen.svg")
        self.window.set_icon_from_file(icon_path)
        
        self.window.show_all()
        
        self.alarm = alarm.Alarm()
        
        self.session_bus = dbus.SessionBus()
        self.dbus_object  = self.session_bus.get_object("org.theftalarm.Alarm","/")

    def set_alarm(self, widget):
        
        if (not self.ignore_battery and 
            self.dbus_object.IsOnBattery(dbus_interface="org.theftalarm.Alarm.Service")):
            print "error: can't set alarm when unplugged"
            dialog = gtk.MessageDialog(parent=self.window,
                                       flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                                       type=gtk.MESSAGE_ERROR,
                                       buttons=gtk.BUTTONS_CLOSE,
                                       message_format="Please plug in laptop before setting alarm")
            dialog.connect("response", self.close_dialog)
            dialog.set_title("Error: Cannot Set Alarm")
            dialog.show()

        else:
            self.window.remove(self.set_alarm_button)
            self.window.add(self.unset_alarm_button)
            self.window.show_all()
            
            self.alarm.initialize()
            
    def close_dialog(self, dialog, response_id):
        print "Dialog: {0}, ID: {1}".format(dialog, response_id )
        dialog.destroy()
        
    def unset_alarm(self, widget):
        self.window.remove(self.unset_alarm_button)
        self.window.add(self.set_alarm_button)
        
        self.alarm.unset()

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"

        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()
#        sys.exit()

    def main(self):
        gtk.main()

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
    
    app = Application(ignore_battery=battery_arg)
    app.main()
    
    
