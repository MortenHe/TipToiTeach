21.08.2023
Skript 01 und 02 geht mit Windows
Imagick Windows 10 + PHP 8.2 geht

(zum Zeitpunkt keine Version für 8.2 vorhanden, daher Links unten)
https://mlocati.github.io/articles/php-windows-imagick.html


https://github.com/Imagick/imagick/issues/573#issuecomment-1431773928
https://github.com/Imagick/imagick/issues/573#issuecomment-1578638424
https://stackoverflow.com/questions/75138367/php-warning-php-startup-imagick-unable-to-initialize-module


16.08.2023
01 - WSL 4.1 geht
02 - WSL 4.1 geht 

15.08.2023
01 -> Windwos (WSL mit Scores aus Musescore 4.1 geht nicht)
02 -> Windows (WSL mit Scores aus Musescore 4.1 geht nicht)

Linux musescore-Aufruf ggf. -f (force) bei Versionsproblemen

Idee
roundedImage + pico2wave in eigene Skripte



01 -> Python Code läuft parallel (WSL)
- WSL 2023 (wegen pico2wave):
- Musescore 4 als AppImage nach C:\ herunterladen und extrahieren nach /etc/musescore4
- ./Musescore.4.1..... --appimage-extract
- sudo mkdir /etc/musescore4
- sudo mv ./squashfs-root/* /etc/musescore4

  https://djobbo.hashnode.dev/a-practical-guide-to-using-appimages-on-wsl2

- Soundfont fuer psst, Pau - se etc. in passenden Ordner kopieren
  cp /mnt/c/Users/Martin/Documents/MuseScore4/SoundFonts/mh-tiptoi.sf2 /etc/musescore4/share/mscore4portable-4.1/sound

02 -> PHP Code (WSL)
- MPDF: Custom Font
  https://www.youtube.com/watch?v=gAZLrpwdYyw
  Grundschrift.ttf nach vendor/mpdf/mpdf/ttfonts kopieren
  vendor/mpdf/mpdf/src/Config/FontVariables.php
  in fontdata Object Wert einfuegen
  "grundschrift" => [
			'R' => "Grundschrift-Regular.ttf",
	],
  in styles.css font-family nutzen (schon erledigt)
  body {
    font-family: 'grundschrift';
  }


- WSL 2023: 
- sudo apt install mp3gain
- sudo apt-get install php-mbstring
- sudo apt-get install php-xml
- tttool herunterladen und nach WSL verschieben
  sudo mv /mnt/c/Users/Martin/Desktop/tttool /etc/tttool

- Windows Fonts zugänglich machen
  https://x410.dev/cookbook/wsl/sharing-windows-fonts-with-wsl/
  cd /etc/fonts
  sudo vi local.conf
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
    <dir>/mnt/c/Windows/Fonts</dir>
</fontconfig>