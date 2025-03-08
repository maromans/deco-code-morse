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
RATE = 44100  # Frecuencia de muestreo
CHUNK = 1024  # Tamaño del bloque de audio
THRESHOLD = 500  # Umbral de detección de sonido
DOT_LENGTH = 0.2  # Duración de un punto en segundos

def detect_morse():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    
    print("Escuchando código Morse...")
    
    morse_sequence = ""
    last_sound_time = None
    detecting = False
    
    try:
        while True:
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            amplitude = np.max(np.abs(data))  # Obtener volumen del sonido
            
            if amplitude > THRESHOLD:
                if not detecting:
                    detecting = True
                    last_sound_time = time.time()
            else:
                if detecting:
                    duration = time.time() - last_sound_time
                    detecting = False
                    
                    if duration < DOT_LENGTH:
                        morse_sequence += '.'  # Punto
                    else:
                        morse_sequence += '-'  # Raya
                    
                    print(f"Detectado: {morse_sequence}")
                    
                    # Espacio entre letras
                    time.sleep(0.2)
                
    except KeyboardInterrupt:
        print("\nFinalizando...")
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Convertir Morse a texto
        words = morse_sequence.split(" ")  # Separar palabras
        decoded_message = "".join([MORSE_CODE_DICT.get(letter, "?") for letter in words])
        print(f"\nMensaje decodificado: {decoded_message}")

# Ejecutar la detección
detect_morse()
