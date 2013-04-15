#!/usr/bin/python

from distutils.core import setup

setup(name='Laptop Guard',
      version='0.6.3',
      description='A laptop alarm gtk application',
      author='James Adney',
      author_email='jfadney@gmail.com',
      packages=['laptopguard'],
      scripts=['alarm-service', 'laptop-guard'],
      data_files=[('share/laptop-guard/ui', ['ui/alarm.glade']),
                  ('share/laptop-guard/media', ['media/caralarm.ogg',
                                                'media/locked.png']),
                  ('/usr/share/doc/laptop-guard', ['README.rst',
                                                   'TODO']),
                  ('/usr/share/dbus-1/services',
                   ['org.theftalarm.Alarm.service']),
                  ('/usr/share/applications', ['laptop-guard.desktop'])],
      requires=['gobject', 'gst', 'gtk', 'dbus'],
      )
