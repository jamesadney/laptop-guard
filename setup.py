#!/usr/bin/python

from distutils.core import setup

setup(name='Laptop Guard',
      version='0.6',
      description='A laptop alarm gtk application',
      author='James Adney',
      author_email='jfadney@gmail.com',
      packages=['laptopguard'],
      scripts=['alarm-service', 'laptop-guard'],
      data_files=[('laptop-guard/ui', ['ui/alarm.glade']),
                  ('laptop-guard/media', ['media/caralarm.ogg', 
                                          'media/locked.png', 
                             'media/system-lock-screen.svg']),
                  ('/usr/share/doc/laptop-guard', ['COPYING', 'README.rst', 
                                                   'TODO']),
                  ('/usr/share/dbus-1/services', 
                   ['org.theftalarm.Alarm.service'])],
      requires=['gobject', 'gst', 'gtk', 'dbus'],
     )
