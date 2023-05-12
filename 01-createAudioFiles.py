import multiprocessing
import os
import shutil
import sys
import signal
import zipfile
from xml.etree import ElementTree as ET
import subprocess
import time
from config import audioDir, tempDir, pages, tempos, timeSignature

# Files for which audio is created
activePages = [
    # "noten_lesen_01",
    # "noten_lesen_02",
    # "noten_lesen_03",
    "rhythmus_uebung_01",
    "lieder_01",
    # "noten_lesen_04",
    # "noten_lesen_05",
    # "rhythmus_uebung_02",
    # "lieder_02",
    # "noten_lesen_06",
    # "noten_lesen_07",
    # "noten_lesen_08",
    # "lieder_03",
]

# TTS fuer Anmeldebutton: "Noten lesen 2"


def create_tts(tts):
    header = tts["header"]
    page = tts["page"]

    print(f'tts "{header}"')

    # command to execute
    cmd = f'balcon -t "{header}" -l ger -w {tempDir}/{page}-tts.wav'

    # execute the command and suppress the output
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
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

        # mp3-Erzeugung
        mp3Path = f'{tempDir}/{name}_{tempoName}.mp3'
        subprocess.run(['MuseScore4.exe', mscxPath, '-o', mp3Path])

        # mp3 normalisieren
        mp3NormPath = f'{tempDir}/{name}_{tempoName}_norm.mp3'
        subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'panic',
                        '-i', mp3Path, '-af', 'loudnorm', '-ar', '44100', mp3NormPath])
        # countInFile + mp3-File mergen
        countInFile = f'{audioDir}/count-in/{tempo["value"]}_{timeSignature}.mp3'
        finalFile = f'{audioDir}/audio/{name}_{tempoName}.mp3'
        mergeCommand = f'ffmpeg -y -hide_banner -loglevel panic -i "concat:{countInFile}|{mp3NormPath}" -acodec copy {finalFile}'
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

        # for page, data in pages.items():
            # Header sammeln pro Blatt fuer TTS bei TT-Anmeldung
            tts.append({
                "page": page,
                "header": data["header"]
            })

            for nameArr in data["names"]:
                # Ueberung eines Blatts sammeln fuer Audio Creation aus MS
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
