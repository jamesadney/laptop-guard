============
Laptop Guard 
============
A laptop alarm system that locks your computer and sounds 
an alarm if triggered.

Introduction
============

What triggers the alarm?
------------------------

- Unplugging the computer from ac power
- Pressing the power button (at least on my computer)
- Pressing ctrl + alt keys at the same time
- Shutting the lid of the computer

What happens when the alarm is triggered?
-----------------------------------------

- An alarm sound is played.
- A picture is taken with the computer's webcam.
- The picture is sent to an email or phone.
    
*WARNING: There are bugs in this code and it is somewhat Ubuntu/Debian and 
Gnome dependent at the moment.*

Current Dependencies (will probably change)
-------------------------------------------

- python2.6
- python-dbus
- python-gtk2
- pulseaudio-utils
- python-gst0.10
- streamer

Installation Instructions (Ubuntu)
==================================

Simple
------

1. Extract the downloaded package
2. Open the folder you extracted
3. Open ubuntu-automated-install and select the "run" option
4. Enter your user account password

Do everything seperately
------------------------

1. Install dependencies::

    sudo apt-get install streamer python-gst0.10 python-dbus python-gtk2 pulseaudio-utils
2. Extract tar.gz file
3. Move into directory and run install script as root::

    cd laptop-guard
    sudo ./install.sh
    
Usage
=====

1. Run command::
    laptop-guard
2. Configure settings by clicking on button in bottom left corner of window.
    
If you want alerts (and the photo of your thief) to go to your phone rather
than an email address, use the email address associated with your phone in
the "To address:" field.

For example: if Verizon is your phone carrier and (555)555-5555 is your number,
use 5555555555@vzwpix.com

- The username and password refer to those of your outgoing mail account (for 
sending text message alert).The password is not securely stored (simply encoded using base64).  Soon this will be
saved in the gnome-keyring.

- ONLY GMAIL is supported right now because this is what I have and I wrote the
program just for myself at first. This will be more generic in the future.

- It is important to remember the "Lock Screen Password"!! The default is 
"password"
