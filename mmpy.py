
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
import numpy.fft as fft
import pyaudio
from IPython.display import clear_output
import random
import warnings
import pandas as pd
from random import choice
import ipywidgets as wg
from IPython.display import display
from ipywidgets import interact, interact_manual, fixed, interactive
from scipy.io.wavfile import write
from scipy.io.wavfile import read
warnings.filterwarnings("ignore")  #Ignorar warnings generados por librerías

class Audio(object):
    def __init__(self, x):
        freq=44100
        N=44100
        #Seteo inicial
        self.x= x
        #Tiempo de duración de la señal
        self.t= np.linspace(0, len(self.x)/freq, len(self.x))
        #Aplicar Transformada de Fourier
        transform = fft.fft(self.x,N)/N  
        magTransform = abs(transform)
        self.faxis = np.linspace(-freq/2,freq/2,freq)#Generar valores para coordenada x
        self.y=fft.fftshift(magTransform) #Generar valores para ordenada
        self.faxis2=self.faxis #Guardar valores para el reset
        self.y2=self.y
    
    def __len__(self):
        return len(self.x)
    def __str__(self):
        return str(self.x)
    def __getitem__(self,i):
        return self.x[i]
    
    def plot_time(self):
        freq=44100
        #Probar con valor "cambiado" si existe, sino, con el original
        try:
            t2=self.t2
            x2=self.x2
        except AttributeError:
            t2=self.t
            x2=self.x
        plt.plot(t2,x2)  #Generar plot
        plt.xlabel('Time (s)')
        plt.ylabel('Magnitude')
        plt.show()
        
    def plot_freq(self):
        freq=44100
        #Probar con valor "cambiado" si existe, sino, con el original
        try:
            faxis=self.faxis2
            n=self.y2
        except AttributeError:
            faxis=self.faxis2
            n=self.y2
        #Plot
        plt.plot(faxis, n)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.show()
        
    def save_time(self):
        freq=44100
        #Función para guardar el plot_time
        plt.plot(self.t,self.x) 
        plt.xlabel('Time (s)')
        plt.ylabel('Magnitude')
        plt.ioff()
        plt.savefig('plot_time.png')
        
    def save_freq(self):
        freq=44100
        #Función para guardar el plot_freq
        plt.plot(self.faxis, self.y)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.ioff()
        plt.savefig('plot_freq.png')
      
    def set_time(self, a, b):
        freq=44100
        if a<min(self.t):
            return print("Intente con un valor más grande")
        if b>max(self.t):
            return print("Intente con un valor más pequeño")
        if a>b:
            return print("Valor inicial mayor que final")
        else:
            #Setear valores
            self.t2 = self.t[int(a*freq):int(b*freq)]
            self.x2 = self.x[int(a*freq):int(b*freq)]

    def set_freq(self,a,b):
        freq=44100
        if a<min(self.faxis):
            return print("Intente con un valor más grande")
        if b>max(self.faxis):
            return print("Intente con un valor más pequeño")
        if a>b:
            return print("Valor inicial mayor que final")
        else:
            a=a-min(self.faxis)
            b=b-min(self.faxis)
            self.faxis2 = self.faxis[int(a):int(b)]
            self.y2 = self.y[int(a):int(b)] 

    def reset(self):
        self.t2 = self.t
        self.x2 = self.x
        self.faxis2 = self.faxis
        self.y2 = self.y
    def save(self, name):
        freq=44100
        return write(name, freq, self.x)
 
    def play(self, volume=0.3):
        freq=44100
        try:
            samples=self.x2
        except AttributeError:
            samples=self.x
        lista = []
        lista.append(samples)
        lista = np.concatenate(lista)*volume
        stream = pyaudio.PyAudio().open(format=pyaudio.paFloat32, channels=1, rate=freq, output=1)
        return stream.write(lista.astype(np.float32).tostring())      

