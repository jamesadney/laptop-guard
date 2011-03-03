import subprocess
import re

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
