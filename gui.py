import customtkinter as ctk
import signall
import librosa
import sounddevice as sd
import time
import numpy as np
import keyboard
import soundfile as sf

#importar o audio

def separar():
    path = str(entry.get())
    signall.separate(path)
    nome_da_musica = str(entry.get())
    nome_da_musica = nome_da_musica[0:-4]
    global audio_drums 
    global audio_bass 
    global audio_instruments
    global audio_voice
    global sr

    audio_drums, sr = librosa.load("separated/htdemucs/"+nome_da_musica+"/drums.wav")
    audio_bass, sr = librosa.load("separated/htdemucs/"+nome_da_musica+"/bass.wav")
    audio_instruments, sr = librosa.load("separated/htdemucs/"+nome_da_musica+"/other.wav")
    audio_voice, sr = librosa.load("separated/htdemucs/"+nome_da_musica+"/vocals.wav")


    # transformar o vetor de audio em um vetor com comprimento par
    if audio_drums.shape[0] % 2 == 1:
        audio_drums = np.concatenate((audio_drums,np.array([0])),axis=0)

    if audio_bass.shape[0] % 2 == 1:
        audio_bass = np.concatenate((audio_bass,np.array([0])),axis=0)

    if audio_instruments.shape[0] % 2 == 1:
        audio_instruments = np.concatenate((audio_instruments,np.array([0])),axis=0)

    if audio_voice.shape[0] % 2 == 1:
        audio_voice = np.concatenate((audio_voice,np.array([0])),axis=0)



    #copia dos arquivos de audio para por os efeitos
    audio_effects_drums = np.copy(audio_drums)
    audio_effects_bass = np.copy(audio_bass)
    audio_effects_instruments = np.copy(audio_instruments)
    audio_effects_voice = np.copy(audio_voice)





#variaveis globais de estado daa faixas
filter_mode_drums = "0"
reverb_mode_drums = False
filter_mode_bass = "0"
reverb_mode_bass = False
filter_mode_instruments = "0"
reverb_mode_instruments = False
filter_mode_voice = "0"
reverb_mode_voice = False
notes = 0

#variaveis globais de estado do sintetizador

waveform1 = 0
waveform2 = 0
filter_mode_synth = 0
reverb_synth = 0


#funçoes
def play_drums():
    global audio_drums
    global audio_effects_drums
    audio_effects_drums = signall.change_volume(audio_drums,float(slider_volume_drums.get()))
    audio_effects_drums = signall.add_distortion(audio_effects_drums,"clip",float(slider_distortion_amount_drums.get()))
    audio_effects_drums = signall.add_echo(audio_effects_drums,float(slider_echo_decay_drums.get()),int(slider_echo_speed_drums.get()))
    audio_effects_drums = signall.add_reverb(audio_effects_drums,reverb_mode_drums)
    audio_effects_drums = signall.filter_song(audio_effects_drums,float(slider_filter_order_drums.get()),float(slider_filter_frequency_drums.get()),filter_mode_drums)
    sd.play(audio_effects_drums,sr)

def play_bass():
    global audio_bass
    global audio_effects_bass
    audio_effects_bass = signall.change_volume(audio_bass,float(slider_volume_bass.get()))
    audio_effects_bass = signall.add_distortion(audio_effects_bass,"clip",float(slider_distortion_amount_bass.get()))
    audio_effects_bass = signall.add_echo(audio_effects_bass,float(slider_echo_decay_bass.get()),int(slider_echo_speed_bass.get()))
    audio_effects_bass = signall.add_reverb(audio_effects_bass,reverb_mode_bass)
    audio_effects_bass = signall.filter_song(audio_effects_bass,float(slider_filter_order_bass.get()),float(slider_filter_frequency_bass.get()),filter_mode_bass)
    sd.play(audio_effects_bass,sr)

def play_instruments():
    global audio_instruments
    global audio_effects_instruments

    audio_effects_instruments = signall.change_volume(audio_instruments,float(slider_volume_instruments.get()))
    audio_effects_instruments = signall.add_distortion(audio_effects_instruments,"clip",float(slider_distortion_amount_instruments.get()))
    audio_effects_instruments = signall.add_echo(audio_effects_instruments,float(slider_echo_decay_instruments.get()),int(slider_echo_speed_instruments.get()))
    audio_effects_instruments = signall.add_reverb(audio_effects_instruments,reverb_mode_instruments)
    audio_effects_instruments = signall.filter_song(audio_effects_instruments,float(slider_filter_order_instruments.get()),float(slider_filter_frequency_instruments.get()),filter_mode_instruments)
    sd.play(audio_effects_instruments,sr)

