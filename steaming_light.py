import os
import json
import threading

# import requests
import pyaudio
import websocket

# from google.cloud import speech

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
# r = sr.Recognizer()


def update_lights(message):

    """
    Takes the json data we are streaming and filters out the junk and then presses button based on highest emotion
    """
    out = json.dumps(message)
    print(out)

    if "irritated" in out:
        print("irritated")
        # requests.post(irritated_1)
    elif "tired" in out:
        # requests.post(tired_2)
        print("tired")
    elif "neutral" in out:
        # requests.post(neutral_3)
        print("neutral")
    elif "happy" in out:
        # requests.post(happy_4)
        print("happy")
    elif "no_speech" in out:
        # requests.post(no_speech_5)
        print("no speech")


# What to do with results
def on_message(ws, message):
    print(message)
    update_lights(message)


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
            byte_stream = bytearray(data)
            print(byte_stream)

            print("streamtype")
            print(type(stream))

            print("data")
            print(type(data))
            print(data)

            ws.send(byte_stream, websocket.ABNF.OPCODE_BINARY)
            # aud = sr.AudioData(data, 16000 * 4, 2)
            aud = sr.Microphone.MicrophoneStream(data)
            transcription(aud)
            # data_bytes = data
            # print(data[:128])
            # transcribe(sr.AudioData(data_bytes, 48000, 2))

        ws.close()

    thread = threading.Thread(target=run)
    thread.start()


def transcription(data):
    print("starting transcription")

    r = sr.Recognizer()
    # audio_data = r.record(data, duration=5)
    # r.record(source)
    text = r.recognize_google(data)
    print(text)

    # with sr.Microphone() as source:
    #     # read the audio data from the default microphone
    #     audio_data = r.record(source, duration=5)
    #     # print("Recognizing...")
    #     # convert speech to text
    #     text = r.recognize_google(audio_data)
    #     print(text)

    #     if "walked" in text:
    #         requests.post(firststanza_6)
    #     elif "saw" in text:
    #         requests.post(secondstanza_7)
    #     elif "wanted" in text:
    #         requests.post(thirdstanza_8)
    #     elif "up" in text:
    #         requests.post(fourthstanza_9)
    #     elif "planted" in text:
    #         requests.post(fifthstanza_10)


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        f"wss://api.oto.ai/stream?models=emotions&output_period={CHUNK_SIZE}&volume_threshold=0.0",
        header={"X-API-KEY": API_KEY},
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
