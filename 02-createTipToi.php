<?php

//TipToi-GME-Datei erstellen, dazu TipToi-PDF mit Codes und Noten-PDF aus mscz-Datei
//count-in-Dateien muessen vorliegen
//Druck bei 1200 dpi

use Mpdf\Mpdf;

require_once('config.php');
require_once __DIR__ . '/vendor/autoload.php';

chdir($audioDir);

//Audio Dateien in verschiedenen Tempi erstellen aus Musescore Dateien
foreach ($pages as $page => $data) {
    $product_id = $data["product_id"];
    echo "Create print and sheet pdf files for project " . $product_id . "-" . $page . "\n";


    //HTML fuer TT-PDF-Datei mit Codes erstellen: Ueberschrift oben
    $html = "<table><tr><td class='t_c'><h1>" . $data["header"] . "</h1></td>";

    //Anmelde-Symbol
    $html .= "<td style='width:100px;' class='t_r'><img src='oid-" . $product_id . "-START.png' /></td>";
    $html .= "</tr></table>";

    //Info anzeigen, falls gesetzt (z.B. andere Taktart, Auftakt, etc.)
    $info = $data["info"] ?? "";
    if ($info) {
        $html .= "<h2>Info</h2>" . $info;
    }

    //Stop-Symbol
    $html .= "<h2>Stop</h2><img src='oid-" . $product_id . "-stop.png' />";

    //Yaml-Datei erzeugen
    $yaml_file = $product_id . "-" . $page . ".yaml";
    $fh = fopen($yaml_file, "w");
    fwrite($fh, "product-id: " . $product_id . "\n\n");
    fwrite($fh, "comment: \"Notenbuch von Martin Helfer\"\n\n");
    fwrite($fh, "gme-lang: GERMAN\n\n");
    fwrite($fh, "welcome: start,header_{$page}\n\n");
    fwrite($fh, "media-path: audio/%s\n\n");
    fwrite($fh, "scripts:\n");
    //fwrite($fh, "  stop: P(stop)\n");

    //Ueber Rows (=Uebungen) des Projekts gehen
    foreach ($data["names"] as $i => $name) {

        //Ueberschrift der Uebung ("Uebung 1" vs. "Rechte Hand")
        $label = $name[1] ?? "Übung " . ($i + 1);
        $html .= "<div><h2>" . $label . "</h2>";

        //Tempos einer Uebung in Tabelle sammeln
        $td_row = "";

        //Ueber tempos einer Uebung gehen
        foreach ($tempos as $tempoId => $tempoData) {

            //Code-Benennung fuer YAML-Datei und code-images
            $code_id = $name[0] . "_" . $tempoId;

            //Tempo Bild, OID-Code + Checkbox
            $td_row .= "<td><img style='margin-left: 20px; margin-bottom: 3px' src='png/speed_" . $tempoId . ".png' /><br>";
            $td_row .= "<img src='oid-" . $product_id . "-" . $code_id . ".png' />";
            $td_row .= "<img class='checkbox' width=20 height=20 src='" . __DIR__ . "/checkbox.svg' /></td>";

            //Abspielcode in YAML-Datei als Script hinterlegen
            fwrite($fh, "  " . $code_id . ": P(" . $code_id . ")\n");
        }

        //fuer diese Uebung eine Tabelle anlegen
        $html .= "<table><tr>" . $td_row . "</tr></table></div>";
    }
    fclose($fh);

    //GME-Datei und OID-Codes erstellen
    shell_exec('tttool assemble ' . $yaml_file);
    shell_exec('tttool oid-codes ' . $yaml_file . ' --pixel-size 5 --code-dim 20');

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
    //TODO: Schriftart
    //TODO: Grundschrift Bold in musescore
    $mpdf = new Mpdf([
        'default_font' => 'Grundschrift'
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
    $mscz_to_pdf_command = 'MuseScore4.exe "' . $mscz_file . '" -o "' . $audioDir . "/" . $product_id . "-" . $page . ' (sheet).pdf"';
    $mscz_to_pdf_command;
    shell_exec($mscz_to_pdf_command);
}
cleanDir();

//Bilddatei mit Text ueberlagern
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

//Dateisystem aufraeumen, temp. Dateien loeschen
function cleanDir()
{
    foreach (glob("{oid-*.png,*.yaml}", GLOB_BRACE) as $file) {
        unlink($file);
    }
}