def play_voice():
    global audio_voice
    global audio_effects_voice
    audio_effects_voice = signall.change_volume(audio_voice,float(slider_volume_voice.get()))
    audio_effects_voice = signall.add_distortion(audio_effects_voice,"clip",float(slider_distortion_amount_voice.get()))
    audio_effects_voice = signall.add_echo(audio_effects_voice,float(slider_echo_decay_voice.get()),int(slider_echo_speed_voice.get()))
    audio_effects_voice = signall.add_reverb(audio_effects_voice,reverb_mode_voice)
    audio_effects_voice = signall.filter_song(audio_effects_voice,float(slider_filter_order_voice.get()),float(slider_filter_frequency_voice.get()),filter_mode_voice)
    sd.play(audio_effects_voice,sr)


def play_all():
    global audio_effects_drums
    global audio_effects_bass
    global audio_effects_instruments
    global audio_effects_voice

    global sr
    global notes

    play_drums()
    sd.stop()
    play_bass()
    sd.stop()
    play_instruments()
    sd.stop()
    play_voice()
    sd.stop()

    audio_total = 0.25 * (audio_effects_bass+audio_effects_drums + audio_effects_instruments+ audio_effects_voice)
    audio_total = signall.change_key(audio_total,sr,notes)
    sd.play(audio_total,sr)

def parar():
    sd.stop()

def high_pass_drums():
    global filter_mode_drums
    filter_mode_drums="highpass"

def high_pass_bass():
    global filter_mode_bass
    filter_mode_bass="highpass"

def high_pass_instruments():
    global filter_mode_instruments
    filter_mode_instruments="highpass"

def high_pass_voice():
    global filter_mode_voice
    filter_mode_voice="highpass"


def low_pass_drums():
    global filter_mode_drums
    filter_mode_drums = "0"

def low_pass_bass():
    global filter_mode
    filter_mode = "0"

def low_pass_instruments():
    global filter_mode_instruments
    filter_mode_instruments = "0"

def low_pass_voice():
    global filter_mode_voice
    filter_mode_voice = "0"

def ligar_reverb_drums():
    global reverb_mode_drums
    reverb_mode_drums = True

def ligar_reverb_bass():
    global reverb_mode_bass
    reverb_mode_bass = True

def ligar_reverb_instruments():
    global reverb_mode_instruments
    reverb_mode_instruments = True

def ligar_reverb_voice():
    global reverb_mode_voice
    reverb_mode_voice = True



def desligar_reverb_drums():
    global reverb_mode_drums
    reverb_mode_drums = False

def desligar_reverb_bass():
    global reverb_mode_bass
    reverb_mode_bass = False

def desligar_reverb_instruments():
    global reverb_mode_instruments
    reverb_mode_instruments = False

def desligar_reverb_voice():
    global reverb_mode_voice
    reverb_mode_voice = False


def keymais():
    global notes
    notes +=1

def keymenos():
    global notes
    notes -=1

def download():
    global audio_effects_drums
    global audio_effects_bass
    global audio_effects_instruments
    global audio_effects_voice

    global sr
    global notes

    play_drums()
    sd.stop()
    play_bass()
    sd.stop()
    play_instruments()
    sd.stop()
    play_voice()
    sd.stop()

    audio_total = 0.25 * (audio_effects_bass+audio_effects_drums + audio_effects_instruments+ audio_effects_voice)
    audio_total = signall.change_key(audio_total,sr,notes)
    sf.write("audio_pronto.mp3", audio_total, sr)

# funções sintetizador
    
def ligar_reverb_synth():
    global reverb_synth
    reverb_synth = 1

def desligar_reverb_synth():
    global reverb_synth
    reverb_synth = 0

def high_pass_synth():
    global filter_mode_synth
    filter_mode_synth = "highpass"

def low_pass_synth():
    global filter_mode_synth
    filter_mode_synth="lowpass"

def osc_seno1():
    global waveform1
    waveform1=0

def osc_quad1():
    global waveform1
    waveform1=1

def osc_serra1():
    global waveform1
    waveform1=2

def osc_seno2():
    global waveform2
    waveform2=0

def osc_quad2():
    global waveform2
    waveform2=1

