# mqpb
mqtt play back? Don't remember the acronym anymore

Basically a minimalistic vlc interface for mqtt.
Primary intended as a network controlled soundboard, but could be used to implement (multi) room streaming as well.

## install
1. modify settings.py
2. install dependencies (https://github.com/oaubert/python-vlc + paho-mqtt and)

## how to use
1. run the script

## mqtt
The script provides multiple mqtt endpoints:
- **play** (payload is the path to a local media file)
- **stream** (payload is a streaming url)
- **update** (no payload required, updates the *files* topic)
- **stop** (no payload required, stops the current play back)

It also pushes the local media files as json to **files** on start up and updates it after receiving a 'update' msg.
 
