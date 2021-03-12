# import library
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pyttsx3
import speech_recognition as sr

engineio = pyttsx3.init()
voices = engineio.getProperty("voices")
engineio.setProperty("rate", 130)  # Aquí puedes seleccionar la velocidad de la voz
engineio.setProperty("voice", voices[0].id)
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

r = sr.Recognizer()

with sr.Microphone() as source:
    for step in range(5):
        print("Sprich...")
        audio = r.listen(source, timeout=3)
        print("Danke!")
        audio_text = r.recognize_google(audio)

        new_user_input_ids = tokenizer.encode(
            audio_text + tokenizer.eos_token, return_tensors="pt"
        )
        bot_input_ids = (
            torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
            if step > 0
            else new_user_input_ids
        )
        chat_history_ids = model.generate(
            bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
        )
        print(chat_history_ids.shape)
        print(type(chat_history_ids))
        new_text = tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1] :][0], skip_special_tokens=True
        )

        print(new_text)
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling

        try:
            # using google speech recognition
            engineio.say(new_text)
            engineio.runAndWait()
        except:
            engineio.say("Sorry, did not understand you")