def osc_serra2():
    global waveform2
    waveform2=2




#GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Projeto de formatura")


botao_separar = ctk.CTkButton(root,text="separar",command=separar)
botao_separar.grid(row=0,column=0,padx=10,pady=10)

entry = ctk.CTkEntry(root, placeholder_text="coloque o nome do arquivo")
entry.grid(row=0,column=5,padx=10,pady=10)

botao_total = ctk.CTkButton(root,text="play",command=play_all)
botao_total.grid(row=0,column=1,padx=10,pady=10)

botao_keymais = ctk.CTkButton(root,text="aumentar tom",command=keymais)
botao_keymais.grid(row=0,column=2,padx=10,pady=10)

botao_keymenos = ctk.CTkButton(root,text="diminuir tom",command=keymenos)
botao_keymenos.grid(row=0,column=3,padx=10,pady=10)

botao_download = ctk.CTkButton(root,text="download",command=download)
botao_download.grid(row=0,column=4,padx=10,pady=10)

frame_drums = ctk.CTkFrame(root)
frame_bass = ctk.CTkFrame(root)
frame_instruments = ctk.CTkFrame(root)
frame_voice = ctk.CTkFrame(root)
frame_synth = ctk.CTkFrame(root)
frame_synth2 = ctk.CTkFrame(root)



#Drums ---------------------------------------------------------------------------------

tilulo = ctk.CTkLabel(frame_drums,text="Bateria")
tilulo.pack()

botao_play = ctk.CTkButton(frame_drums,text="play",command=play_drums)
botao_play.pack()

botao_stop = ctk.CTkButton(frame_drums,text="stop",command=parar)
botao_stop.pack()


label_volume = ctk.CTkLabel(frame_drums,text="volume")
label_volume.pack()

slider_volume_drums = ctk.CTkSlider(frame_drums,from_=1,to=100, orientation=ctk.HORIZONTAL)
slider_volume_drums.pack()
slider_volume_drums.set(100)


label_distortion = ctk.CTkLabel(frame_drums,text="distorção")
label_distortion.pack()

slider_distortion_amount_drums = ctk.CTkSlider(frame_drums,from_=0,to=100, orientation=ctk.HORIZONTAL)
slider_distortion_amount_drums.pack()
slider_distortion_amount_drums.set(0)

label_echo_decay = ctk.CTkLabel(frame_drums,text="eco decay")
label_echo_decay.pack()

slider_echo_decay_drums = ctk.CTkSlider(frame_drums,from_=0.0,to=1.0, orientation=ctk.HORIZONTAL, number_of_steps=100)
slider_echo_decay_drums.pack()
slider_echo_decay_drums.set(0)

label_echo_speed = ctk.CTkLabel(frame_drums,text="velocidade do eco")
label_echo_speed.pack()

slider_echo_speed_drums = ctk.CTkSlider(frame_drums,from_=50,to=1000, orientation=ctk.HORIZONTAL)
slider_echo_speed_drums.pack()

botao_ligar_reverb_drums = ctk.CTkButton(frame_drums,text="ligar reverb",command=ligar_reverb_drums)
botao_ligar_reverb_drums.pack()

botao_desligar_reverb_drums = ctk.CTkButton(frame_drums,text="desligar reverb",command=desligar_reverb_drums)
botao_desligar_reverb_drums.pack()

label_filter_frequency = ctk.CTkLabel(frame_drums,text="frequência do filtro")
label_filter_frequency.pack()

slider_filter_frequency_drums = ctk.CTkSlider(frame_drums,from_=20,to=20000, orientation=ctk.HORIZONTAL)
slider_filter_frequency_drums.pack()
slider_filter_frequency_drums.set(20000)

label_filter_order = ctk.CTkLabel(frame_drums,text="ordem do filtro")
label_filter_order.pack()

slider_filter_order_drums = ctk.CTkSlider(frame_drums,from_=1,to=10, orientation=ctk.HORIZONTAL)
slider_filter_order_drums.pack()
slider_filter_order_drums.set(1)

botao_low_pass_drums = ctk.CTkButton(frame_drums,text="passa-baixa",command=low_pass_drums)
botao_low_pass_drums.pack()

botao_high_pass_drums = ctk.CTkButton(frame_drums,text="passa-alta",command=high_pass_drums)
botao_high_pass_drums.pack()

frame_drums.grid(row=1,column=0,padx=10,pady = 10)

