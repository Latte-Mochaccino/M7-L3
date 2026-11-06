import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
from googletrans import LANGUAGES

duration = 7  # segundos de grabación
sample_rate = 44100

hierarchized_words = {"árbol":1, "flor":1, "hogar":1, "perro":1, "gato":1, "repositorio":2, "computadora":2, "ventana":2, "extensión":2, "programación":2, "inteligencia artificial":3, "reconocimiento de voz":3, "traducción automática":3, "maquinaria":3, "procesamiento de lenguaje natural":3}

points = 0

difficulty = int(input("Selecciona la dificultad de las palabras a traducir 🚥 (1 para fácil, 2 para medio, 3 para difícil): "))
if difficulty not in [1, 2, 3]:
    print("Dificultad no válida. Por favor, elige '1', '2' o '3'.")
    exit()

for i in range(5):
    print(f"\nRonda {i+1}:")
    word = np.random.choice([w for w, d in hierarchized_words.items() if d <= difficulty])
    print(f"Palabra a traducir: {word}")
    start = input("Presiona Enter para comenzar a grabar tu voz...")
    print("Habla ahora...")
    recording = sd.rec(
        int(duration * sample_rate), # el número de muestras a grabar
        samplerate=sample_rate,      # tasa de muestreo
        channels=1,                  # 1 significa grabación mono
        dtype="int16")               # tipo de datos para las muestras grabadas
    sd.wait()  # esperando a que termine la grabación

    wav.write("output1.wav", sample_rate, recording)
    print("Grabación completa, ahora reconociendo...")
    recognizer = sr.Recognizer()
    with sr.AudioFile("output1.wav") as source:
        audio = recognizer.record(source)

        try:
            audio = recognizer.recognize_google(audio, language="en")
            translator = Translator()
            translated = translator.translate(word, src="es", dest="en")
            print("Dijiste:", audio)
            if str(translated.text).lower() in audio.lower():
                points += hierarchized_words[word]
                print(f"¡Correcto! Has dicho la palabra correctamente (+{hierarchized_words[word]}) 🎉.")
            else:
                print(f"Incorrecto. Traducción correcta: {translated.text}. Llendo a la siguiente ronda.")

        except sr.UnknownValueError:             # - si Google no pudo entender el habla debido a ruido o silencio
            print("No se pudo reconocer el habla.")
        except sr.RequestError as e:             # - si no hay conexión a Internet o la API no está disponible
            print(f"Error del servicio: {e}")

print(f"\nJuego terminado. Has obtenido un total de {points} puntos 🌟.")