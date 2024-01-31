<?php

//2024: 3 Piano Audios aus kombinierter Datei erzeugen

//mscz -> musicxml

//volume auf 0 setzen -> Audio export
$msczDir = "C:/Users/Martin/Desktop";
$fileName = "lieder13";

$musicxmlFilePath = "{$msczDir}/mxml/{$fileName}.musicxml";

$command = "Musescore4.exe {$msczDir}/{$fileName}.mscz -o {$musicxmlFilePath}";
exec($command);



//Lautstaerke-Tags holen (Klavier 1, Klavier 2, Gitarre, div. Percussions)
$muteParts = [1, 2];

foreach ($muteParts as $mutePart) {

    $domdoc = new DOMDocument();
    $domdoc->loadXML(file_get_contents($musicxmlFilePath));
    $xpath = new DOMXPath($domdoc);

    $xpath->query("//score-part[@id='P{$mutePart}']/*/volume")->item(0)->nodeValue = 0;

    $fh = fopen("{$msczDir}/mxml/temp{$mutePart}.musicxml", "w");
    fwrite($fh, $domdoc->saveXML());
    fclose($fh);


    exec("Musescore4.exe {$msczDir}/mxml/temp{$mutePart}.musicxml -o {$msczDir}/mxml/solo{$mutePart}.mp3");
}