#Bass  ---------------------------------------------------------------------------------

tilulo = ctk.CTkLabel(frame_bass,text="Baixo")
tilulo.pack()

botao_play = ctk.CTkButton(frame_bass,text="play",command=play_bass)
botao_play.pack()

botao_stop = ctk.CTkButton(frame_bass,text="stop",command=parar)
botao_stop.pack()


label_volume = ctk.CTkLabel(frame_bass,text="volume")
label_volume.pack()

slider_volume_bass = ctk.CTkSlider(frame_bass,from_=1,to=100, orientation=ctk.HORIZONTAL)
slider_volume_bass.pack()
slider_volume_bass.set(100)


label_distortion = ctk.CTkLabel(frame_bass,text="distorção")
label_distortion.pack()

slider_distortion_amount_bass = ctk.CTkSlider(frame_bass,from_=0,to=100, orientation=ctk.HORIZONTAL)
slider_distortion_amount_bass.pack()
slider_distortion_amount_bass.set(0)

label_echo_decay = ctk.CTkLabel(frame_bass,text="eco decay")
label_echo_decay.pack()

slider_echo_decay_bass = ctk.CTkSlider(frame_bass,from_=0.0,to=1.0, orientation=ctk.HORIZONTAL, number_of_steps=100)
slider_echo_decay_bass.pack()
slider_echo_decay_bass.set(0)

label_echo_speed = ctk.CTkLabel(frame_bass,text="velocidade do eco")
label_echo_speed.pack()

slider_echo_speed_bass = ctk.CTkSlider(frame_bass,from_=50,to=1000, orientation=ctk.HORIZONTAL)
slider_echo_speed_bass.pack()

botao_ligar_reverb_bass = ctk.CTkButton(frame_bass,text="ligar reverb",command=ligar_reverb_bass)
botao_ligar_reverb_bass.pack()

botao_desligar_reverb_bass = ctk.CTkButton(frame_bass,text="desligar reverb",command=desligar_reverb_bass)
botao_desligar_reverb_bass.pack()

label_filter_frequency = ctk.CTkLabel(frame_bass,text="frequência do filtro")
label_filter_frequency.pack()

slider_filter_frequency_bass = ctk.CTkSlider(frame_bass,from_=20,to=20000, orientation=ctk.HORIZONTAL)
slider_filter_frequency_bass.pack()
slider_filter_frequency_bass.set(20000)

label_filter_order = ctk.CTkLabel(frame_bass,text="ordem do filtro")
label_filter_order.pack()

slider_filter_order_bass = ctk.CTkSlider(frame_bass,from_=1,to=10, orientation=ctk.HORIZONTAL)
slider_filter_order_bass.pack()
slider_filter_order_bass.set(1)

botao_low_pass_bass = ctk.CTkButton(frame_bass,text="passa-baixa",command=low_pass_bass)
botao_low_pass_bass.pack()

botao_high_pass_bass = ctk.CTkButton(frame_bass,text="passa-alta",command=high_pass_bass)
botao_high_pass_bass.pack()

frame_bass.grid(row=1,column=1,padx=10,pady = 10)


#Instruments ---------------------------------------------------------------------------------

tilulo = ctk.CTkLabel(frame_instruments,text="Instrumentos")
tilulo.pack()

botao_play_instruments = ctk.CTkButton(frame_instruments,text="play",command=play_instruments)
botao_play_instruments.pack()

botao_stop = ctk.CTkButton(frame_instruments,text="stop",command=parar)
botao_stop.pack()


label_volume = ctk.CTkLabel(frame_instruments,text="volume")
label_volume.pack()

slider_volume_instruments = ctk.CTkSlider(frame_instruments,from_=1,to=100, orientation=ctk.HORIZONTAL)
slider_volume_instruments.pack()
slider_volume_instruments.set(100)


label_distortion = ctk.CTkLabel(frame_instruments,text="distorção")
label_distortion.pack()

slider_distortion_amount_instruments = ctk.CTkSlider(frame_instruments,from_=0,to=100, orientation=ctk.HORIZONTAL)
slider_distortion_amount_instruments.pack()
slider_distortion_amount_instruments.set(0)

label_echo_decay = ctk.CTkLabel(frame_instruments,text="eco decay")
label_echo_decay.pack()

