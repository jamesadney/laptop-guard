============
Laptop Guard 
============
A laptop alarm system that locks your computer and sounds 
an alarm if triggered.

*This project is at an early stage, so expect bugs.  That being said, it should
work on most systems*

Introduction
============

What triggers the alarm?
------------------------

- Unplugging the computer from ac power
- Pressing the power button (at least on my computer)
- Pressing ctrl & alt keys at the same time
- Shutting the lid of the computer

What happens when the alarm is triggered?
-----------------------------------------

- An alarm sound is played.
- A picture is taken with the computer's webcam.
- The picture is sent to an email or phone.

Current Dependencies (will probably change)
-------------------------------------------

- python2.6
- python-dbus
- python-gtk2
- pulseaudio-utils
- python-gst0.10
- python-opencv

Installation Instructions
=========================

Simple (Tested on Ubuntu 10.04 & 10.10)
---------------------------------------

1. Extract the downloaded package
2. Open the folder you extracted
3. Open ubuntu-automated-install and select the "run" option
4. Enter your user account password

Do everything separately (Ubuntu and probably Debian in general)
----------------------------------------------------------------

1. Install dependencies::

    sudo apt-get install streamer python-gst0.10 python-dbus python-gtk2 pulseaudio-utils
2. Extract tar.gz file
3. Move into directory and run install script as root::

    cd <folder-you-extracted-into>
    sudo ./install.sh

Installation on Fedora (tested with 14)
---------------------------------------

1. Install dependencies::

    su root
    yum install opencv-python
2. Extract tar.gz file
3. Run install script (as root)::

    cd <folder-you-extracted-into>
    ./install.sh  
    
Usage
=====

Run this command to start the application::

    laptop-guard
    
You should configure the alarm settings (by clicking the button in the bottom-
left corner of the main window) the first time you run the program.

Configuration
=============

General
-------

======================  ========================================================
Setting                 Description
======================  ========================================================
Alarm Volume            If the alarm is activated, this will be the volume of 
                        the alarm sound.  You should leave this high except when 
                        testing the alarm.
Pictures Directory      On activation, the program takes pictures and stores
                        them in this directory.  These are overwritten each time
                        the alarm is activated.
Lock Screen Password    This is the password you will need to give in order to
                        unlock your computer after setting your alarm.
======================  ========================================================

Text Messaging
--------------

======================  ========================================================
Setting                 Description
======================  ========================================================
To Email Address        This is the email address that will receive the picture
                        and alert which is sent when the alarm is activated.
                        **You can ideally use your cell phone to receive 
                        this message depending on your service provider.** For 
                        example: if your provider is verizon you would put this 
                        email here <your-phone-#>@vzwpix.com
From Email Address      This is the email address that you want the message to 
                        come from.  To be safe, use an email address that
                        corresponds with the domain of your outgoing mail server.
                        *Mail server configuration has not yet been implemented*
======================  ========================================================

Email Account
-------------

======================  ========================================================
Setting                 Description
======================  ========================================================
Username                The username for your mail account. **Only gmail is
                        supported as of now**
Password                The password corresponding with your email account.
                        *This is stored in a non-human-readable form, however it
                        is not encrypted.  Soon it will be saved using gnome 
                        keyring.*
======================  ========================================================
