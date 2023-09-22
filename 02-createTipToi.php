<?php
// A: GME-Datei erzeugen
//   1: YAML-Datei mit Play-Codes erstellen
//   2: GME erzeugen mit tttool
// B: PDF mit TipToi-Codes erzeugen
//   1: HTML erstellen mit Header + Code images
//   2: OID-Code-PNGs erstellen mit tttool
//   3: Abgerundete Version von OID-Code-PNGs erstellen mit Imagick
//   4: PDF-Datei mit MPDF
// C: Noten-PDF aus mscz-Datei
//   1: PDF-Datei mit Musescore
//Druck bei 1200 dpi

require_once __DIR__ . '/vendor/autoload.php';

use Mpdf\Mpdf;

//sollen runde Bilder generiert werden?
$roundedImages = false;

// Read the JSON file
$json = file_get_contents("config.json");

// Parse the JSON data
$jsonData = json_decode($json, true);

//windows vs. linux
$mode = $jsonData["mode"];
$audioDir = $jsonData["audioDir" . ucfirst($mode)];
chdir($audioDir);

$activePages = [
    //"noten_lesen_01",
    //"noten_lesen_02",
    //"noten_lesen_03",
    //"rhythmus_uebung_01",
    //"lieder_01",
    //"noten_lesen_04",
    //"noten_lesen_05",
    //"rhythmus_uebung_02",
    //"lieder_02",
    //"noten_lesen_06",
    //"noten_lesen_07",
    //"noten_lesen_08",
    //"lieder_03",
    //"rhythmus_uebung_03",
    //"noten_lesen_09",
    //"noten_lesen_10",
    #"noten_lesen_11",
    #"noten_lesen_12",
    #"lieder_04",
    #"rhythmus_uebung_04",
    #"noten_lesen_13",
    "lieder_05",
];

