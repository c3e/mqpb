#!/usr/bin/python3
import os
import sys
import logging
import json

import vlc
import paho.mqtt.client as mqtt

from settings import *


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,format='%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

def path_to_dict(path):
    """
    building a dict over a given directory
    """
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "dir"
        d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir
(path)]
    else:
        d['type'] = "file"
    return d


logging.debug("Current media files:")
logging.debug(path_to_dict(MEDIA_PATH))

instance = vlc.Instance()
player = instance.media_player_new()


def on_connect(client, userdata, flags, rc):
    logging.debug("Connected with result code " + str(rc))

    client.subscribe(MQTT_TOPIC + "#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if msg.topic.endswith('play'):
        path = msg.payload.decode('UTF-8')
        path = path.replace("..", "").replace(";", "").lower()
        if path[0].isalnum():
            try:
                media = instance.media_new(MEDIA_PATH + path)
                player.set_media(media)
                player.play()
                logging.debug('start playback of %s' % path)
            except:
                logging.error("failed to play file: %s" % path)
    elif msg.topic.endswith('stream'):
        try:
            media = instance.media_new(msg.payload.decode('UTF-8'))
            media.get_mrl()
            player.set_media(media)
            player.play()
            logging.debug('start stream of: %s' % msg.payload.decode('UTF-8'))
        except:
            logging.error("failed to stream: %s" % msg.payload.decode('UTF-8'))
    elif msg.topic.endswith('stop'):
        print('stop playback')
        player.stop()
    elif msg.topic.endswith('update'):
        logging.debug("publish current files")
        client.publish(MQTT_TOPIC + "files", json.dumps(path_to_dict(MEDIA_PATH), retain=True))

client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

client.loop_forever()
