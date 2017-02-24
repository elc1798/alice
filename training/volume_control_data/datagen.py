import re

graph = {
    "ROOT" : [ "turn", "make", "decrease", "increase" ],
    "turn" : [ "up1", "down1", "the2" ],
    "up1" : [ "the1" ],
    "down1" : [ "the1" ],
    "the1" : [ "tunez1", "volume1", "sound1", "beat1", "tune1", "tunes1",
        "music1", "song1" ],
    "tunez1" : [ "STOP" ],
    "volume1" : [ "STOP" ],
    "sound1" : [ "STOP" ],
    "beat1" : [ "STOP" ],
    "tune1" : [ "STOP" ],
    "tunes1" : [ "STOP" ],
    "music1" : [ "STOP" ],
    "song1" : [ "STOP" ],
    "the2" : [ "tunez2", "volume2", "sound2", "beat2", "tune2", "tunes2",
        "music2", "song2" ],
    "tunez2" : [ "up2", "down2" ],
    "volume2" : [ "up2", "down2" ],
    "sound2" : [ "up2", "down2" ],
    "beat2" : [ "up2", "down2" ],
    "tune2" : [ "up2", "down2" ],
    "tunes2" : [ "up2", "down2" ],
    "music2" : [ "up2", "down2" ],
    "song2" : [ "up2", "down2" ],
    "up2" : [ "STOP" ],
    "down2" : [ "STOP" ],
    "make" : [ "the3" ],
    "the3" : [ "tunez3", "volume3", "sound3", "beat3", "tune3", "tunes3",
        "music3", "song3" ],
    "tunez3" : [ "louder", "softer", "quieter", "lower", "higher" ],
    "volume3" : [ "louder", "softer", "quieter", "lower", "higher" ],
    "sound3" : [ "louder", "softer", "quieter", "lower", "higher" ],
    "beat3" : [ "louder", "softer", "quieter", "lower", "higher" ],
    "tune3" : [ "louder", "softer", "quieter", "lower", "higher" ],
    "tunes3" : [ "louder", "softer", "quieter", "lower", "higher" ],
    "music3" : [ "louder", "softer", "quieter", "lower", "higher" ],
    "song3" : [ "louder", "softer", "quieter", "lower", "higher" ],
    "louder" : [ "STOP" ],
    "softer" : [ "STOP" ],
    "quieter" : [ "STOP" ],
    "lower" : [ "STOP" ],
    "higher" : [ "STOP" ],
    "decrease" : [ "the1" ],
    "increase" : [ "the1" ]
}

data_list = []

queue = [ ("ROOT", "") ]
def bfs():
    global queue, data_list
    while len(queue) > 0:
        current = queue.pop(0)

        for item in graph[current[0]]:
            if item == "STOP":
                data_list.append( current[1] )
                data_list.append( "can you " + current[1] )
                data_list.append( "can you please " + current[1] )
                data_list.append( current[1] + " please" )
            else:
                queue.append( (item, " ".join((current[1], item)).strip()) )

bfs()

with open("true.txt", 'w') as f:
    f.write( re.sub(r'\d+', '', "\n".join(data_list)))

