# A: TTS fuer Anmeldebutton ("Noten lesen 3")
#   1. pico2wave
#   2. mp3 normalisieren

# B: Audios fuer Uebungen erstellen aus Musescore
#   1. mscz -> mscx
#   2. Tempo anpassen im XML
#   3. mp3 exportieren
#   4. mp3 normalisieren
#   5. Count-in file + mp3 mergen -> finale mp3

import multiprocessing
import os
import shutil
# import sys
# import signal
import zipfile
from xml.etree import ElementTree as ET
import subprocess
import time
import json

# windows vs. linux
mode = 'linux'

json_file = 'config.json'
with open(json_file) as f:
    data = json.load(f)

audioDir = data["audioDir" + str.capitalize(mode)]
tempDir = data["tempDir" + str.capitalize(mode)]
timeSignature = data["timeSignature"]
tempos = data["tempos"]
pages = data["pages"]

# Signal vor Einzaehler
preCountInFile = f'{audioDir}/count-in/pre_count_in.mp3'

# Files for which audio is created
activePages = [
    # "noten_lesen_01",
    # "noten_lesen_02",
    # "noten_lesen_03",
    # "rhythmus_uebung_01",
    # "lieder_01",
    # "noten_lesen_04",
    # "noten_lesen_05",
    # "rhythmus_uebung_02",
    # "lieder_02",
    # "noten_lesen_06",
    # "noten_lesen_07",
    # "noten_lesen_08",
    # "lieder_03",
    # "rhythmus_uebung_03",
    # "noten_lesen_09",
    # "noten_lesen_10",
    # "noten_lesen_11",
    # "noten_lesen_12",
    "lieder_04",
]

# TTS fuer Anmeldebutton: "Noten lesen 2"


def create_tts(tts):
    header = tts["header"]
    page = tts["page"]

    print(f'tts "{header}"')

    # Windows version
    if (mode == "windows"):
        cmd = f'balcon -t "{header}" -l ger -w {tempDir}/{page}-tts.wav'

    # Linux version
    elif (mode == 'linux'):
        cmd = f'pico2wave -l de-DE -w {tempDir}/{page}-tts.wav "{header}"'

    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    # normalize
    os.system(
        f'ffmpeg -i {tempDir}/{page}-tts.wav -af equalizer=f=300:t=h:width=200:g=-30 {tempDir}/{page}-tts-eq.wav -hide_banner -loglevel error -y')
    os.system(
        f'ffmpeg -i {tempDir}/{page}-tts-eq.wav -af acompressor=threshold=-11dB:ratio=9:attack=200:release=1000:makeup=8 {audioDir}/audio/header_{page}.mp3 -hide_banner -loglevel error -y')

# Audio files aus Musescore generieren in div. Tempi


def create_audio(name):
    print(f'audio "{name}"')

    # mscz zu xml extrahieren
    with zipfile.ZipFile(f'{audioDir}/mscz-audio/{name}.mscz') as zip:
        zip.extractall(f'{tempDir}/{name}')

    # XML laden, hier kann man das Tempo aendern
    mscxPath = f'{tempDir}/{name}/{name}.mscx'
    xml = ET.parse(mscxPath)
    first_tempo = xml.find('.//tempo')

    # Ueber Tempos einer Uebung gehen
    for tempoName, tempo in tempos.items():
        first_tempo.text = str(tempo["mult"])
        xml.write(mscxPath)
        mp3Path = f'{tempDir}/{name}_{tempoName}.mp3'

        # mp3-Erzeugung
        # Windows version
        if (mode == 'windows'):
            subprocess.run(['MuseScore4.exe', mscxPath, '-o', mp3Path])

        # Linux fersion
        elif (mode == 'linux'):
            mscommand = f'/etc/musescore4/AppRun {mscxPath} -o {mp3Path}'
            subprocess.run(mscommand, shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # mp3 normalisieren mit ffmpeg
        # mp3NormPath = f'{tempDir}/{name}_{tempoName}_norm.mp3'
        # subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'panic',
        #                '-i', mp3Path, '-af', 'loudnorm', '-ar', '44100', mp3NormPath])

        # mp3 normalisieren mit mp3gain
        # TODO: Abfrage y/n weg -q?
        subprocess.run(['mp3gain', '-r', mp3Path])

        # countInFile + mp3-File mergen
        countInFile = f'{audioDir}/count-in/{tempo["value"]}_{timeSignature}.mp3'
        finalFile = f'{audioDir}/audio/{name}_{tempoName}.mp3'

        # merge command fuer Normalisierung mit ffmpeg
        # mergeCommand = f'ffmpeg -y -hide_banner -loglevel panic -i "concat:{preCountInFile}|{countInFile}|{mp3NormPath}" -acodec copy {finalFile}'

        # merge command fuer Normalisierung mit mp3gain
        mergeCommand = f'ffmpeg -y -hide_banner -loglevel panic -i "concat:{preCountInFile}|{countInFile}|{mp3Path}" -acodec copy {finalFile}'
        subprocess.run(mergeCommand, shell=True)

 # Delete all files and folders inside the directory


def empty_dir():
   # Remove all files and subdirectories inside the directory
    for filename in os.listdir(tempDir):
        file_path = os.path.join(tempDir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == '__main__':
    try:
        start_time = time.time()
        empty_dir()

        # sys.exit(0)
        tts = []
        names = []
        for page in activePages:
            data = pages[page]

            # Header sammeln pro Blatt fuer TTS bei TT-Anmeldung
            tts.append({
                "page": page,
                "header": data["header"]
            })

            # Uebungen eines Blatts sammeln fuer Audio Creation aus MS
            for nameArr in data["names"]:
                names.append(nameArr[0])

        # Run tts creation processes in parallel
        ttsPool = multiprocessing.Pool(processes=50)
        ttsPool.map(create_tts, tts)
        print("tts creation done")

        # Run audio creation processes in parallel
        audioPool = multiprocessing.Pool(processes=50)
        audioPool.map(create_audio, names)
        print("audio creation done")

        empty_dir()

        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
    except KeyboardInterrupt:
        ttsPool.terminate()
        ttsPool.join()

        audioPool.terminate()
        audioPool.join()
        print('Exiting...')
