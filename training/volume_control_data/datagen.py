# Procedurally generate dataset using state diagram / graph implementation
# YES, i know I didn't make the graph correctly, and there's some grammatically
# incorrect traversals. I just wanted to save some time.

graph = {
    "ROOT" : [ "turn", "make", "increase", "decrease", "increase", "lower",
        "higher"],
    "turn" : [ "up", "down", "the"],
    "make" : [ "the" ],
    "up" : [ "the", "tunez", "volume", "sound", "beat", "tune", "tunes", "music",
        "song" ],
    "down": [ "the", "tunez", "volume", "sound", "beat", "tune", "tunes", "music",
        "song" ],
    "the" : [ "tunez", "volume", "sound", "beat", "tune", "tunes", "music",
        "song" ],
    "tunez" : [ "louder", "softer", "quieter", "lower", "higher", "STOP"],
    "volume" : [ "louder", "softer", "quieter", "lower", "higher", "STOP" ],
    "sound" : [ "louder", "softer", "quieter", "lower", "higher", "STOP" ],
    "beat" : [ "louder", "softer", "quieter", "lower", "higher", "STOP" ],
    "tune" : [ "louder", "softer", "quieter", "lower", "higher", "STOP" ],
    "tunes" : [ "louder", "softer", "quieter", "lower", "higher", "STOP" ],
    "music" : [ "louder", "softer", "quieter", "lower", "higher", "STOP" ],
    "song" : [ "louder", "softer", "quieter", "lower", "higher", "STOP" ],
    "decrease" : [ "the", "volume", "sound", "tunes", "music" ],
    "increase" : [ "the", "volume", "sound", "tunes", "music" ],
    "lower" : [ "the", "volume", "sound", "tunes", "music" ],
    "higher" : [ "the", "volume", "sound", "tunes", "music" ],
    "louder" : ["STOP"],
    "softer" : ["STOP"],
    "quieter" : ["STOP"],
    "lower" : ["STOP"],
    "higher" : ["STOP"],
    "STOP" : []
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
    f.write( "\n".join(data_list) )

