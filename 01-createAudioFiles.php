<?php
//Audiodateien fuer GME-Erstellung generieren und in passendem Ordner ablegen.
//Falls bei der ZIP-Extrahierung ein falscher Dateiname fuer die .mscx-Datei erstellt wird, Datei in Musescore offnen und kleine Aenderung speichern
//mit 7ZIP gegenpruefen

require_once('config.php');

echo "use python";
return;

emptyDirectory("{$audioDir}/Temp");

//Taktart
$timeSignature = "4_4";

//Audio Dateien in verschiedenen Tempi erstellen aus Musescore Dateien
foreach ($pages as $page => $data) {
  echo $page . "\n";

  //TTS fuer Anmeldebutton: "Noten lesen 2"
  $header = $data["header"];
  exec("balcon -t \"{$header}\" -l ger -w {$audioDir}/Temp/tts.wav");
  exec("ffmpeg -i {$audioDir}/Temp/tts.wav -af equalizer=f=300:t=h:width=200:g=-30 {$audioDir}/Temp/tts-eq.wav -hide_banner -loglevel error -y");
  exec("ffmpeg -i {$audioDir}/Temp/tts-eq.wav -af acompressor=threshold=-11dB:ratio=9:attack=200:release=1000:makeup=8 {$audioDir}/audio/header_{$page}.mp3 -hide_banner -loglevel error -y");

  foreach ($data["names"] as $nameArr) {
    $name = $nameArr[0];
    echo "  " . $name . "\n";

    //mscz zu xml extrahieren
    $zip = new ZipArchive;
    $zip->open("{$audioDir}/mscz-audio/{$name}.mscz");
    $zip->extractTo("{$audioDir}/Temp");
    $zip->close();

    //XML laden, hier kann man das Tempo aendern
    $mscxPath = "{$audioDir}/Temp/" . $name . ".mscx";
    $xml = simplexml_load_file($mscxPath);
    $first_tempo = $xml->xpath('//tempo')[0];

    //Ueber Tempos einer Uebung gehen
    foreach ($tempos as $tempoName => $tempo) {
      $first_tempo[0] = $tempo["mult"];
      $xml->asXML($mscxPath);

      //mp3-Erzeugung
      $mp3Path = "{$audioDir}/Temp/" . $name . "_" . $tempoName . ".mp3";
      shell_exec("MuseScore4.exe " . $mscxPath . " -o " . $mp3Path);

      //mp3 normalisieren
      $mp3NormPath = "{$audioDir}/Temp/" . $name . "_" . $tempoName . "_norm.mp3";
      shell_exec("ffmpeg -y -hide_banner -loglevel panic -i {$mp3Path} -af loudnorm -ar 44100 {$mp3NormPath}");

      //countInFile + mp3-File mergen
      $countInFile = "{$audioDir}/count-in/" . $tempo["value"] . "_{$timeSignature}.mp3";
      $finalFile = "{$audioDir}/audio/{$name}_{$tempoName}.mp3";
      $mergeCommand = "ffmpeg -y -hide_banner -loglevel panic -i \"concat:{$countInFile}|{$mp3NormPath}\" -acodec copy {$finalFile}";
      shell_exec($mergeCommand);
    }
  }
}

emptyDirectory("{$audioDir}/Temp");

function emptyDirectory($dir)
{
  $files = scandir($dir);
  foreach ($files as $file) {
    if ($file == '.' || $file == '..') {
      continue;
    }
    if (is_file("$dir/$file")) {
      unlink("$dir/$file");
    } elseif (is_dir("$dir/$file")) {
      emptyDirectory("$dir/$file");
      rmdir("$dir/$file");
    }
  }
}
