import librosa
import numpy as np
import time
import demucs
import os
import math


# separa as faixas
def separate(path):
    print("python -m demucs.separate "+path)
    os.system("python -m demucs.separate "+path)

# volume gvai de 0 a 100
# a formula que muda o volume é I = 10^(v/50) -1
def change_volume(song,v):
    song = song / np.max(song)
    return song*((np.power(10,v/50)-1)/100)

def change_key(song,samplingrate,notes):
    return librosa.effects.pitch_shift(song, sr=samplingrate, n_steps=notes)





def filter_song(song,order,cutoff,type):

    H1 = np.linspace(0,20000,round(song.shape[0]/2))
    H1 = 1/np.sqrt(1+ np.power(H1/cutoff,2*order))
    H2 = np.flip(H1)
    H = np.concatenate((H1, H2), axis=0)
    if type=="highpass" or type == 1:
        H = 1 - H
    fft_song = np.fft.fft(song)
    return np.real(np.fft.ifft(fft_song*H))


# adiciona distorção linear, do tipo sigmoid ou hardclip
# Intensidade de 0 a 100
def add_distortion(song,type,amount):
    if type=="clip":
        if amount == 100:
            amount = 99.9
        max = np.max(song)
        song = song / np.max(song)
        maskp = song > ((100-amount)/100)
        song[maskp] = ((100-amount)/100)
        maskn = song < -1 * ((100-amount)/100)
        song[maskn] = -1 * ((100-amount)/100)

        return max * (song / np.max(song))
    if type=="gamma":
        max = np.max(song)
        song = song / np.max(song)
        song = 2 / (1 + np.power(2.718281,-1*((np.power(10,amount/50)-1)+0.4)* song)) - 1
        return max * (song / np.max(song))

# decay é exponencial de 0 a 1, ex: x[n+1] = decay * x[n]
# speed é a o tempo entre cada eco
def add_echo(song,decay,speed):
    max = np.max(song)
    song = song / np.max(song)
    song_original = np.copy(song)
    for i in range(1,10):
        if i*speed*44 < song.shape[0]:
            song += np.power(decay,i)*np.concatenate((np.zeros(i*speed*44), song_original[:-i*speed*44]))
    return max * (song / np.max(song))


def add_reverb(song,mode):
    N = 10 # numbero de canais
    F = 10 # numero de ciclos de feedback
    if mode == False or mode == 0:
        return song
    max = np.max(song)
    song = song / np.max(song)

    song_channels = np.zeros((song.shape[0],N))
    for i in range(0,N):
        song_channels[:,i] = song
    for i in range(0,N):
        song_channels[:,i] = np.roll(song_channels[:,i],44*int(np.round(np.random.rand(1)*150)))
        if i % 2 == 1:
            song_channels[:,i] = -1 * song_channels[:,i]
        #matriz hadamard
    for i in range(0,F):
        for j in range(0,N-1):
            song_channels[:,j] = song_channels[:,j] + pow(0.5,i) * np.roll(song_channels[:,j],44*int(np.round(np.random.rand(1)*150)),axis=0) + pow(0.4,i) * song_channels[:,j+1]
    song = np.mean(song_channels,axis=1)
    return max * (song / np.max(song))


def osc(waveform,f,t):
    song = np.linspace(0,t,44100*t)
    song = np.sin(2*np.pi*f*song)
    if waveform=="square" or waveform==1:
        maskp = song >= 0
        song[maskp] = 1
        maskn = song < 0
        song[maskn] = -1
    if waveform == "sawtooth" or waveform==2:
        T = round(44100/f)
        for i in range(1,song.shape[0]):
            song[i] = 2*(i%T)*f/44100-1
    for i in range(0,song.shape[0]):
        if song[i] == 0:
            song[i] = 0.0001
    return song

def adrs(song,a,d,s,r):
    if a < song.shape[0] and d < song.shape[0] and s < song.shape[0]:
        a = int(a * 44)
        d = int(d * 44)
        s = int(s * 44)
        r = 10**(-r/10)
    envelope = np.ones(song.shape[0])
    domain = np.linspace(0,song.shape[0]/44100,song.shape[0])
    envelope[0:a] = 1 - np.exp((-5*44100/a)*domain[0:a])
    envelope[a:d+a] = (1-r)*np.exp((-5*44100/d)*domain[0:d]) + r
    envelope[d+a:s+d+a] = r * np.exp((-5*44100/s)*domain[0:s])
    envelope[s+d+a:-1] = 0  
    envelope[-1] = 0  
    song = song * envelope
    return song

def generate(z):
    timee=2
    audio1 = osc(z[0],z[5],timee)
    audio2 = osc(z[1],z[6],timee)
    audio = ((z[4]*audio2/100)+((100-z[4])*audio1/100))/2
    if np.max(audio) == 0:
        return audio
    audio = filter_song(audio,z[8],z[7],z[2])
    audio = adrs(audio,z[9],z[10],z[12],z[11])
    if np.max(audio) == 0:
        return audio
    audio = add_distortion(audio,"gamma",z[13])
    audio = add_echo(audio,z[14],z[15])
    audio = add_reverb(audio,z[3])
    return audio

def repeat(song,l,o):
    #5s
    granular = np.zeros(44100* 10) + 0.0001
    grain = song[o:o+l]
    k = math.floor(granular.shape[0]/l)
    for i in range(0,k):
        if ((1+i)*l) < granular.shape[0]:
            granular[(i*l):((1+i)*l)] = grain
    return granular
