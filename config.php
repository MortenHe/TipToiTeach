<?php

//Dir fuer mp3 Erzeugung aus Musescore Noten
$audioDir = "C:/Users/Martin/Desktop/Nextcloud/Martin/TipToiTeach";

//Files fuer die Audio erstellt wird
$pages = [
    "noten_lesen_01" => [
        "product_id" => 925,
        "header" => "Noten lesen 1",
        "info" => "Spiele jede Übung erst im langsamen, dann im mittleren und zum Schluss im schnellen Tempo. Hake die Übungen ab, die du geschafft hast.",
        "names" => [
            ["noten_lesen_01_1"],
            ["noten_lesen_01_2"],
            ["noten_lesen_01_3"]
        ]
    ],
    //"noten_lesen_02_1",
    //"noten_lesen_02_2",
    //"noten_lesen_02_3",
    //"rhythmus_01_1",
    //"rhythmus_01_2",
    //"rhythmus_01_3",
    //"song_01_wo_bist_du",
];

//Liste der Tempos pro Musescore Datei
$tempos = [
    //Tempo 60 => 60 / 60
    "snail" => [
        "value" => 60,
        "mult" => 1
    ],
    //Tempo 70 => 70 / 60
    "horse" =>
    [
        "value" => 70,
        "mult" => 1.1666
    ],
    //Tempo 80 => 80 / 60
    "cheetah" =>  [
        "value" => 80,
        "mult" => 1.3333
    ]
];

//Taktart
$timeSignature = "4_4";

/*
//Headerbereich der YAML-Datei
$output = "product-id: 925
comment: \"Notenbuch von Martin Helfer\"
welcome: start, welcome
gme-lang: GERMAN
media-path: Audio/%s";

//Scripts der YAML-Datei
$data = [
    "01-das-klavier" => [
        ["klavier", 5, "single"],
        ["glissando"],
        ["klavier_tief", 2, "multi"],
        ["klavier_mittel", 2, "multi"],
        ["klavier_hoch", 2, "multi"],
        ["keys", 3, "multi"],
        ["der_ton_c"],
        ["draw_c_und_d", 2, "multi"],
        ["words_with_c"],
        ["der_ton_d"],
        ["words_with_d"],
    ],
    "02-die-notenschrift" => [
        ["notenschrift", 4, "single"],
        ["viertelnote", 2, "multi"],
        ["notenlinien", 3, "multi"],
        ["notenlinien_mit_noten", 2, "multi"],
        ["notenlinien_mit_allem", 2, "multi"],
        ["noten_c_und_d"],
        ["draw_noten_c_und_d", 2, "multi"],
    ],
    "03-noten-lesen-01" => [
        ["uebung_01_explain", 2, "multi"],
        ["faster_than_cheetah", 2, "multi"],
        ["fingers_01_explain"],
        ["fingers_01_repeat"],
        ["stop_explain"],

        ["noten_lesen_01_1_snail"],
        ["noten_lesen_01_1_horse"],
        ["noten_lesen_01_1_cheetah"],
        ["noten_lesen_01_2_snail"],
        ["noten_lesen_01_2_horse"],
        ["noten_lesen_01_2_cheetah"],
        ["noten_lesen_01_3_snail"],
        ["noten_lesen_01_3_horse"],
        ["noten_lesen_01_3_cheetah"],
    ],
    "04-der-ton-e" => [
        ["der_ton_e"],
        ["draw_e", 2, "multi"],
        ["words_with_e"],
        ["recognize_notes_e", 2, "multi"],
        ["write_notes_e"],
    ],
    "05-noten-lesen-02" => [
        ["uebung_02_explain"],
        ["fingers_02_explain", 2, "multi"],
        ["fingers_02_repeat"],
        ["notes_and_fingers_short"],

        ["noten_lesen_02_1_snail"],
        ["noten_lesen_02_1_horse"],
        ["noten_lesen_02_1_cheetah"],
        ["noten_lesen_02_2_snail"],
        ["noten_lesen_02_2_horse"],
        ["noten_lesen_02_2_cheetah"],
        ["noten_lesen_02_3_snail"],
        ["noten_lesen_02_3_horse"],
        ["noten_lesen_02_3_cheetah"],
    ],
    "06-viertelpause" => [
        ["viertelpause"],
        ["make_a_break", 2, "multi"],
        ["rest_01_explain", 2, "multi"],

        ["rhythmus_01_1_snail"],
        ["rhythmus_01_1_horse"],
        ["rhythmus_01_1_cheetah"],
        ["rhythmus_01_2_snail"],
        ["rhythmus_01_2_horse"],
        ["rhythmus_01_2_cheetah"],
        ["rhythmus_01_3_snail"],
        ["rhythmus_01_3_horse"],
        ["rhythmus_01_3_cheetah"],
    ],

    "07-wo-bist-du" => [
        ["song_01_explain", 2, "multi"],
        ["wo_bist_du", 2, "multi"],
        ["summary_01_explain"],
        ["summary_piano"],
        ["summary_c", 2, "multi"],
        ["summary_d", 2, "multi"],
        ["summary_e", 2, "multi"],
        ["summary_viertelnote"],
        ["summary_viertelpause"],
        ["summary_notenlinien"],
        ["summary_violinschluessel"],
        ["summary_vier_viertel_takt"],
        ["summary_01_fingersatz"],
        ["summary_notenlinie_komplett", 2, "multi"],

        ["song_01_wo_bist_du_snail"],
        ["song_01_wo_bist_du_horse"],
        ["song_01_wo_bist_du_cheetah"],
    ],
];
*/