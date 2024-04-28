
import config
import speech_recognition as sr
import os
import webbrowser
import google.generativeai as genai
import datetime
from test import main
genai.configure(api_key=config.apikey)


os.environ["TOKENIZERS_PARALLELISM"] = "false"

def chat(query):
    # MODEL_NAME = 'paraphrase-MiniLM-L6-v2'
    GEMINI_MODEL_NAME = "gemini-pro"
    model   = genai.GenerativeModel(model_name=GEMINI_MODEL_NAME)
    chat = model.start_chat(history=[])

    try:
        r = chat.send_message(["Keep answer in short"] + query)
        # print(r)
        say(r.candidates[0].content.parts[0].text)
    except TypeError as e:
        print("Type error:", e)
    except Exception as e:
        print("An error occurred:", e)



def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold =  1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")

            if "the time" in query:
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                say(f"Sir time is {hour} bajke {min} minutes")

            elif query == 'what is lpc PS':
                say("LPCPS is one of the most coveted colleges for admission for Degree Programs in the Northern India.")


            elif "go to sleep".lower() in query.lower():
                say("Bye Bye!, I gonna sleep for million years!, You made me cry, I will cry like a baby. No prince can, wake me up!")
                exit()

            else:
                print("Chatting...")
                # print(type(query), query)  # Check what you're actually passing to the send_message
                res = chat([query])
                # print(query)
                # print(res)
                # say(res)

        except Exception as e:
            print("I am not able to understand, Please try again!")




#
#
# if __name__ == '__main__':
#     # train_model(model, data_loader)
#     print('Welcome to LPCPS, Lucknow')
#     say(" Hello I am Vidushi, Nice to meet you!")
#
#     while True:
#         print("Listening...")
#         query = takeCommand()
#         print(f"User said: {query}")
#         try:
#             if query == 'Vidushi':
#                 say("Hi!, How may I help you!")
#             elif "vidushi" or "videshi" in query.lower():
#                    # todo: Add more sites
#                 sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
#                 for site in sites:
#                     if f"Open {site[0]}".lower() in query.lower():
#                         say(f"Opening {site[0]} sir...")
#                         webbrowser.open(site[1])
#                 # todo: Add a feature to play a specific song
#
#                 if "the time" in query:
#                     hour = datetime.datetime.now().strftime("%H")
#                     min = datetime.datetime.now().strftime("%M")
#                     say(f"Sir time is {hour} bajke {min} minutes")
#
#                 elif query == 'what is lpc PS':
#                    say("LPCPS is one of the most coveted colleges for admission for Degree Programs in the Northern India.")
#
#
#                 elif "Lpc ps".lower() in query.lower():
#                     res=main([str(query)])
#                     print(res)
#                     say(res)
#
#                 elif "go to sleep".lower() in query.lower():
#                     say("Bye Bye!, I gonna sleep for million years!, You made me cry, I will cry like a baby. No prince can, wake me up!")
#                     exit()
#
#                 elif "reset chat".lower() in query.lower():
#                     chatStr = ""
#
#                 else:
#                     print("Chatting...")
#                     print(type(query), query)  # Check what you're actually passing to the send_message
#                     res=chat([query])
#                     print(query)
#                     print(res)
#                     say(res)
#
#         except Exception as e:
#             print("I am not able to understand, Please try again!")
