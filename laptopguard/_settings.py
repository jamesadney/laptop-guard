# Modified from D-FEET #
#
#
#    THIS FILE IS PART OF THE D-FEET PROJECT AND LICENSED UNDER THE GPL. SEE
#    THE 'COPYING' FILE FOR DETAILS
#
#   portions taken from the Jokosher project
#
#

import ConfigParser
import os


class Settings:

    """
    Handles loading/saving settings from/to a file on disk.
    """

    instance = None

    # the different settings in each config block
    general = {
        "alarm_volume": 100,
        "pictures_directory": os.path.expanduser("~/Pictures"),
        "to_address": "",
        "from_address": "",
        "username": "",
        "password": "cGFzc3dvcmQ=",  # "password"
        "media_path": "/usr/local/laptop-guard/media/",
        "ui_path": "/usr/local/laptop-guard/ui",
        "audio_file": "caralarm.ogg",
        "text_message": "Laptop Alarm!!",
        "pictures_file_extension": "jpeg",
        "lockscreen_password": "password",
        "smtp_server": "smtp.gmail.com",
        "port": "587",
        "use_tls": True
    }

    def __init__(self, filename=None):
        """
        Creates a new instance of Settings.

        Parameters:
            filename -- path to the settings file.
                        If None, the default ~/.laptop-guard/config will be used.
        """
        if not filename:
            self.filename = os.path.expanduser("~/.laptop-guard/config")
        else:
            self.filename = filename
        self.config = ConfigParser.ConfigParser()

        self.read()

    @classmethod
    def get_instance(cls):
        """ This class is a singlton so use this method to get it """

        if cls.instance:
            return cls.instance

        cls.instance = Settings()
        return cls.instance

    def read(self):
        """
        Reads configuration settings from the config file and loads
        then into the Settings dictionaries.
        """
        self.config.read(self.filename)

        if not self.config.has_section("General"):
            self.config.add_section("General")

        for key, value in self.config.items("General"):
            if key.endswith('list'):
                value = value.split(',')

            self.general[key] = value

    def write(self):
        """
        Writes configuration settings to the Settings config file.
        """
        for key in self.general:
            if key.endswith('list'):
                self.general[key] = ','.join(self.general[key])

            self.config.set("General", key, self.general[key])

        # make sure that the directory that the config file is in exists
        new_file_dir = os.path.split(self.filename)[0]
        if not os.path.isdir(new_file_dir):
            os.makedirs(new_file_dir)
        file = open(self.filename, 'w')
        self.config.write(file)
        file.close()
