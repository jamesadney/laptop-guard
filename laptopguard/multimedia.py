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

import subprocess
import os
import audio, playall

class Sound:

    def __init__(self, file_location, volume_percent=100):
    
        self.file_location = file_location
        self.playing = False
        try:
            self.audio_data = audio.get_system_info()
            self.was_muted = self.audio_data[1]
            self.initial_volume = self.audio_data[2]
        except AttributeError:
            print "Error retrieving volume information"
            self.was_muted = True
            self.initial_volume = 40
        
        # unmute and set volume at desired level
        self.__unmute()
        self.__set_volume(volume_percent)
        
        self.player = playall.Player(file_location)

    def play(self):
        """
        Simply plays an audio file using gst
        """
        
        if self.playing:
            print "Sorry, the sound is already playing"
            
        else:
            print "Playing audio file"
            self.player.run()
            self.playing = True
      
    def stop(self):
        """
        Stop playing sound
        """
        if self.playing:
            print "Stopping audio playback"
            self.player.stop()
            self.playing = False
            
        else:
            print "Sorry, nothing is playing"
            
    def __set_volume(self, percentage):
        """
        Set volume level using pulseaudio
        """
        volume_arg = int(percentage / 100.0 * 65536)
        volume_arg = str(volume_arg)
        subprocess.call(["pactl", "set-sink-volume", "0", volume_arg])
        
    def __get_volume(self):
        """
        Get Master Volume
        """
        
    def __is_muted(self):
        """
        Check if master volume control is muted
        """
            
    def __mute(self):
        """
        Mutes sound using pulseaudio
        """
        subprocess.call(["pactl", "set-sink-mute", "0", "1"])
        
    def __unmute(self):
        """
        Unmutes sound using pulseaudio
        """
        subprocess.call(["pactl", "set-sink-mute", "0", "0"])
            
    def __del__(self):
        """
        Make sure to stop playing sound when program exits
        """
        self.stop()
        
        #TODO: restore previous volume settings
        # set volume to 40% and mute
        self.__set_volume(self.initial_volume)
        self.__mute()
        
        
class Webcam:
    """
    Takes pictures with webcam using streamer
    """
    def __init__(self):
        pass
    
    def take_pictures(self, dest_directory=None, file_extension="jpeg"):
        
        if dest_directory:
            os.chdir(dest_directory)
        
        args = ['streamer', '-t', '4', '-r', '2', '-o', 
                'alarmpic0.{0}'.format(file_extension)]
        pics_process = subprocess.Popen(args)
        return pics_process.pid

    
if __name__ == "__main__":
    
    print "doesn't work right unless imported as module'"
