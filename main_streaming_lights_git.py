import time
##libraries necessary to clean up data
import json

##and push the virtual button
import requests

import threading

import pyaudio
import websocket
from google.cloud import speech

import os

import speech_recognition as sr




# REPLACE WITH YOUR KEY
API_KEY = os.environ["DEEPTONE_API"]
# Send a message to the API every 4.096 seconds. Lower this number if you want a lower latency has to be a multiple of 1024
CHUNK_SIZE = 4096

# Define microphone input stream
pa = pyaudio.PyAudio()
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=CHUNK_SIZE,
)
r = sr.Recognizer()
"""
def get_largest_emotion(dict_input):
    """
"""
This is a function to read and find the greatest value in a (any) dictionary
    Iterates through each value and checks if it's greater than zero (initially) and makes it the new max_value
    Outputs the final (greater than all others) dictionary key
   """
"""
    max_value = -1
    max_key = None
    for k, v in dict_input.items():
        if v > max_value:
            max_value = v
            max_key = k
    return max_key
"""

def update_lights(message):

    """
    Takes the json data we are streaming and filters out the junk and then presses button based on highest emotion
    """
    out = json.dumps(message)
    #print(out)

    if "irritated" in out:
        print("irritated")
        requests.post(irritated_1)
    elif "tired" in out:
        requests.post(tired_2)
        print("tired")
    elif "neutral" in out:
        requests.post(neutral_3)
        print("neutral")
    elif "happy" in out:
        requests.post(happy_4)
        print("happy")
    elif "no_speech" in out:
        requests.post(no_speech_5)
        print("no speech")


    """
    emotions_dict = dict(out["message_type"]["channels"]["0"]["timestamp"]["emotions"])
    emotions_dict.pop("no_speech_fraction", None)
    emotions_dict.pop("silence_fraction", None)
    max_emo = get_largest_emotion(emotions_dict)
    print(max_emo)
    if max_emo == "irritated_fraction":
        requests.post(irritated_1)
    elif max_emo == "tired_fraction":
        requests.post(tired_2)
    elif max_emo == "neutral_fraction":
        requests.post(neutral_3)
    elif max_emo == "happy_4":
        requests.post(happy_4)
    """
def transcribe(audio_data):

    text = r.recognize_google(audio_data)
    print(text)


# What to do with results
def on_message(ws, message):
    print(message)
    update_lights(message)
    #transcribe(stream)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")




# Once websocket connection is established start sending microphone input stream
def on_open(ws):
    stream.start_stream()

    def run():
        while stream.is_active():
            data = stream.read(CHUNK_SIZE)
            ws.send(bytearray(data), websocket.ABNF.OPCODE_BINARY)
            #data_bytes = data
            #print(data[:128])
            #transcribe(sr.AudioData(data_bytes, 48000, 2))

        ws.close()

    thread = threading.Thread(target=run)
    thread.start()

"""after models= choose the models to use.

Options are gender, emotions, arousal"""


if __name__ == "__main__":
    ws = websocket.WebSocketApp(f"wss://api.oto.ai/stream?models=emotions&output_period={CHUNK_SIZE}&volume_threshold=0.0",
                                header={'X-API-KEY': API_KEY},
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

"""
with sr.Microphone() as source:
    # read the audio data from the default microphone
    audio_data = r.record(source, duration=5)
    print("Recognizing...")
    # convert speech to text
    text = r.recognize_google(audio_data)
    print(text)
"""

