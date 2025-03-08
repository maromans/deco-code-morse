import pyaudio
import numpy as np
import time

# Diccionario de Código Morse
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9'
}

# Configuración de audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 1000  # Frecuencia de muestreo
CHUNK = 1024 # Tamaño del bloque de audio
THRESHOLD = 300  # Umbral de detección de sonido

# Duraciones en segundos
DOT_LENGTH = 0.3  # Punto
DASH_LENGTH = DOT_LENGTH * 3  # Raya
LETTER_GAP = DOT_LENGTH * 3  # Espacio entre letras
WORD_GAP = DOT_LENGTH * 7  # Espacio entre palabras

def detect_morse():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    
    print("Escuchando código Morse...\n")

    decoded_text = ""  # Texto decodificado en tiempo real
    current_morse_letter = ""  # Código Morse de la letra en construcción
    last_sound_time = None
    detecting = False
    silence_start = None

    try:
        while True:
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            amplitude = np.max(np.abs(data))  # Obtener volumen del sonido
            
            if amplitude > THRESHOLD:
                if not detecting:
                    detecting = True
                    last_sound_time = time.time()
                    if silence_start is not None:
                        silence_duration = time.time() - silence_start
                        if silence_duration >= WORD_GAP:
                            decoded_text += " "  # Espacio entre palabras
                            print("\nPalabra detectada:", decoded_text)
                        elif silence_duration >= LETTER_GAP:
                            # Convertir Morse a letra y agregar al texto decodificado
                            letter = MORSE_CODE_DICT.get(current_morse_letter, "?")
                            decoded_text += letter
                            print("Letra detectada:", letter, " | Texto hasta ahora:", decoded_text)
                            current_morse_letter = ""  # Reiniciar código Morse de la letra actual

                silence_start = None
            else:
                if detecting:
                    duration = time.time() - last_sound_time
                    detecting = False
                    
                    if DOT_LENGTH * 0.8 <= duration <= DOT_LENGTH * 1.2:
                        current_morse_letter += '.'  # Punto
                    elif DASH_LENGTH * 0.8 <= duration <= DASH_LENGTH * 1.2:
                        current_morse_letter += '-'  # Raya
                    
                    silence_start = time.time()
                
    except KeyboardInterrupt:
        print("\nFinalizando...")
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Convertir última letra si quedó sin procesar
        if current_morse_letter:
            letter = MORSE_CODE_DICT.get(current_morse_letter, "?")
            decoded_text += letter
            print("Letra final detectada:", letter)

        print(f"\nMensaje final decodificado: {decoded_text}")

# Ejecutar la detección
detect_morse()
