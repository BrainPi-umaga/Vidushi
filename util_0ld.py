import speech_recognition as sr
from pydub import AudioSegment
import os
import librosa
import numpy as np

def load_audio_files(directory):
    labels = []
    features = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                path = os.path.join(subdir, file)
                audio, sr = librosa.load(path, sr=None)
                mfccs = librosa.feature.mfcc(y=audio, sr=sr)
                features.append(mfccs.mean(axis=1))
                labels.append(1)  # Assuming all samples are the wake word
    return np.array(features), np.array(labels)


#### if data convertion required
# convert_ogg_to_wav(data_directory)
def convert_ogg_to_wav(directory):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ogg'):
                ogg_path = os.path.join(subdir, file)
                wav_path = ogg_path[:-4] + '.wav'  # Change file extension to .wav
                try:
                    audio = AudioSegment.from_ogg(ogg_path)
                    audio.export(wav_path, format='wav')
                    print(f"Converted '{ogg_path}' to '{wav_path}'")
                except Exception as e:
                    print(f"Failed to convert {ogg_path}: {str(e)}")

def listen_for_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say 'Vidushi' to activate...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if text.lower() == "vidushi":
                print("Activated. Waiting for command...")
                command_audio = r.listen(source)
                command = r.recognize_google(command_audio)
                execute_command(command)
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

def execute_command(command):
    print(f"Executing command: {command}")


