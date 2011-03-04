import os

# Make sure to turn this up when you're done testing
VOLUME_PERCENT = 0

# FILL IN YOUR INFORMATION BELOW
#####################################################################
INSTALL_DIRECTORY = "" #parent directory: "<your_file_system>/laptop-alarm/"
PICTURES_PATH = ""
FROM_EMAIL_ADDRESS = "username@gmail.com" #only gmail for now
TO_EMAIL_ADDRESS = "" #phone_number@vzwpix.com, etc.
USERNAME = ""
#TODO: Store passwords in gnome/kde keyring
PASSWORD = "" #use base64.b64encode("PASSWORD")
#######################################################################
# END REQUIRED INFORMATION

AUDIO_FILE = os.path.join(INSTALL_DIRECTORY, "caralarm.mp3")
PICTURES_FILE_EXTENSION = "jpeg"
# for lock screen (default is preyrocks)
HASHED_PASSWORD = 'e75f0173be748b6f68b3feb61255693c'
#TODO: use string instead of file for email text?
TEXT_MESSAGE = os.path.join(INSTALL_DIRECTORY, "letter.txt")
