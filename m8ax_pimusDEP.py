####################################################################################################################################
#
#  Programado Por Marcos Ochoa Diez - M8AX - MvIiIaX - 16-Ene-2023
#
#  Programa Para Generar Música Con Los Decimales De PI - 3.(14159....).
#  Se Creará Un Fichero Midi, Otro Ogg Y Un M4a, Con La Música De Los Decimales De PI.
#  También Se Creará Un Video Con La Música Y Con El Fondo m8axpimusic.png
#  La Música Se Generará Así... Decimales De PI - 0,1,2,3,4,5,6,7,8,9 - Notas - "C", "D", "E", "F", "G", "A", "B", "C5", "D5", "E5".
#  Se Necesita Un Fichero Pi_Dec.TxT, Con Los Decimales De PI, Que Queremos Transformar En Música... Se Incluye Fichero Con 50000.
#  La Duración De Cada Nota, Será De 0.4s.
#  En El Video, Saldrá El Decimal De PI En Grande, Que Suena En Ese Momento, Así Como... El WaveForm Del Audio...
#  Al Final Tendremos 4 Ficheros, El Midi, El Ogg, El M4a Y El MP4 Con Los Resultados Y Los Metadatos Añadidos...
#  El Fichero M4A Es También El Sonido De Los Decimales De PI, Pero Comprimido Con La Libreria libfdk_aac aac_he_v2 Que Ocupa Menos.
#  Ejemplo - py m8ax_pimusDEP.py
#
####################################################################################################################################

import time
import math
import numpy as np
import sys
import music21
import os
import errno
import cv2
import glob
from music21 import *
from subprocess import call
from os import remove

