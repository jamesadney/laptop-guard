#!/usr/bin/env python
#
# Prey Linux Lock
# By Tomas Pollak - (c) 2010 Fork Ltd.
# http://preyproject.com
# GPLv3 Licence
#

import os
import sys
import hashlib
import gtk
import pango
import dbus


class Lock:

    def get_md5(self, string):
        return hashlib.md5(string).hexdigest()

    def enter_callback(self, entry):

        # old hashed password ##
        # hashed_text = self.get_md5(entry.get_text())
        # print hashed_text

        password = entry.get_text()

        if password != self.password:
            print " -- Bad password attempt."
            self.label.show()
            return True
        else:
            print ' -- Correctomondo. PC Unlocked.'
            self.bg_window.hide()
            self.window.hide()

    def on_delete_event(self, widget, event):
        return True
        # self.window.set_keep_above(True)

    def on_focus_change(self, widget, event):
        print " -- Focus changed."
        return True

    def on_window_state_change(self, widget, event):
        self.window.activate_focus()
        print " -- Something happened."
        return False

    def on_key_press(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
#        print "Key %s (%d) was pressed" % (keyname, event.keyval)

        if event.keyval == 269025066:
            self.dbus_object.ManuallyTrigger(dbus_interface='org.theftalarm.Alarm.Service')
            print "Power Button Pressed, activating alarm"

        if event.keyval > 65470 and event.keyval < 65481:  # F1 through F12
            print "Key %s (%d) was pressed" % (keyname, event.keyval)
            # return True
        if event.state & gtk.gdk.CONTROL_MASK:
            print "Control was being held down"
            if event.keyval == 65513 or event.keyval == 65027:
                self.dbus_object.ManuallyTrigger(dbus_interface='org.theftalarm.Alarm.Service')
                print "ctrl+alt pressed, activating alarm"
            # return True
        # FIXME: doesn't work with right alt
        if event.state & gtk.gdk.MOD1_MASK:
            print "Alt was being held down"
            if event.keyval == 65507 or event.keyval == 65508:
                self.dbus_object.ManuallyTrigger(dbus_interface='org.theftalarm.Alarm.Service')
                print "ctrl+alt pressed, activating alarm"
            # return True
        if event.state & gtk.gdk.SHIFT_MASK:
            print "Shift was being held down"

    def __init__(self, password, working_directory):

        # set up dbus stuff for theft-alarm
        self.session_bus = dbus.SessionBus()
        self.dbus_object = self.session_bus.get_object("org.theftalarm.Alarm", "/")

        self.password = password

        # calculate number of screens
        width = gtk.gdk.screen_width()
        height = gtk.gdk.screen_height()

        black = gtk.gdk.color_parse("black")

        #
        # black bg
        #

        self.bg_window = gtk.Window(gtk.WINDOW_POPUP)
        self.bg_window.modify_bg(gtk.STATE_NORMAL, black)
        self.bg_window.resize(width, height)
        self.bg_window.set_deletable(False)
        self.bg_window.show()

        monitors = self.bg_window.get_screen().get_n_monitors()

        #
        # window
        #

        self.window = gtk.Window(gtk.WINDOW_POPUP)
        self.window.set_title("Prey Lock")
        self.window.modify_bg(gtk.STATE_NORMAL, black)

        # prevents window from being closed
        self.window.connect("delete_event", self.on_delete_event)
        # capture keypresses
        self.window.connect("key_press_event", self.on_key_press)

        self.window.stick()
        self.window.set_deletable(False)
        # self.window.set_focus_on_map(True)
        self.window.set_decorated(False)
        self.window.set_border_width(0)
        self.window.set_keep_above(True)
        self.window.set_resizable(False)
        # self.window.fullscreen()

        main_screen_width = self.window.get_screen().get_monitor_geometry(0).width
        main_screen_height = self.window.get_screen().get_monitor_geometry(0).height
        main_screen_middle = main_screen_width/2

        vbox = gtk.VBox(False, 0)
        self.window.add(vbox)
        # vbox.show()

        #
        # background color and image
        #

        image_directory = os.path.join(working_directory, "share/laptop-guard/media/")

        image = gtk.Image()
        bg_path = os.path.join(image_directory, "locked.png")
        image.set_from_file(bg_path)
        image.show()
        vbox.set_size_request(main_screen_width, main_screen_height)
        vbox.add(image)

        #
        # label
        #

        hbox = gtk.HBox(False, 0)
        vbox.add(hbox)
        hbox.show()

        self.entry = gtk.Entry(max=0)
        self.entry.set_max_length(40)

        self.entry.set_inner_border(None)
        self.entry.set_width_chars(24)
        self.entry.set_visibility(False)
        # self.entry.set_has_frame(False)
        self.entry.modify_font(pango.FontDescription("sans 20"))
        self.entry.set_flags(gtk.CAN_FOCUS | gtk.HAS_FOCUS | gtk.HAS_GRAB | gtk.CAN_DEFAULT | gtk.SENSITIVE)

        # BUG! original version had self.entry as last callback
        # TODO: fix bug upstream
        self.entry.connect("activate", self.enter_callback)
        # self.entry.show()

        fixed = gtk.Fixed()
        fixed.put(self.entry, main_screen_middle-240, -(main_screen_height/2) - 40)
        fixed.show()
        hbox.pack_start(fixed, False, False, 30)

        text = 'Invalid password. Access denied.'
        self.label = gtk.Label()
        self.label.set_markup('<span foreground="#aa0000">'+text+'</span>')
        self.label.modify_font(pango.FontDescription("sans 20"))
        self.label.set_size_request(main_screen_width, 30)

        fixed2 = gtk.Fixed()
        fixed2.put(self.label, -main_screen_width/2-240, -(main_screen_height/2)+60)
        hbox.pack_start(fixed2, True, False, 30)

        self.window.show_all()
        self.window.set_focus(self.entry)
        gtk.gdk.keyboard_grab(fixed.window, True)
        self.label.hide()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        passwd = 'preyrocks'  # preyrocks
        # print 'No password specified.'
        # os._exit(1)
    else:
        passwd = sys.argv[1]

    lock = Lock(passwd)
    gtk.main()
