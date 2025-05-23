import numpy as np
from pydub import AudioSegment
from collections import Counter
import random
import os

def chiffrement_cesar(message, cle):
    message_chiffre = ""
    for caractere in message:
        if caractere.isalpha():
            base = ord('A') if caractere.isupper() else ord('a')
            message_chiffre += chr((ord(caractere) - base + cle) % 26 + base)
        else:
            message_chiffre += caractere
    return message_chiffre

def string_2_char_tab(s):
    return list(s)

def verif_no_NULL(l):
    for char in l:
        if ord(char) == 0:
            return False
    return True

def replace_NULL_2_space(l):
    for i in range(len(l)):
        if ord(l[i]) == 0:
            l[i] = ' '
    return l

def ajout_marche_arret(l):
    start = [chr(c) for c in b'STARTMSG']
    end = [chr(c) for c in b'ENDMSG']
    return start + l + end

def convertir_en_liste_binaire(liste_caracteres):
    liste_binaire = []
    for char in liste_caracteres:
        binaire = bin(ord(char))[2:].zfill(8)
        liste_binaire.extend([int(bit) for bit in binaire])
    return liste_binaire

def gen_audio_path(audio_path, new_suffix):
    file_parts = audio_path.rsplit('.', 1)
    if len(file_parts) != 2:
        raise ValueError("Le chemin du fichier doit avoir une extension valide.")
    file_name, file_extension = file_parts
    new_file_name = f"{file_name}{new_suffix}.{file_extension}"
    return new_file_name

def ecriture(audio_path, output_path, bit_array):
    file_extension = audio_path.split('.')[-1].lower()
    if file_extension == 'mp3':
        audio = AudioSegment.from_mp3(audio_path)
    elif file_extension == 'wav':
        audio = AudioSegment.from_wav(audio_path)
    else:
        raise ValueError("Format de fichier non supporté. Utilisez MP3 ou WAV.")
    samples = np.array(audio.get_array_of_samples())

    if len(bit_array) > len(samples):
        raise ValueError("pas la place")

    start_position = random.randint(0, len(samples) - len(bit_array) - 1)
    for i in range(len(bit_array)):
        bit_value = bit_array[i]
        if bit_value == 0:
            samples[i + start_position] = samples[i + start_position] & ~1
        else:
            samples[i + start_position] = samples[i + start_position] | 1

    modified_audio = audio._spawn(samples.tobytes())
    new_path = os.path.join("templates", os.path.basename(output_path))
    if file_extension == 'mp3':
        modified_audio.export(new_path, format="mp3")
        new_path = os.path.join("static/js", os.path.basename(output_path))
        modified_audio.export(new_path, format="mp3")
        new_path = os.path.join("upload", os.path.basename(output_path))
        modified_audio.export(new_path, format="mp3")
    elif file_extension == 'wav':
        modified_audio.export(new_path, format="wav")
        new_path = os.path.join("static/js", os.path.basename(output_path))
        modified_audio.export(new_path, format="wav")
        new_path = os.path.join("upload", os.path.basename(output_path))
        modified_audio.export(new_path, format="wav")
    return new_path

def motif_marqueur(mot):
    return [int(bit) for c in mot for bit in bin(ord(c))[2:].zfill(8)]

def steganographie(audio_path, text, key=None):
    if key is None:
        char_txt = string_2_char_tab(text)
    else:
        char_txt = string_2_char_tab(chiffrement_cesar(text, key))
    if not verif_no_NULL(char_txt):
        char_txt = replace_NULL_2_space(char_txt)
    char_txt = ajout_marche_arret(char_txt)
    bits_list_txt = convertir_en_liste_binaire(char_txt)
    audio_path_out = gen_audio_path(audio_path, "___MODIFF___")
    return ecriture(audio_path, audio_path_out, bits_list_txt)

def find_marker(marker, arr, start=0):
    for i in range(start, len(arr) - len(marker) + 1):
        if arr[i:i+len(marker)] == marker:
            return i
    return -1

def lecture(audio_path, key=None):
    file_extension = audio_path.split('.')[-1].lower()
    if file_extension == 'mp3':
        audio = AudioSegment.from_mp3(audio_path)
    elif file_extension == 'wav':
        audio = AudioSegment.from_wav(audio_path)
    else:
        raise ValueError("Format de fichier non supporté. Utilisez MP3 ou WAV.")
    samples = np.array(audio.get_array_of_samples())

    # Marqueurs binaires
    start_marker = motif_marqueur("STARTMSG")
    end_marker = motif_marqueur("ENDMSG")
     # Récupère tous les LSB
    lsb_array = [s & 1 for s in samples]

    start_index = find_marker(start_marker, lsb_array)
    if start_index != -1:
        start_index += len(start_marker)
    end_index = find_marker(end_marker, lsb_array, start_index)

    bit_array = lsb_array[start_index:end_index]
    char_array = []
    for i in range(0, len(bit_array), 8):
        byte = bit_array[i:i + 8]
        if len(byte) == 8:
            char_array.append(chr(int(''.join(map(str, byte)), 2)))

    message = ''.join(char_array)
    if key is not None:
        message = chiffrement_cesar(message, -key)


    # Frequency analysis
    freq_fr = {'e': 14.715, 'a': 7.636, 'i': 7.529, 's': 7.948, 'n': 7.095,
               'r': 6.553, 't': 6.046, 'o': 5.796, 'l': 5.469, 'u': 4.639,
               'd': 3.669, 'c': 3.260, 'm': 2.968, 'p': 2.521, 'g': 1.001}

    message_freq = Counter(char.lower() for char in message if char.isalpha())
    total_letters = sum(message_freq.values())
    message_freq = {char: (count / total_letters) * 100 for char, count in message_freq.items()}

    score = sum(abs(message_freq.get(char, 0) - freq_fr[char]) for char in freq_fr)
    return message

