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

with open('config.json', encoding='utf-8') as f:
    json_data = json.load(f)

# windows vs. linux
mode = json_data["mode"]
instrument = json_data["instrument"]
audioDir = json_data["audioDir" + str.capitalize(mode)]
tempDir = json_data["tempDir" + str.capitalize(mode)]
tempDirLinux = json_data["tempDirLinux"]
pages = json_data["pages"]

# Files for which audio is created
activePages = json_data["activePages"]
# TTS fuer Anmeldebutton: "Noten lesen 2"


def create_tts(tts):
    header = tts["header"]
    page = tts["page"]

    print(f'tts "{header}"')

    # Windows version
    # Nov. 2023: pico2wave per wsl Aufruf
    if (mode == "windows"):
        # cmd = f'balcon -t "{header}" -l ger -w {tempDir}/{page}-tts.wav'
        cmd = f'wsl -e pico2wave -l de-DE -w {tempDirLinux}/{page}-tts.wav "{header}"'

    # Linux version
    elif (mode == 'linux'):
        cmd = f'pico2wave -l de-DE -w {tempDir}/{page}-tts.wav "{header}"'

    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    # normalize
    os.system(
        f'ffmpeg -i {tempDir}/{page}-tts.wav -af equalizer=f=300:t=h:width=200:g=-30 {tempDir}/{page}-tts-eq.wav -hide_banner -loglevel error -y')
    os.system(
        f'ffmpeg -i {tempDir}/{page}-tts-eq.wav -af acompressor=threshold=-11dB:ratio=9:attack=200:release=1000:makeup=8 {audioDir}/audio/{instrument}/header_{page}.mp3 -hide_banner -loglevel error -y')

# Audio files aus Musescore generieren in div. Tempi


def create_audio(song):
    name = song[0]
    tempos = song[1]
    count_in = song[2]
    pre_count_in = song[3]

    print(f'audio "{name}"')
    # print(f'count_in "{count_in}"')
    # print(f'pre_count_in "{pre_count_in}"')
    # print(f'tempos "{tempos}"')

    # mscz zu xml extrahieren
    with zipfile.ZipFile(f'{audioDir}/mscz-audio/{instrument}/{name}.mscz') as zip:
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
        countInFile = f'{audioDir}/audio/count-in/{tempo["value"]}_{count_in}.mp3'
        finalFile = f'{audioDir}/audio/{instrument}/{name}_{tempoName}.mp3'

        # merge command fuer Normalisierung mit ffmpeg
        # mergeCommand = f'ffmpeg -y -hide_banner -loglevel panic -i "concat:{preCountInFile}|{countInFile}|{mp3NormPath}" -acodec copy {finalFile}'

        # Signal vor Einzaehler
        preCountInFile = f'{audioDir}/audio/count-in/pre_count_in_{pre_count_in}.mp3'

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
            # inactive pages uebergehen
            if page.startswith(' '):
                # print("ignore " + page)
                continue

            data = pages[instrument][page]

            # Header sammeln pro Blatt fuer TTS bei TT-Anmeldung
            tts.append({
                "page": page,
                "header": data["header"]
            })

            # tempos
            tempos = data["tempos"] if "tempos" in data else [
                "60"] * len(data["names"])

            # time signature
            count_in = data["count_in"] if "count_in" in data else [
                "4_4"] * len(data["names"])

            # pre count in note
            pre_count_in = data["pre_count_in"] if "pre_count_in" in data else [
                "c"] * len(data["names"])

            # Uebungen eines Blatts sammeln fuer Audio Creation aus MS
            for idx, nameArr in enumerate(data["names"]):
                names.append([nameArr[0], json_data["tempos"][tempos[idx]],
                             count_in[idx], pre_count_in[idx]])

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