//HTML erstellen fuer PDF-Generierung
foreach ($activePages as $page) {
    $data = $jsonData["pages"][$page];
    $product_id = $data["product_id"];
    echo "Create print and sheet pdf files for project " . $product_id . "-" . $page . "\n";

    //HTML fuer TT-PDF-Datei mit Codes erstellen: Ueberschrift oben
    $html = "<table><tr><td class='t_c'><h1>" . $data["header"] . "</h1></td>";
    $html .= "</tr></table>";

    //Anmelde-Symbol rechts mit negativem Margin, damit h1 zentriert ist
    if ($roundedImages) {
        $html .= "<div style='margin-top: -75px;' class='t_r'><img src='oid-" . $product_id . "-START_rounded.png' /></div>";
    } else {
        $html .= "<div style='margin-top: -75px;' class='t_r'><img src='oid-" . $product_id . "-START.png' /></div>";
    }

    $info = $data["info"] ?? "";
    if ($info) {
        $html .= "<h2>Info</h2>" . $info;
    }

    //Stop-Symbol
    if ($roundedImages) {
        $html .= "<h2 style='margin-left:20px; margin-bottom:10px'>Stop</h2><img src='oid-" . $product_id . "-stop_rounded.png' />";
    } else {
        $html .= "<h2 style='margin-left:20px; margin-bottom:10px'>Stop</h2><img src='oid-" . $product_id . "-stop.png' />";
    }

    //Yaml-Datei erzeugen
    $yaml_file = $product_id . "-" . $page . ".yaml";
    $fh = fopen($yaml_file, "w");
    fwrite($fh, "product-id: " . $product_id . "\n\n");
    fwrite($fh, "comment: \"Notenbuch von Martin Helfer\"\n\n");
    fwrite($fh, "gme-lang: GERMAN\n\n");
    fwrite($fh, "welcome: start,header_{$page}\n\n");
    fwrite($fh, "media-path: audio/%s\n\n");
    fwrite($fh, "scripts:\n");

    //Ueber Rows (=Uebungen) des Projekts gehen
    $imgArr = [
        "oid-{$product_id}-START",
        "oid-{$product_id}-stop"
    ];
    foreach ($data["names"] as $i => $name) {

        //Ueberschrift der Uebung ("Uebung 1" vs. "Rechte Hand")
        //TODO: Abstand zwischen Uebungen vergroessern
        $label = $name[1] ?? "Übung " . ($i + 1);
        $html .= "<div><h2 style='margin-left: 10px'>" . $label . "</h2>";

        //Tempos einer Uebung in Tabelle sammeln
        $td_row = "";
        foreach ($jsonData["tempos"] as $tempoId => $tempoData) {

            //Code-Benennung fuer YAML-Datei und code-images
            $code_id = $name[0] . "_" . $tempoId;

            //Tempo Bild
            $imgArr[] = "oid-{$product_id}-{$code_id}";
            $td_row .= "<td><img style='margin-left: 20px; margin-bottom: 3px' src='png/speed_" . $tempoId . ".png' /><br>";

            //OID-Code
            if ($roundedImages) {
                $td_row .= "<img src='oid-" . $product_id . "-" . $code_id . "_rounded.png' />";
            } else {
                $td_row .= "<img src='oid-" . $product_id . "-" . $code_id . ".png' />";
            }

            //Checkbox
            $td_row .= "<img class='checkbox' width=20 height=20 src='" . __DIR__ . "/checkbox.svg' /></td>";

            //Abspielcode in YAML-Datei als Script hinterlegen
            fwrite($fh, "  " . $code_id . ": P(" . $code_id . ")\n");
        }

        //fuer diese Uebung eine Tabelle anlegen
        $html .= "<table><tr>" . $td_row . "</tr></table></div>";
    }
    fclose($fh);

    //GME-Datei erstellen
    //Windows version
    if ($mode === "windows") {
        shell_exec('tttool assemble ' . $yaml_file);
    }

    //Linux version
    else {
        shell_exec('/etc/tttool assemble ' . $yaml_file);
    }

    //OID-Codes
    //Windows version
    if ($mode === "windows") {
        shell_exec('tttool oid-codes ' . $yaml_file . ' --pixel-size 5 --code-dim 20');
    }

    //Linux version
    else {
        shell_exec('/etc/tttool oid-codes ' . $yaml_file . ' --pixel-size 5 --code-dim 20');
    }

    //Runde Bilder erstellen
    if ($roundedImages) {
        foreach ($imgArr as $imgName) {
            createRoundImage($imgName);
        }
    }

    //Ueber Rows (=Uebungen) und Tempos des Projekts gehen und png-Bilder anpassen (Tempo ueber Code legen)
    /*
foreach ($project_config["rows"] as $name) {
foreach ($name["tempos"] as $tempo) {
$image = "oid-" . $product_id . "-t_" . $name["id"] . "_" . $tempo . ".png";
addTextToImage($image, $tempo);
}
}
 */

    //PDF-Datei vorbereiten
    $mpdf = new Mpdf([
        'default_font' => 'grundschrift-regular'
    ]);
    $mpdf->img_dpi = 1200;
    $stylesheet = file_get_contents(__DIR__ . '/styles.css');
    $mpdf->WriteHTML($stylesheet, \Mpdf\HTMLParserMode::HEADER_CSS);
    $mpdf->WriteHTML($html, \Mpdf\HTMLParserMode::HTML_BODY);

    //Footer mit aktuellem Datum
    //$mpdf->SetHTMLFooter("<small>" . gmdate("d.m.Y", time()) . "</small>");

    //pdf als Datei speichern
    $mpdf->Output($product_id . "-" . $page . " (codes).pdf");

    //Aus mscz-Datei eine PDF-Datei erzeugen
    $mscz_file = $audioDir . "/mscz-sheet/" . $page . ".mscz";

    //PDF Erzeugung
    //Windows Version 
    if ($mode === "windows") {
        $mscz_to_pdf_command = 'MuseScore4.exe "' . $mscz_file . '" -o "' . $audioDir . "/" . $product_id . "-" . $page . ' (sheet).pdf"';
    }

    //Linux Version
    else {
        $mscz_to_pdf_command =   '/etc/musescore4/AppRun "' . $mscz_file . '" -o "' . $audioDir
            . "/" . $product_id . "-" . $page . ' (sheet).pdf"';
    }
    shell_exec($mscz_to_pdf_command);
}
cleanDir();

function createRoundImage($imgName)
{
    global $audioDir;
    $sourceImagePath = "{$audioDir}/{$imgName}.png";
    $imagick = new \Imagick($sourceImagePath);
    $imagick->setImageBackgroundColor('transparent');
    $imagick->roundCorners($imagick->getImageWidth() / 2, $imagick->getImageHeight() / 2);
    $savePath = "{$audioDir}/{$imgName}_rounded.png";
    $imagick->writeImage($savePath);
    $imagick->destroy();
}

//Bilddatei mit Text ueberlagern
/*
function addTextToImage($image, $text, $font_size = 250)
{

    //Bildobjekt erstellen
    $png_image = imagecreatefrompng($image);

    //Textfarbe schwarz und Schriftart setzen
    $black = imagecolorallocate($png_image, 0, 0, 0);
    $font_path = __DIR__ . '/arial-outline.ttf';

    //Text einfuegen
    imagettftext($png_image, $font_size, 0, 35, 350, $black, $font_path, $text);

    //Bild speichern und mem leeren
    imagepng($png_image, $image);
    imagedestroy($png_image);
}
*/

//Dateisystem aufraeumen, temp. Dateien loeschen
function cleanDir()
{
    foreach (glob("{oid-*.png,*.yaml}", GLOB_BRACE) as $file) {
        unlink($file);
    }
}
