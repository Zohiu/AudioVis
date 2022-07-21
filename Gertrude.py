import speech_recognition as sr
import playsound
import json
import pyttsx3
import os
import wave
from pydub import AudioSegment
from pydub import effects
from gtts import gTTS
import random
from datetime import datetime

r = sr.Recognizer()

engine = pyttsx3.init()

file = open("Data/config.json", "r")
config = json.loads(file.read())
file.close()

def ReloadConfig():
    global config
    file = open("Data/config.json", "r")
    config = json.loads(file.read())
    file.close()

def GetSpeech():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            return r.recognize_google(audio, language="de-DE")
        except sr.UnknownValueError:
            return []

def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

def say(text):
    myobj = gTTS(text=text, lang="de", )

    myobj.save("tts.mp3")

    speed = config["speed"]

    sound = AudioSegment.from_mp3("tts.mp3")
    sound = sound.speedup(speed, 150, 25)
    sound.export("tts.wav", format="wav")

    CHANNELS = 1
    swidth = 2
    Change_RATE = config["pitch"]

    spf = wave.open('tts.wav', 'rb')
    RATE = spf.getframerate()
    signal = spf.readframes(-1)

    wf = wave.open('tts.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE * Change_RATE)
    wf.writeframes(signal)
    wf.close()

    # Playing the converted file
    playsound.playsound('tts.wav', True)
    os.remove("tts.mp3")
    os.remove("tts.wav")

lastjoke = "Ich habe dir noch keinen Witz erzählt."

while True:
    text = str(GetSpeech()).lower()
    print(text)

    if config["name"] in text:
        playsound.playsound('sounds/activation.wav', False)
        ReloadConfig()

        text = str(GetSpeech()).lower()
        print(text)

        if "erzähle mir einen witz" in text or "erzähl mir einen witz" in text or "erzähl einen witz" in text or "erzähle einen witz" in text or "noch einen" in text:
            file = open("Data/witze.json", "r")
            witze = json.loads(file.read())
            file.close()
            print(witze)
            lastjoke = random.choice(witze)
            say(lastjoke)

        elif "wiederhole den witz" in text:
            say(lastjoke)

        elif text.split(" ")[0] == "sage":
            tosay = ""
            for i in range(1, len(text.split(" "))):
                tosay += text.split(" ")[i]
            say(tosay)

        elif "seit wann gibt es dich" in text:
            say("Mich gibt es seit 2021.")

        #elif "was ist mon" in text:
        #    monallgemein = open("Mon.txt", "r")
        #    say(monallgemein.read())

        elif "was sind deine daten" in text:
            say("Meine Daten sind im Moment:"
                "Aktivierungswort: " + str(config["name"]) +
                ". Pitch: " + str(config["pitch"]).replace(".", ",") +
                ". Geschwindigkeit: " + str(config["speed"]).replace(".", ","))

        elif "wie spät ist es" in text:
            now = datetime.now()

            current_time = now.strftime("%H:%M")
            print("Current Time =", current_time)
            say("Es ist " + str(current_time))

        elif "was ist deine lieblingsfarbe" in text:
            say("Ich mag grün, aber noch viel lieber mag ich Nullen und einsen")

        elif "was ist dein lieblingsessen" in text:
            say("Strom natürlich. Was ist deins?")

            playsound.playsound('sounds/activation.wav', False)
            text = str(GetSpeech()).lower()
            print(text)

            try:
                print(text[2])
                say("Oh. Du isst gerne " + text + "? das klingt lecker. Schade, dass ich nur Strom essen kann. " + text + " würde ich auch gerne mal probieren.")
            except:
                say("Du hast nichts gesagt? Naja. Dann hast du anscheinend kein Lieblingsessen. Du solltest mal Strom probieren. Das ist lecker.")

        # IDEE: Wenn eine Frage mit "wie" anfängt, auf google danach suchen ja!

        else:
            try:
                print(text[2])
                say("Es tut mir leid, das habe ich nicht verstanden.")
            except:
                say("Wenn du nichts sagst, kann ich auch nichts machen.")