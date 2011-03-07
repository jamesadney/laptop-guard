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

import subprocess
import re

#FIXME: doesn't work when music is playing (does it work when not muted in general)
def get_system_info():
    p = subprocess.Popen(["pactl", "list"], stdout=subprocess.PIPE)
    audio_data = p.stdout
    
    #TODO: use readlines to simplify regular expression?
    #TODO: just use search and line numbers instead of re?
    audio_data = audio_data.read()
    
    #TODO: how to skip lines in a better way
    #TODO: get volume percents in a better way
    r = re.search(r"""^Sink\ \#(?P<sink>\d)       # Get Sink number
                  .+                         
                  ^\tMute:\ (?P<mute>[a-z]+)        # is muted?
                  .+                        
                  ^\tVolume.+\ {2}(?P<volume>\d+)%  # get volume
                  """, audio_data, re.M | re.X | re.S)
                  
    master_sink = r.group("sink")
    muted = r.group("mute")
    if muted.lower() == "yes":
        muted = True
    elif muted.lower() == "no":
        muted = False
    else:
        print "Error retrieving muted info"
    
    previous_volume_percent = int(r.group("volume"))
    
    return master_sink, muted, previous_volume_percent

if __name__ == "__main__":
    print get_system_info()
