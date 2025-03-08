
from gtts import gTTS
from playsound import playsound

import speech_recognition as sr

"""
# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("diga algo")
    audio = r.listen(source)
"""

voz=("esto ")
s = gTTS(voz, lang='es')
s.save('sample.mp3')
playsound('sample.mp3')



equivalencias = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "CH": "----",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "Ñ": "--.--",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    ":": "---...",
    "?": "..--..",
    "'": ".----.",
    "-": "-....-",
    "/": "-..-.",
    "\"": ".-..-.",
    "@": ".--.-.",
    "=": "-...-",
    "!": "−.−.−−",
    "": " ",
}


def morse_a_caracter_plano(morse):
    for caracter in equivalencias:
        if equivalencias[caracter] == morse:
            return caracter
    # Si no encontramos equivalencia, regresamos una cadena vacía
    return ""


def decodificar_morse(morse):
    texto_plano = ""  # Aquí alojamos el resultado
    for caracter_morse in morse.split(" "):
        if caracter_morse == (""):
            texto_plano += " "
        # Por cada carácter, buscamos su equivalencia
        caracter_plano = morse_a_caracter_plano(caracter_morse)
        # Lo concatenamos al resultado.

        texto_plano += caracter_plano

    return texto_plano


def caracter_plano_a_morse(caracter):
    if caracter in equivalencias:
        return equivalencias[caracter]
    else:
        # Si no existe, regresamos una cadena vacía
        return ""


def codificar_morse(texto_plano):
    # A mayúsculas para evitar hacer más comparaciones
    texto_plano = texto_plano.upper()
    morse = ""  # Aquí alojamos el resultado
    for caracter in texto_plano:
        # Por cada carácter, buscamos su equivalencia
        caracter_codificado = caracter_plano_a_morse(caracter)
        # Lo concatenamos al resultado, además de agregar un espacio
        morse += caracter_codificado + " "
    return morse


palabra = voz

codificado = codificar_morse(palabra)
print(codificado)

decodificado = decodificar_morse(codificado)
print(decodificado)
