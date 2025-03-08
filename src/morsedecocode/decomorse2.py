import pyaudio  # Librería para trabajar con audio en tiempo real
import numpy as np  # Librería para operaciones numéricas
import time  # Para manejar temporizadores y pausas

# Diccionario de Código Morse: Mapeo de secuencias de morse a letras y números
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

# Configuración de audio:
FORMAT = pyaudio.paInt16  # Formato de los datos de audio (16 bits por muestra)
CHANNELS = 1  # Mono (un solo canal)
RATE = 44100  # Frecuencia de muestreo: 44.1 kHz (calidad de CD)
CHUNK = 1024  # Tamaño de cada bloque de datos de audio que se procesa
THRESHOLD = 500  # Umbral para detectar si el sonido es lo suficientemente fuerte
DOT_LENGTH = 0.2  # Duración de un punto en código morse (en segundos)
WORD_GAP = 0.7  # Duración de la pausa entre palabras (en segundos)

# Función principal para detectar código morse desde un micrófono
def detect_morse():
    p = pyaudio.PyAudio()  # Inicializa PyAudio para la captura de audio
    # Abre un flujo de entrada de audio desde el micrófono
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    
    print("Escuchando código Morse...")  # Mensaje inicial
    
    # Variables para almacenar la secuencia de morse y el estado de la detección
    morse_sequence = ""  # Secuencia completa de código morse
    current_letter = ""  # Letra en construcción (secuencia morse actual)
    last_sound_time = None  # Marca de tiempo del último sonido detectado
    detecting = False  # Estado de detección de sonido (si hay un sonido actual)
    last_pause_time = None  # Marca de tiempo de la última pausa detectada
    
    try:
        while True:
            # Lee los datos del micrófono (bloques de audio)
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            amplitude = np.max(np.abs(data))  # Calcula la amplitud del sonido

            # Si el sonido es mayor que el umbral, estamos detectando un punto o raya
            if amplitude > THRESHOLD:
                if not detecting:  # Si no estamos ya detectando sonido
                    detecting = True
                    last_sound_time = time.time()  # Registra el tiempo del inicio del sonido
                    # Si hubo una pausa larga, asumimos que es una nueva palabra
                    if last_pause_time and time.time() - last_pause_time > WORD_GAP:
                        morse_sequence += " "  # Añadimos espacio entre palabras
            else:
                # Si el sonido ha terminado (no se detecta sonido)
                if detecting:
                    duration = time.time() - last_sound_time  # Duración del sonido detectado
                    detecting = False
                    
                    # Si la duración del sonido es corta (menor que DOT_LENGTH), es un punto
                    if duration < DOT_LENGTH:
                        current_letter += '.'  # Agrega un punto a la letra
                    else:
                        current_letter += '-'  # Agrega una raya a la letra
                    
                    print(f"Detectado: {current_letter}")  # Muestra lo que se ha detectado

                    # Si la duración de la pausa es mayor que DOT_LENGTH, hemos terminado una letra
                    if time.time() - last_sound_time > DOT_LENGTH:
                        morse_sequence += current_letter + " "  # Añade la letra detectada a la secuencia
                        current_letter = ""  # Restablece la letra actual
                    
                    last_pause_time = time.time()  # Registra el tiempo de la pausa
                    time.sleep(0.1)  # Pausa corta entre detecciones de sonido
                
    except KeyboardInterrupt:  # Si se interrumpe el programa (Ctrl+C)
        print("\nFinalizando...")  # Mensaje final
        stream.stop_stream()  # Detiene el flujo de audio
        stream.close()  # Cierra el flujo
        p.terminate()  # Termina PyAudio

        # Convertir Morse a texto
        words = morse_sequence.split(" ")  # Separar las palabras por espacios
        decoded_message = "".join([MORSE_CODE_DICT.get(letter, "?") for letter in words])  # Decodificar a texto
        print(f"\nMensaje decodificado: {decoded_message}")  # Muestra el mensaje decodificado

# Ejecutar la detección de código morse
detect_morse()
