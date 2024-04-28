import os
import struct
import wave
from datetime import datetime
import pvporcupine
from pvrecorder import PvRecorder
from Utils import say, takeCommand
import pyaudio

def Listner():
    keyword_paths = ['./VidushiModel/vidushi.ppn']
    audio_device_index = -1
    output_path = None

    porcupine = pvporcupine.create(
        access_key='yATVwpNGd9k/WUdaFTDPLJHXWkmQEx7TjrQLMd5U7cA4QOq4bmn8Pg==',
        # library_path=args.library_path,
        model_path='./porcupine_params_hi.pv',
        keyword_paths=['./VidushiModel/vidushi.ppn'],
        sensitivities=([0.5] * len(keyword_paths))
        )

    keywords = list()
    for x in keyword_paths:
        keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
        if len(keyword_phrase_part) > 6:
            keywords.append(' '.join(keyword_phrase_part[0:-6]))
        else:
            keywords.append(keyword_phrase_part[0])


    recorder = PvRecorder(
        frame_length=porcupine.frame_length,
        device_index= audio_device_index)
    recorder.start()


    print('Welcome to LPCPS, Lucknow')
    say(" Hello I am Vidushi, Nice to meet you!")
    print('Listening ... ')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)


            if wav_file is not None:
                wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

            if result >= 0:
                print('[%s] Detected %s' % (str(datetime.now()), keywords[result]))
                # say("Hi!, How may I help you!")
                # ret=takeCommand()

    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()
        if wav_file is not None:
            wav_file.close()

#
if __name__ == '__main__':
    Listner()