slider_echo_decay_instruments = ctk.CTkSlider(frame_instruments,from_=0.0,to=1.0, orientation=ctk.HORIZONTAL, number_of_steps=100)
slider_echo_decay_instruments.pack()
slider_echo_decay_instruments.set(0)

label_echo_speed = ctk.CTkLabel(frame_instruments,text="velocidade do eco")
label_echo_speed.pack()

slider_echo_speed_instruments = ctk.CTkSlider(frame_instruments,from_=50,to=1000, orientation=ctk.HORIZONTAL)
slider_echo_speed_instruments.pack()

botao_ligar_reverb_instruments = ctk.CTkButton(frame_instruments,text="ligar reverb",command=ligar_reverb_instruments)
botao_ligar_reverb_instruments.pack()

botao_desligar_reverb_instruments = ctk.CTkButton(frame_instruments,text="desligar reverb",command=desligar_reverb_instruments)
botao_desligar_reverb_instruments.pack()

label_filter_frequency = ctk.CTkLabel(frame_instruments,text="frequência do filtro")
label_filter_frequency.pack()

slider_filter_frequency_instruments = ctk.CTkSlider(frame_instruments,from_=20,to=20000, orientation=ctk.HORIZONTAL)
slider_filter_frequency_instruments.pack()
slider_filter_frequency_instruments.set(20000)

label_filter_order = ctk.CTkLabel(frame_instruments,text="ordem do filtro")
label_filter_order.pack()

slider_filter_order_instruments = ctk.CTkSlider(frame_instruments,from_=1,to=10, orientation=ctk.HORIZONTAL)
slider_filter_order_instruments.pack()
slider_filter_order_instruments.set(1)

botao_low_pass_instruments = ctk.CTkButton(frame_instruments,text="passa-baixa",command=low_pass_instruments)
botao_low_pass_instruments.pack()

botao_high_pass = ctk.CTkButton(frame_instruments,text="passa-alta",command=high_pass_instruments)
botao_high_pass.pack()

frame_instruments.grid(row=1,column=2,padx=10,pady = 10)

#Voice ---------------------------------------------------------------------------------

tilulo = ctk.CTkLabel(frame_voice,text="Voz")
tilulo.pack()

botao_play = ctk.CTkButton(frame_voice,text="play",command=play_voice)
botao_play.pack()

botao_stop = ctk.CTkButton(frame_voice,text="stop",command=parar)
botao_stop.pack()


label_volume = ctk.CTkLabel(frame_voice,text="volume")
label_volume.pack()

slider_volume_voice = ctk.CTkSlider(frame_voice,from_=1,to=100, orientation=ctk.HORIZONTAL)
slider_volume_voice.pack()
slider_volume_voice.set(100)


label_distortion = ctk.CTkLabel(frame_voice,text="distorção")
label_distortion.pack()

slider_distortion_amount_voice = ctk.CTkSlider(frame_voice,from_=0,to=100, orientation=ctk.HORIZONTAL)
slider_distortion_amount_voice.pack()
slider_distortion_amount_voice.set(0)

label_echo_decay = ctk.CTkLabel(frame_voice,text="eco decay")
label_echo_decay.pack()

slider_echo_decay_voice = ctk.CTkSlider(frame_voice,from_=0.0,to=1.0, orientation=ctk.HORIZONTAL, number_of_steps=100)
slider_echo_decay_voice.pack()
slider_echo_decay_voice.set(0)

label_echo_speed = ctk.CTkLabel(frame_voice,text="velocidade do eco")
label_echo_speed.pack()

slider_echo_speed_voice = ctk.CTkSlider(frame_voice,from_=50,to=1000, orientation=ctk.HORIZONTAL)
slider_echo_speed_voice.pack()

botao_ligar_reverb_voice = ctk.CTkButton(frame_voice,text="ligar reverb",command=ligar_reverb_voice)
botao_ligar_reverb_voice.pack()

botao_desligar_reverb_voice = ctk.CTkButton(frame_voice,text="desligar reverb",command=desligar_reverb_voice)
botao_desligar_reverb_voice.pack()

label_filter_frequency = ctk.CTkLabel(frame_voice,text="frequência do filtro")
label_filter_frequency.pack()

slider_filter_frequency_voice = ctk.CTkSlider(frame_voice,from_=20,to=20000, orientation=ctk.HORIZONTAL)
slider_filter_frequency_voice.pack()
slider_filter_frequency_voice.set(20000)

