#!/usr/bin/env python

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

import gobject

import dbus.service
import dbus.mainloop.glib

class DBusService(dbus.service.Object):
    def __init__(self, conn, object_path, check_battery=True, check_lid=True):
        dbus.service.Object.__init__(self, conn, object_path)
        
        self.loop = gobject.MainLoop()
    
        gobject.timeout_add(200, self.get_properties)
        
        system_bus = dbus.SystemBus()
        self.upower_object = system_bus.get_object('org.freedesktop.UPower', 
                                   '/org/freedesktop/UPower')
        self.upower_interface = dbus.Interface(self.upower_object, 
                                               'org.freedesktop.DBus.Properties')
        
        self.__signal_sent = False
        self.check_battery = check_battery
        self.check_lid = check_lid
    
    @dbus.service.signal(dbus_interface='org.theftalarm.Alarm.Service')
    def TriggerAlarm(self, reason):
        
        if reason == "Unplugged":
            print "Signal: AC Unplugged!"
        elif reason == "LidClosed":
            print "Signal: Lid was closed!"
        elif reason == "PowerButtonPressed":
            print "Signal: Power button was pressed"
            
        self.__signal_sent = True    
        return "Trigger Alarm!"
    
    #TODO: Only send signals one time in a row?    
    @dbus.service.method(dbus_interface='org.theftalarm.Alarm.Service')
    def IsOnBattery(self):
        
        print "Checking Battery"
        battery_state = self.upower_interface.Get('org.freedesktop.UPower', 'OnBattery')
        
        # No real improvements using this method (more universal?)
        # maybe faster, try without sending signal
#        battery_state_file = open("/proc/acpi/ac_adapter/ACAD/state")
#        battery_state_text = battery_state_file.read().split()[1]
#        if battery_state_text == "off-line":
#            battery_state = True
#        elif battery_state_text == "on-line":
#            battery_state = False
#        else:
#            print "Error determining battery state"
#            raise AttributeError

        if battery_state:
            self.TriggerAlarm("Unplugged")
        
        return battery_state
    
    @dbus.service.method(dbus_interface='org.theftalarm.Alarm.Service')
    def IsLidClosed(self):
        
        print "Checking Lid"
        lid_closed = self.upower_interface.Get('org.freedesktop.UPower', 'LidIsClosed')
        if lid_closed:
            self.TriggerAlarm("LidClosed")
        
        return lid_closed
    
    @dbus.service.method(dbus_interface='org.theftalarm.Alarm.Service')
    def Reset(self):
        """
        Send a signal next time even if it's redundant
        """
        self.__signal_sent = False
        
    @dbus.service.method(dbus_interface='org.theftalarm.Alarm.Service')
    def ManuallyTrigger(self):
        
        if not self.__signal_sent:
            self.TriggerAlarm("PowerButtonPressed")
            return "alarm manually triggered"
        else:
            print "signal already sent"
    
    def get_properties(self):
        
        self.upower_properties = self.upower_interface.GetAll('org.freedesktop.UPower')
        
        self.send_signals()
        
        for key in self.upower_properties:
            print key, self.upower_properties[key]
            
        return True
    
    def send_signals(self):
        
        if self.check_battery and self.upower_properties['OnBattery']:
            if not self.__signal_sent:
                print "On battery power"
                self.TriggerAlarm("Unplugged")
        elif self.check_lid and self.upower_properties['LidIsClosed']:
            if not self.__signal_sent:
                print "Lid is closed"
                self.TriggerAlarm("LidClosed")
    
    def start(self):
        
        try:
            self.loop.run()
        except KeyboardInterrupt:
            self.Exit()
    
    @dbus.service.method(dbus_interface='org.theftalarm.Alarm.Service')
    def Exit(self):
        
        print "Exiting Alarm Service"
        self.loop.quit()

if __name__ == "__main__":

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName('org.theftalarm.Alarm', session_bus)
    service_instance = DBusService(name, '/')
    service_instance.start()
