# import library
import pyttsx3
import speech_recognition as sr

engineio = pyttsx3.init()
voices = engineio.getProperty("voices")
engineio.setProperty("rate", 130)  # Aquí puedes seleccionar la velocidad de la voz
engineio.setProperty("voice", voices[0].id)


# Initialize recognizer class (for recognizing the speech)

r = sr.Recognizer()

# Reading Microphone as source
# listening the speech and store in audio_text variable

with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source, timeout=3)
    print("Time over, thanks")
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling

    try:
        # using google speech recognition
        text = r.recognize_google(audio_text)
        engineio.say(text)
        engineio.runAndWait()
    except:
        print("Sorry, I did not get that")
