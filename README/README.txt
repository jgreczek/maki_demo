Maki Demo:

Running the demo:
The maki_demo package contains the files to play audio and control maki behaviours using cordial_maki and cordial_sound.
The maki_test.py node can be used to deploy sound and actions to maki.
After the maki_cordial_server.py and soundplay_node.py nodes are started, the maki_test.py node can be run.

The sound file to be played and the action to be done can be changed in the maki_test.py code.
Even the number of times and interval of the behaviour can be changed.

All the audio files of the sentences narrated are stored in the cordial_sound package under sounds.
These sound files are played from the iVona text to speech converter website using Ivy kid voice and are recorded using audacity.

All the actions which can be used are the sequences defined in maki.ppr. 
They should even be declared under the 'motions' variable in maki_cordial_server.
If the actions are not working then either they/their poses are not defined in the maki.ppr properly or not included in maki_cordial_server.

Running the demo using launch file:
The same function as above can be run using the launch file too which is not preferable.
The test.py node has the list of sentences and it calls the maki_demo.launch file for each sentence.
The launch file deploys two nodes, sub.py which plays the requested sentence and is written in cordial_sound and 
maki_test2.py which changes the behaviour of maki. The type of behaviour should be defined inside the maki_test2.py.
