import speech_recognition as sr


def transcription():
    print("starting transcription")

    r = sr.Recognizer()

    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        # print("Recognizing...")
        # convert speech to text
        text = r.recognize_google(audio_data)
        print(text)

        if "walked" in text:
            requests.post(firststanza_6)
        elif "saw" in text:
            requests.post(secondstanza_7)
        elif "wanted" in text:
            requests.post(thirdstanza_8)
        elif "up" in text:
            requests.post(fourthstanza_9)
        elif "planted" in text:
            requests.post(fifthstanza_10)


if __name__ == "__main__":
    transcription()