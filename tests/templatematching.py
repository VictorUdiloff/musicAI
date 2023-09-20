import librosa
import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt
import sys
import soundfile as sf

np.set_printoptions(threshold=sys.maxsize)

aaa, sr = librosa.load("testtemplatematching2.mp3")
song_np= np.array(aaa)

kick = song_np[650:8400]
clap = song_np[20650:25500]
hat = song_np[41300:44000]
snare = song_np[61700:64700]

#kick = kick /np.max(kick)
#clap = clap/np.max(clap)
#hat = hat/np.max(hat)
#snare = snare/np.max(snare)

#beat, ba = librosa.beat.beat_track(y=aaa,sr=sr)
bpm = 130

template_kick = np.convolve(np.flip(kick),song_np)
template_clap = np.convolve(np.flip(clap),song_np)
template_hat = np.convolve(np.flip(hat),song_np)
template_snare = np.convolve(np.flip(snare),song_np)

n_beats = int(np.round(bpm*(8/60)*(song_np.shape[0]/sr)))
n_channels = 4

r = np.zeros((n_beats,n_channels))

time_axis = np.linspace(0,song_np.shape[0],song_np.shape[0]) / sr 
beat_axis = (bpm*8/60) * np.linspace(0,song_np.shape[0],song_np.shape[0]) / sr


template_kick = np.roll(template_kick,-kick.shape[0])
for i in range(0,template_kick.shape[0]):
    if template_kick[i] > 50:
        template_kick[i] =1
    else:
        template_kick[i] = 0
template_kick -= np.roll(template_kick,-1)

for i in range(0,template_kick.shape[0]-1):
    if template_kick[i+1] < 0:
        template_kick[i+1] =0


for i in range(0,song_np.shape[0]):
    if template_kick[i] != 0:
        r[int(np.round((bpm)*(8/60)*(i/sr))),0] = 1



template_clap = template_clap > 10
template_clap = np.roll(template_clap,-clap.shape[0])

for i in range(0,song_np.shape[0]):
    if template_clap[i] != 0:
        r[int(np.round((bpm)*(8/60)*(i/sr))),1] = 1



template_hat = template_hat > 0.8
template_hat = np.roll(template_hat,-hat.shape[0])

for i in range(0,song_np.shape[0]):
    if template_hat[i] != 0:
        r[int(np.round((bpm)*(8/60)*(i/sr))),2] = 1



template_snare = template_snare > 40
template_snare = np.roll(template_snare,-snare.shape[0])

for i in range(0,song_np.shape[0]):
    if template_snare[i] != 0:
        r[int(np.round((bpm)*(8/60)*(i/sr))),3] = 1





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
    s[9+T*i,3] = 1
    s[25+T*i,3] = 1

new_beat = np.zeros(int(2*np.round((n_beats*(1/bpm)*(60/8)*sr))))

for i in range(0,n_channels):
    for j in range(0,n_beats):
        if s[j,0] == 1:
            new_beat[int(((1/bpm)*(60/8)*sr)*j):int(((1/bpm)*(60/8)*sr)*j)+kick.shape[0]] += kick*np.max(kick)
        if s[j,1] == 1:
            new_beat[int(((1/bpm)*(60/8)*sr)*j):int(((1/bpm)*(60/8)*sr)*j)+clap.shape[0]] += clap*np.max(clap)
        if s[j,2] == 1:
            new_beat[int(((1/bpm)*(60/8)*sr)*j):int(((1/bpm)*(60/8)*sr)*j)+hat.shape[0]] += hat*np.max(hat)
        if s[j,3] == 1:
            new_beat[int(((1/bpm)*(60/8)*sr)*j):int(((1/bpm)*(60/8)*sr)*j)+snare.shape[0]] += snare*np.max(snare)

new_song = np.copy(song_np)
for i in range(0,template_kick.shape[0]):
    if template_kick[i] == 1:
        new_song[i:i+kick.shape[0]] -= kick 



#print(song_np.shape)
#print(r[:,0].shape)
plt.plot(song_np)
plt.plot(new_song)
#plt.plot(template_clap)
#plt.plot(template_hat)
#plt.plot(template_snare)

plt.show()
sf.write("novamusica.mp3", new_song, sr)