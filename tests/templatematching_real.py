import librosa
import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt
import sys

np.set_printoptions(threshold=sys.maxsize)

aaa, sr = librosa.load("audio/NewStuff.mp3")
song_np= np.array(aaa)

aaa2, sr2 = librosa.load("audio/NewStuffdrums.mp3")
song_np2= np.array(aaa2)


kick = song_np2[200:10000]
clap = song_np2[52650:67500]
hat = song_np2[90600:98000]

kick = kick /np.max(kick)
clap = clap/np.max(clap)
hat = hat/np.max(hat)

#beat, ba = librosa.beat.beat_track(y=aaa,sr=sr)
bpm = 124

template_kick = np.convolve(np.flip(kick),song_np)
template_clap = np.convolve(np.flip(clap),song_np)
template_hat = np.convolve(np.flip(hat),song_np)


n_beats = int(np.round(bpm*(8/60)*(song_np.shape[0]/sr)))
n_channels = 3

r = np.zeros((n_beats,n_channels))

time_axis = np.linspace(0,song_np.shape[0],song_np.shape[0]) / sr 
beat_axis = (bpm*8/60) * np.linspace(0,song_np.shape[0],song_np.shape[0]) / sr


template_kick = template_kick > 700
template_kick = np.roll(template_kick,-kick.shape[0])

for i in range(0,song_np.shape[0]):
    if template_kick[i] != 0:
        r[int(np.round((bpm)*(8/60)*(i/sr))),0] = 1



template_clap = template_clap > 30
template_clap = np.roll(template_clap,-clap.shape[0])

for i in range(0,song_np.shape[0]):
    if template_clap[i] != 0:
        r[int(np.round((bpm)*(8/60)*(i/sr))),1] = 1



template_hat = template_hat > 10
template_hat = np.roll(template_hat,-hat.shape[0])

for i in range(0,song_np.shape[0]):
    if template_hat[i] != 0:
        r[int(np.round((bpm)*(8/60)*(i/sr))),2] = 1



s = np.zeros((n_beats,n_channels))

for i in range(0,10):
    T = 32 #periodo
    s[1+T*i,0] = 1
    s[21+T*i,0] = 1
    s[9+T*i,1] = 1
    s[25+T*i,1] = 1
    s[3+T*i,2] = 1
    s[5+T*i,2] = 1
    s[11+T*i,2] = 1
    s[15+T*i,2] = 1
    s[21+T*i,2] = 1
    s[25+T*i,2] = 1
    s[39+T*i,2] = 1
    s[9+T*i,1] = 1
    s[25+T*i,1] = 1

new_beat = np.zeros(int(2*np.round((n_beats*(1/bpm)*(60/8)*sr))))

for i in range(0,n_channels):
    for j in range(0,n_beats):
        if s[j,0] == 1:
            new_beat[int(((1/bpm)*(60/8)*sr)*j):int(((1/bpm)*(60/8)*sr)*j)+kick.shape[0]] += kick*np.max(kick)
        if s[j,1] == 1:
            new_beat[int(((1/bpm)*(60/8)*sr)*j):int(((1/bpm)*(60/8)*sr)*j)+clap.shape[0]] += clap*np.max(clap)
        if s[j,2] == 1:
            new_beat[int(((1/bpm)*(60/8)*sr)*j):int(((1/bpm)*(60/8)*sr)*j)+hat.shape[0]] += hat*np.max(hat)



#print(song_np.shape)
#print(r[:,0].shape)
#plt.plot(song_np)
#plt.plot(template_kick)
#plt.plot(template_clap)
#plt.plot(template_hat)
#plt.plot(template_snare)

#plt.show()

sd.play(new_beat,sr)
time.sleep(5)
sd.stop()