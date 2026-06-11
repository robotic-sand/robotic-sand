import sounddevice as sd 
import scipy.io.wavfile as wav
import speech_recognition as sr 
import numpy as np
from googletrans import Translator
import random

#configuraciones
duration = 4 
sample_rate = 44100

words_by_level = {
    "facil": ["gato", "perro", "manzana", "leche", "sol"],
    "medio": ["banano", "escuela", "amigo", "ventana", "amarillo"],
    "dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}

while True:
    print("===========================")
    print("Bienvenido al juego de pronunciación")
    dificultad = input("Selecciona el nivel de dificultad (facil, medio, dificil): ").lower()
    if dificultad in words_by_level:
        lista_palabras = words_by_level[dificultad]
        palabra_seleccionada = random.choice(lista_palabras)
        print(f"como se dice '{palabra_seleccionada}' en inglés")
        break
    else:
        print("Nivel de dificultad no válido. Intenta de nuevo.")

#grabacion de audio
print("Habla ahora...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate,channels=1, dtype='int16')
sd.wait()

#guardar el audio grabado
wav.write("grabacion.wav", sample_rate, recording)
print("Audio guardado como grabacion.wav")

#reconocimiento de voz
print("Reconociendo...")
recognizer = sr.Recognizer()
translator = Translator()
with sr.AudioFile("grabacion.wav") as source:
    audio= recognizer.record(source)

try:
    text= recognizer.recognize_google(audio, language="en-US")
    palabra_traducida = translator.translate(palabra_seleccionada, src='es', dest='en').text
    if palabra_traducida.lower() == text.lower():
        print("Correcto Has pronunciado bien la palabra.")
    else:
        print(f"Incorrecto La pronunciación correcta es: {palabra_traducida}")

    print("y tu has dicho: " + text)
except sr.UnknownValueError:
    print("No se pudo entender el audio vocaliza mejor")

except sr.RequestError as e:
    print(f"Error al solicitar resultados del servicio de reconocimiento de voz; {e}")