label_filter_order = ctk.CTkLabel(frame_voice,text="ordem do filtro")
label_filter_order.pack()

slider_filter_order_voice = ctk.CTkSlider(frame_voice,from_=1,to=10, orientation=ctk.HORIZONTAL)
slider_filter_order_voice.pack()
slider_filter_order_voice.set(1)

botao_low_pass_voice = ctk.CTkButton(frame_voice,text="passa-baixa",command=low_pass_voice)
botao_low_pass_voice.pack()

botao_high_pass_voice = ctk.CTkButton(frame_voice,text="passa-alta",command=high_pass_voice)
botao_high_pass_voice.pack()

frame_voice.grid(row=1,column=3,padx=10,pady = 10)

#Synth ---------------------------------------------------------------------------------

tilulo = ctk.CTkLabel(frame_synth,text="Sintetizador")
tilulo.pack()

label_mix = ctk.CTkLabel(frame_synth,text="mix")
label_mix.pack()

slider_mix = ctk.CTkSlider(frame_synth,from_=0,to=100, orientation=ctk.HORIZONTAL)
slider_mix.pack()
slider_mix.set(50)

label_forma_de_onda_1 = ctk.CTkLabel(frame_synth,text="forma de onda oscilador 1")
label_forma_de_onda_1.pack()

seno_oscilador_1 = ctk.CTkButton(frame_synth,text="seno",command=osc_seno1)
seno_oscilador_1.pack()

quadrado_oscilador_1 = ctk.CTkButton(frame_synth,text="onda quadrada",command=osc_quad1)
quadrado_oscilador_1.pack()

serra_oscilador_1 = ctk.CTkButton(frame_synth,text="dente de serra",command=osc_serra1)
serra_oscilador_1.pack()

label_forma_de_onda_2 = ctk.CTkLabel(frame_synth,text="forma de onda oscilador 2")
label_forma_de_onda_2.pack()

seno_oscilador_2 = ctk.CTkButton(frame_synth,text="seno",command=osc_seno2)
seno_oscilador_2.pack()

quadrado_oscilador_2 = ctk.CTkButton(frame_synth,text="onda quadrada",command=osc_quad2)
quadrado_oscilador_2.pack()

serra_oscilador_2 = ctk.CTkButton(frame_synth,text="dente de serra",command=osc_serra2)
serra_oscilador_2.pack()

label_distortion = ctk.CTkLabel(frame_synth,text="distorção")
label_distortion.pack()

slider_distortion_amount_synth = ctk.CTkSlider(frame_synth,from_=0,to=100, orientation=ctk.HORIZONTAL)
slider_distortion_amount_synth.pack()
slider_distortion_amount_synth.set(0)

label_echo_decay = ctk.CTkLabel(frame_synth,text="eco decay")
label_echo_decay.pack()

slider_echo_decay_synth = ctk.CTkSlider(frame_synth,from_=0.0,to=1.0, orientation=ctk.HORIZONTAL, number_of_steps=100)
slider_echo_decay_synth.pack()
slider_echo_decay_synth.set(0)

label_echo_speed = ctk.CTkLabel(frame_synth,text="velocidade do eco")
label_echo_speed.pack()

slider_echo_speed_synth = ctk.CTkSlider(frame_synth,from_=50,to=1000, orientation=ctk.HORIZONTAL)
slider_echo_speed_synth.pack()

botao_ligar_reverb_synth = ctk.CTkButton(frame_synth2,text="ligar reverb",command=ligar_reverb_synth)
botao_ligar_reverb_synth.pack()

botao_desligar_reverb_synth = ctk.CTkButton(frame_synth2,text="desligar reverb",command=desligar_reverb_synth)
botao_desligar_reverb_synth.pack()

label_filter_frequency = ctk.CTkLabel(frame_synth2,text="frequência do filtro")
label_filter_frequency.pack()

slider_filter_frequency_synth = ctk.CTkSlider(frame_synth2,from_=20,to=20000, orientation=ctk.HORIZONTAL)
slider_filter_frequency_synth.pack()
slider_filter_frequency_synth.set(20000)

label_filter_order = ctk.CTkLabel(frame_synth2,text="ordem do filtro")
label_filter_order.pack()

slider_filter_order_synth = ctk.CTkSlider(frame_synth2,from_=1,to=10, orientation=ctk.HORIZONTAL)
slider_filter_order_synth.pack()
slider_filter_order_synth.set(1)