def segahms(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas * 60 * 60
    minutos = int(segundos / 60)
    segundos -= minutos * 60
    return f"{horas}h:{minutos}m:{int(segundos)}s"

def barra_progreso_vibrante(progreso, total, tiembarra):
    porcen = 100 * (progreso / float(total))
    segrestante = 0
    if porcen > 0:
        segrestante = (100 * (tiembarra - time.time()) / porcen) - (tiembarra - time.time())
    barra = "█" * int(porcen) + "-" * (100 - int(porcen))
    print(
        (
            f"\r\033[38;2;{np.random.randint(0, 256)};{np.random.randint(0, 256)};{np.random.randint(0, 256)}m|{barra}|"
            f" - ETA - {segahms(segrestante*-1)} - {porcen:.2f}%      "
        ),
        end="\r\033[0m",
    )

with open("Pi_Dec.TxT", "r") as file:
    ficherillo = file.read()
    caratot = len(ficherillo)
file.close()
os.system("cls")
s = stream.Stream()
note_list = ["C", "D", "E", "F", "G", "A", "B", "C5", "D5", "E5"]
cuenta = 0
tiembarra = time.time()
print(
    f"... Comienzo Del Programa ...\n\n... Haciendo Ficheros Jpg, Con Cada Decimal De PI, En El"
    f" Centro ...\n"
)
font = cv2.FONT_HERSHEY_TRIPLEX
with open("Pi_Dec.TxT", "r") as file:
    for line in file:
        for char in line:
            cuenta += 1
            img = cv2.imread("m8axpimusic.png")
            ubica = (565, 950)
            tamale = 40
            colorle = (
                np.random.randint(0, 256),
                np.random.randint(0, 256),
                np.random.randint(0, 256),
            )
            grosorle = 22
            cv2.putText(img, char, ubica, font, tamale, colorle, grosorle)
            ubica = (42, 27)
            tamale = 0.9
            grosorle = 2
            cv2.putText(
                img, "Decimal NUM# - " + str(cuenta), ubica, font, tamale, colorle, grosorle
            )
            cv2.imwrite("M8AX-" + str(cuenta) + ".Jpg", img, [cv2.IMWRITE_JPEG_QUALITY,35])
            note = note_list[int(char)]
            d = music21.duration.Duration(0.4)
            n = music21.note.Note(note, quarterLength=d.quarterLength)
            s.append(n)
            barra_progreso_vibrante((cuenta * 100) / (caratot), 100, tiembarra)
barra_progreso_vibrante((caratot * 100) / (caratot), 100, tiembarra)
print(
    f"\n\n... {cuenta} Decimales De PI Procesados En Ficheros Jpg ...\n\n... Creando Video, Con"
    " Cada Decimal De PI En Pantalla Y Sin Sonido ...\n"
)
mf = midi.translate.music21ObjectToMidiFile(s)
mf.open("M8AX-Pi-Decimals.Mid", "wb")
mf.write()
mf.close()
file.close()
tiemp = time.time()
nn = 0
framesize = ((1920), (1080))
outv = cv2.VideoWriter("M8AX-Video-Temporal.Mp4", cv2.VideoWriter_fourcc(*"h265"), 5, framesize)
print("")
for filename in sorted(glob.glob("*.jpg"), key=os.path.getmtime):
    imgv = cv2.imread(filename)
    outv.write(imgv)
    nn += 1
    barra_progreso_vibrante((nn * 100) / len(glob.glob("*.jpg")), 100, tiemp)
barra_progreso_vibrante((len(glob.glob("*.jpg")) * 100) / len(glob.glob("*.jpg")), 100, tiemp)
print("\n")
print(*sorted(glob.glob("*.jpg"), key=os.path.getmtime), sep="\n")
outv.release()
print("\n... Video Con Cada Decimal De PI En Pantalla Y Sin Sonido, Realizado Correctamente ...")
print("\n... Música De Decimales De PI, Creada Correctamente En Formato Midi ...")
print(f"\n... Introduciendo Metadatos En Video MP4 ...\n")
call(
    [
        "ffmpeg",
        "-threads",
        "8",
        "-i",
        "M8AX-Video-Temporal.Mp4",
        "-map",
        "0",
        "-metadata",
        "episode_id=M8AX - La Música De PI",
        "-metadata",
        "copyright=-///\\\ --- MvIiIaX & M8AX 2020 - 2030 --- ///\\\-",
        "-metadata",
        "description=Mi Página En OnCyber - https://oncyber.io/m8ax",
        "-metadata",
        "genre=--- MarcoS OchoA DieZ ---",
        "-metadata",
        "grouping=--- MarcoS OchoA DieZ ---",
        "-metadata",
        "album_artist=MvIiIaX - M8AX - THE ALGORITHM MAN - M8AX - MvIiIaX",
        "-metadata",
        "author=--- MarcoS OchoA DieZ ---",
        "-metadata",
        "show=Mi Canal De Youtube - https://youtube.com/m8ax",
        "-metadata",
        "grouping=Mi Blog - https://mviiiaxm8ax.blogspot.com",
        "-metadata",
        (
            "comment=1 - Por Muchas Vueltas Que Demos, Siempre Tendremos El Culo Atrás... 2 - El"
            " Futuro... No Esta Establecido, Solo Existe... El Que Nosotros Hacemos... 3 - Música"
            " De Decimales De PI, Compilada En Honor A MDDD Por M8AX... 4 - El Miedo Es El Camino"
            " Hacia El Lado Oscuro, El Miedo Lleva A La Ira, La Ira Lleva Al Odio, El Odio Lleva Al"
            " Sufrimiento... 5 - Yo He Visto Cosas Que Vosotros No Creeriais. Atacar Naves En"
            " Llamas Mas Alla De Orion. He Visto Rayos-C Brillar En La Oscuridad Cerca De La Puerta"
            " De Tannhauser. Todos Esos Momentos Se Perderan En El Tiempo, Como Lagrimas En La"
            " Lluvia. Es Hora De Morir..."
        ),
        "-metadata",
        "title=M8AX - La Música De PI",
        "-codec",
        "copy",
        "M8AX-Pi-Temporal.Mp4",
    ]
)
print("\n... Metadatos Añadidos A Video Correctamente ...")
print(f"\n... Convirtiendo Midi A Audio Ogg ...\n")
call(
    [
        "fluidsynth",
        "-nli",
        "-r",
        "44100",
        "-g",
        "2",
        "-o",
        "synth.cpu-cores=16",
        "-T",
        "oga",
        "-F",
        "M8AX-Pi-Temporal.Ogg",
        "m8ax.sf2",
        "M8AX-Pi-Decimals.Mid",
    ]
)
print(f"\n... Audio Convertido, Introduciendo Metadatos En Audio Ogg ...\n")
call(
    [
        "ffmpeg",
        "-threads",
        "8",
        "-i",
        "M8AX-Pi-Temporal.Ogg",
        "-map",
        "0",
        "-metadata",
        "episode_id=M8AX - La Música De PI",
        "-metadata",
        "copyright=-///\\\ --- MvIiIaX & M8AX 2020 - 2030 --- ///\\\-",
        "-metadata",
        "description=Mi Página En OnCyber - https://oncyber.io/m8ax",
        "-metadata",
        "genre=--- MarcoS OchoA DieZ ---",
        "-metadata",
        "grouping=--- MarcoS OchoA DieZ ---",
        "-metadata",
        "album_artist=MvIiIaX - M8AX - THE ALGORITHM MAN - M8AX - MvIiIaX",
        "-metadata",
        "author=--- MarcoS OchoA DieZ ---",
        "-metadata",
        "show=Mi Canal De Youtube - https://youtube.com/m8ax",
        "-metadata",
        "grouping=Mi Blog - https://mviiiaxm8ax.blogspot.com",
        "-metadata",
        (
            "comment=1 - Por Muchas Vueltas Que Demos, Siempre Tendremos El Culo Atrás... 2 - El"
            " Futuro... No Esta Establecido, Solo Existe... El Que Nosotros Hacemos... 3 - Música"
            " De Decimales De PI, Compilada En Honor A MDDD Por M8AX... 4 - El Miedo Es El Camino"
            " Hacia El Lado Oscuro, El Miedo Lleva A La Ira, La Ira Lleva Al Odio, El Odio Lleva Al"
            " Sufrimiento... 5 - Yo He Visto Cosas Que Vosotros No Creeriais. Atacar Naves En"
            " Llamas Mas Alla De Orion. He Visto Rayos-C Brillar En La Oscuridad Cerca De La Puerta"
            " De Tannhauser. Todos Esos Momentos Se Perderan En El Tiempo, Como Lagrimas En La"
            " Lluvia. Es Hora De Morir..."
        ),
        "-metadata",
        "title=M8AX - La Música De PI",
        "-codec",
        "copy",
        "M8AX-Pi-Decimals.Ogg",
    ]
)
print("\n... Metadatos Añadidos A Audio Correctamente ...")
print(
    f"\n... Haciendo Video MP4, Añadiendo WaveForm - Ondas De Sonido Al Video Y El Propio Sonido"
    f" ...\n"
)
call(
    [
        "ffm8ax",
        "-threads",
        "8",
        "-i",
        "M8AX-Pi-Decimals.Ogg",
        "-i",
        "M8AX-Pi-Temporal.Mp4",
        "-filter_complex",
        "[0:a]showwaves=s=1920x800:mode=line:rate=60,colorkey=0x000000:0.01:0.1,format=yuva420p[v];[1:v]scale=1920:1080[bg];[bg][v]overlay=x=W-w-0:y=500[outv]",
        "-map",
        "[outv]",
        "-map",
        "0:a",
        "-c:v",
        "hevc_amf",
        "-c:a",
        "libfdk_aac",
        "-profile:a",
        "aac_he_v2",
        "-b:a",
        "32k",
        "M8AX-Pi-Decimal.Mp4",
    ]
)
print(f"\n... Aplicando Correcciones Al Video Final ...\n")
call(
    [
        "ffmpeg",
        "-threads",
        "8",
        "-i",
        "M8AX-Pi-Temporal.Mp4",
        "-i",
        "M8AX-Pi-Decimal.Mp4",
        "-map",
        "1",
        "-map_metadata",
        "0",
        "-c",
        "copy",
        "M8AX-Pi-Decimals.Mp4",
    ]
)
print(f"\n... Correcciones Realizadas ...")
print(f"\n... Haciendo Audio M4A AAC_HE_V2 Y Añadiendo Metadatos Al Mismo ...\n")
call(
    [
        "ffm8ax",
        "-threads",
        "8",
        "-i",
        "M8AX-Pi-Decimals.Ogg",
        "-map",
        "0",
        "-metadata",
        "episode_id=M8AX - La Música De PI",
        "-metadata",
        "copyright=-///\\\ --- MvIiIaX & M8AX 2020 - 2030 --- ///\\\-",
        "-metadata",
        "description=Mi Página En OnCyber - https://oncyber.io/m8ax",
        "-metadata",
        "genre=--- MarcoS OchoA DieZ ---",
        "-metadata",
        "grouping=--- MarcoS OchoA DieZ ---",
        "-metadata",
        "album_artist=MvIiIaX - M8AX - THE ALGORITHM MAN - M8AX - MvIiIaX",
        "-metadata",
        "author=--- MarcoS OchoA DieZ ---",
        "-metadata",
        "show=Mi Canal De Youtube - https://youtube.com/m8ax",
        "-metadata",
        "grouping=Mi Blog - https://mviiiaxm8ax.blogspot.com",
        "-metadata",
        (
            "comment=1 - Por Muchas Vueltas Que Demos, Siempre Tendremos El Culo Atrás... 2 - El"
            " Futuro... No Esta Establecido, Solo Existe... El Que Nosotros Hacemos... 3 - Música"
            " De Decimales De PI, Compilada En Honor A MDDD Por M8AX... 4 - El Miedo Es El Camino"
            " Hacia El Lado Oscuro, El Miedo Lleva A La Ira, La Ira Lleva Al Odio, El Odio Lleva Al"
            " Sufrimiento... 5 - Yo He Visto Cosas Que Vosotros No Creeriais. Atacar Naves En"
            " Llamas Mas Alla De Orion. He Visto Rayos-C Brillar En La Oscuridad Cerca De La Puerta"
            " De Tannhauser. Todos Esos Momentos Se Perderan En El Tiempo, Como Lagrimas En La"
            " Lluvia. Es Hora De Morir..."
        ),
        "-metadata",
        "title=M8AX - La Música De PI",
        "-c:a",
        "libfdk_aac",
        "-profile:a",
        "aac_he_v2",
        "-b:a",
        "32k",
        "M8AX-Pi-Decimals.M4a",
    ]
)
print(f"\n... Fichero De Audio M4A Creado ...\n")
remove("M8AX-Pi-Temporal.Mp4")
remove("M8AX-Pi-Decimal.Mp4")
remove("M8AX-Pi-Temporal.Ogg")
remove("M8AX-Video-Temporal.Mp4")
files = glob.glob("m8ax*.jpg")
for f in files:
    os.remove(f)
print(f"... Ficheros Temporales Borrados, Todo Correcto ...")
print(
    f"\n---------------------------------------------------------------------------------------------------------------------------------\n\n..."
    f" TRABAJO FINALIZADO ...\n\n... LOS TIEMPOS DE CÁLCULO SE CALCULAN UNA VEZ FINALIZADO TODO EL"
    f" PROCESO, ES DECIR, CONTANDO EL PASO A VIDEO ETC"
    f" ...\n\n---------------------------------------------------------------------------------------------------------------------------------\n"
)
print(
    "Tiempo De Proceso -"
    f" {segahms(time.time()-tiembarra)}\n\n{round(cuenta/(time.time()-tiembarra),3)} Dec_PI/Seg."
    f" Pasados A Audio/Video...\n\n{round((cuenta*60)/(time.time()-tiembarra),3)} Dec_PI/Min."
    f" Pasados A Audio/Video...\n\n{round((cuenta*3660)/(time.time()-tiembarra),3)} Dec_PI/Hora."
    " Pasados A Audio/Video..."
)
print(
    "\n... Trabajo Realizado Correctamente ...\n\n... By M8AX ...\n\n..."
    " https://youtube.com/m8ax ..."
)