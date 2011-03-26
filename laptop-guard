#!/usr/bin/python

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

import pygtk
pygtk.require('2.0')
import gtk
import dbus

import os
from base64 import b64decode, b64encode

from laptopguard import alarm
from laptopguard._settings import Settings

class App:
    def __init__(self, ignore_battery=False, use_local_dirs=False):
        
        self.ignore_battery = ignore_battery
        
        if use_local_dirs:
            working_directory = os.getcwd()
        else:
            working_directory = None
            
        self.alarm = alarm.Alarm(working_directory)
        
        ## Set up dbus ##
        self.session_bus = dbus.SessionBus()
        self.dbus_object  = self.session_bus.get_object("org.theftalarm.Alarm","/")
        
        ## Load glade file(s) and initialize ##
        self.builder = gtk.Builder()
        
        new_settings = Settings.get_instance()
        if use_local_dirs:
            ui_directory = os.path.join(working_directory, "ui")
        else:
            ui_directory = new_settings.general["ui_path"]
        self.builder.add_from_file(os.path.join(ui_directory, "alarm.glade"))
        
        self.builder.connect_signals(self)
        self._get_builder_objects()

        self._load_settings()
        
        self.main_window.show_all()
        
    def _get_builder_objects(self):
        
        ## Main Window ##
        self.main_window = self.builder.get_object("main_window")
        self.set_button = self.builder.get_object("set_btn")
        self.unset_button = self.builder.get_object("unset_btn")
        
        ## Preferences Window ##
        self.prefs_window = self.builder.get_object("prefs_window")
        self.volume_adjustment = self.builder.get_object("volume_adjustment")
        self.pictures_directory_entry = self.builder.get_object("pictures_directory_entry")
        self.lock_pwd_entry = self.builder.get_object("lock_pwd_entry")
        self.to_address_entry = self.builder.get_object("to_address_entry")
        self.from_address_entry = self.builder.get_object("from_address_entry")
        self.username_entry = self.builder.get_object("username_entry")
        self.password_entry = self.builder.get_object("password_entry")
        self.show_password_box = self.builder.get_object("show_password_box")
        self.smtp_entry = self.builder.get_object("smtp_entry")
        self.port_entry = self.builder.get_object("port_entry")
        self.tls_box = self.builder.get_object("tls_box")
        
        ## About Dialog ##
        self.about_dialog = self.builder.get_object("about_dialog")
        
    def _load_settings(self):
        
        new_settings = Settings.get_instance()
        
        self.alarm_volume = int(new_settings.general["alarm_volume"])
        self.pictures_directory = new_settings.general["pictures_directory"]
        self.lock_password = new_settings.general["lockscreen_password"]
        self.to_address = new_settings.general["to_address"]
        self.from_address = new_settings.general["from_address"]
        self.username = new_settings.general["username"]
        self.password = b64decode(new_settings.general["password"])
        self.smtp_server = new_settings.general["smtp_server"]
        self.port = new_settings.general["port"]
        self.use_tls = bool(new_settings.general["use_tls"])
        
    ## Main window callbacks ##
    
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
        
    def on_unset_btn_clicked(self, widget):
        widget.set_sensitive(False)
        self.set_button.set_sensitive(True)
        
        self.alarm.unset()
    
    def on_prefs_btn_clicked(self, widget):
        print "Preferences Button pushed"
        
        ## Restore settings ##
        self.volume_adjustment.set_value(self.alarm_volume)
        self.pictures_directory_entry.set_text(self.pictures_directory)
        self.lock_pwd_entry.set_text(self.lock_password)
        self.to_address_entry.set_text(self.to_address)
        self.from_address_entry.set_text(self.from_address)
        self.username_entry.set_text(self.username)
        self.password_entry.set_text(self.password)
        self.smtp_entry.set_text(self.smtp_server)
        self.port_entry.set_text(self.port)
        self.tls_box.set_active(self.use_tls)
        
        self.prefs_window.show_all()
        
        # Unset alarm so changes to preferences will apply
        if self.alarm.is_set:
            self.alarm.unset()
            self.set_button.set_sensitive(True)
            self.unset_button.set_sensitive(False)
            
    def on_about_btn_clicked(self, widget):
        self.about_dialog.show_all()
        
    #TODO: redo with glade    
    def close_dialog(self, dialog, response_id):
        print "Destroying battery message dialog"
        dialog.destroy()
        
    def on_close_btn_clicked(self, widget):
        gtk.main_quit()
        
    def on_main_window_destroy(self, widget, *args):
        print "Destroy signal occurred"
        gtk.main_quit()
        
    ## Preferences window callbacks ##
        
    def on_show_password_box_toggled(self, button):
        
        self.show_password = button.get_active()
        if self.show_password:
            self.password_entry.set_visibility(True)
        else:
            self.password_entry.set_visibility(False)
        
    def on_prefs_close_btn_clicked(self, widget):
        self._close_prefs_window()
        
    def on_prefs_window_delete_event(self, widget, *args):
        print "delete event"
        self._close_prefs_window()
        
        # prevent window from being destroyed
        return True
    
    def _close_prefs_window(self):
        
        ## Un-show password ##
        self.password_entry.set_visibility(False)
        self.show_password_box.set_active(False)
        
        new_settings = Settings.get_instance()
        
        ## read values ##
        self.alarm_volume = int(self.volume_adjustment.get_value())
        self.pictures_directory = self.pictures_directory_entry.get_text()
        self.lock_password = self.lock_pwd_entry.get_text()
        self.to_address = self.to_address_entry.get_text()
        self.from_address = self.from_address_entry.get_text()
        self.username = self.username_entry.get_text()
        self.password = self.password_entry.get_text()
        self.smtp_server = self.smtp_entry.get_text()
        self.port = self.port_entry.get_text()
        self.use_tls = self.tls_box.get_active()
        
        #TODO: only update if changed
        ## Save settings ##
        new_settings.general['alarm_volume'] = self.alarm_volume
        new_settings.general['pictures_directory'] = self.pictures_directory
        new_settings.general['lockscreen_password'] = self.lock_password
        new_settings.general['to_address'] = self.to_address
        new_settings.general['from_address'] = self.from_address
        new_settings.general['username'] = self.username
        new_settings.general['password'] = b64encode(self.password)
        new_settings.general['smtp_server'] = self.smtp_server
        new_settings.general['port'] = self.port
        new_settings.general['use_tls'] = self.use_tls
        
        new_settings.write()
        self.prefs_window.hide()
    
    def on_hscale1_format_value(self, scale, value):
        formatted_value = "{0:.0f}%".format(value)
        return formatted_value
    
    ## About dialog callbacks ##
    
    def on_about_dialog_delete_event(self, dialog, *args):
        print "About button delete event"
        dialog.hide()
        return True
    
    def on_about_dialog_response(self, dialog, response_id):
        print "About Button Response"
        dialog.hide()

if __name__ == "__main__":
    
    import optparse

    parser = optparse.OptionParser(usage="%prog [options] [project-file]")
    
    parser.add_option("-l", "--local-dirs", 
                      action="store_true", 
                      dest="use_local_dirs", 
                      help="Use files from the local directory tree")
    
    parser.add_option("--ignore-battery",
                      action="store_true",
                      dest="ignore_battery",
                      help="Allow user to set alarm when on battery power.\n\
                      This will make alarm go off immediately upon it being set.")
    
    options, args = parser.parse_args()      
    
    app = App(options.ignore_battery, options.use_local_dirs)
    gtk.main()
