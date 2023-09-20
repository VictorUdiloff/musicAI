import librosa
import numpy as np
import sounddevice as sd
import time
import demucs
import os

audio, ra = librosa.load("../audio/teste_audio.mp3")
os.system("python -m demucs.separate ../audio/teste_audio.mp3")


'''
def change_key(song,samplingr,notes):
    return librosa.effects.pitch_shift(song, sr=samplingr, n_steps=notes)


sd.play(change_key(audio,ra,-3),ra)
time.sleep(10)
sd.stop()
'''