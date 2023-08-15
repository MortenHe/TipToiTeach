15.08.2023
01 -> Windwos (WSL Musescore 4.1 geht nicht)
02 -> Windows (WSL Musescore 4.1 geht nicht)

Idee
roundedImage + pico2wave in eigene Skripte



01 -> Python Code läuft parallel (WSL)
- WSL 2023 (wegen pico2wave):
- Musescore 4 als AppImage nach C:\ herunterladen und extrahieren nach /etc/musescore4
- ./Musescore.4.0..... --appimage-extract
- mkdir /etc/musescore4
- mv ./squashfs-root/ /etc/musescore4

  https://djobbo.hashnode.dev/a-practical-guide-to-using-appimages-on-wsl2

- Soundfont fuer psst, Pau - se etc. in passenden Ordner kopieren
  cp /mnt/c/Users/Martin/Documents/MuseScore4/SoundFonts/mh-tiptoi.sf2 /etc/musescore4/share/mscore4portable-4.0/sound

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