botao_low_pass_synth = ctk.CTkButton(frame_synth2,text="passa-baixa",command=low_pass_synth)
botao_low_pass_synth.pack()

botao_high_pass_synth = ctk.CTkButton(frame_synth2,text="passa-alta",command=high_pass_synth)
botao_high_pass_synth.pack()

label_attack = ctk.CTkLabel(frame_synth2,text="attack")
label_attack.pack()

slider_attack = ctk.CTkSlider(frame_synth2,from_=1,to=500, orientation=ctk.HORIZONTAL)
slider_attack.pack()
slider_attack.set(1)

label_decay = ctk.CTkLabel(frame_synth2,text="decay")
label_decay.pack()

slider_decay = ctk.CTkSlider(frame_synth2,from_=1,to=500, orientation=ctk.HORIZONTAL)
slider_decay.pack()
slider_decay.set(1)

label_sustain = ctk.CTkLabel(frame_synth2,text="sustain")
label_sustain.pack()

slider_sustain = ctk.CTkSlider(frame_synth2,from_=1,to=10, orientation=ctk.HORIZONTAL)
slider_sustain.pack()
slider_sustain.set(1)

label_release = ctk.CTkLabel(frame_synth2,text="release")
label_release.pack()

slider_release = ctk.CTkSlider(frame_synth2,from_=1,to=1000, orientation=ctk.HORIZONTAL)
slider_release.pack()
slider_release.set(1)

label_comeco_granular = ctk.CTkLabel(frame_synth2,text="começo granular")
label_comeco_granular.pack()

slider_comeco_granular = ctk.CTkSlider(frame_synth2,from_=1,to=44100, orientation=ctk.HORIZONTAL)
slider_comeco_granular.pack()
slider_comeco_granular.set(1000)

label_janela_granular = ctk.CTkLabel(frame_synth2,text="tamanho da janela granular")
label_janela_granular.pack()

slider_janela_granular = ctk.CTkSlider(frame_synth2,from_=1,to=44100, orientation=ctk.HORIZONTAL)
slider_janela_granular.pack()
slider_janela_granular.set(100)


frame_synth.grid(row=1,column=4,padx=10,pady = 10)
frame_synth2.grid(row=1,column=5,padx=10,pady = 10)


#-----------------------------------------------------------------------------------------

#z = [forma de onda 1,forma de onda 2,tipo do filtro,reverb,mix,f1,f2,f corte,ordem,a,d,s,r,instensidade da distorçao,decay,velocidade do eco]
z = [0,1,0,0,50,440,700,3000,2,1,200,100,100,100,0.5,5]

def gerar_som():
    global waveform1
    global waveform2
    global filter_mode_synth
    global reverb_synth
    z[0] = waveform1
    z[1] = waveform2
    z[2] = filter_mode_synth
    z[3] = reverb_synth
    z[4] = float(slider_mix.get())
    z[7] = float(slider_filter_frequency_synth.get())
    z[8] = float(slider_filter_order_synth.get())
    z[9] = float(slider_attack.get())
    z[10] = float(slider_decay.get())
    z[11] = float(slider_sustain.get())
    z[12] = float(slider_release.get())
    z[13] = float(slider_distortion_amount_synth.get())
    z[14] = float(slider_echo_decay_synth.get())
    z[15] = int(slider_echo_speed_synth.get())

    sd.play(signall.generate(z),sr)

def on_key_event(e):
    print(f"Key {e.name} {'pressed' if e.event_type == keyboard.KEY_DOWN else 'released'}")
    if e.name == "a":
        z[5] = 261
        z[6] = 1.5*z[5]
    if e.name == "s":
        z[5] = 293
        z[6] = 1.5*z[5]
    if e.name == "d":
        z[5] = 329
        z[6] = 1.5*z[5]
    if e.name == "f":
        z[5] = 349
        z[6] = 1.5*z[5]
    if e.name == "g":
        z[5] = 392
        z[6] = 1.5*z[5]
    if e.name == "h":
        z[5] = 440
        z[6] = 1.5*z[5]
    if e.name == "j":
        z[5] = 493
        z[6] = 1.5*z[5]
    if e.name != "z":
        gerar_som()
    if e.name == "z":
        sd.play(signall.repeat(audio_instruments,round(slider_janela_granular.get()),round(slider_comeco_granular.get())))

keyboard.on_press(on_key_event)
keyboard.on_release(on_key_event)




root.mainloop()