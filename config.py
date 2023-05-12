# Directory for mp3 generation from Musescore notes
audioDir = "C:/Users/Martin/Desktop/Nextcloud/Martin/TipToiTeach"
tempDir = "C:/Users/Martin/Desktop/media/TipToiTeachTemp"

# Files for which audio is created
pages = {
    "noten_lesen_01": {
        "product_id": 801,
        "header": "Noten lesen 1",
        "info": "Spiele jede Übung erst im langsamen, dann im mittleren und zum Schluss im schnellen Tempo.<br>Hake die Übungen ab, die du geschafft hast.<br>Vor jeder Übung werden 4 Schläge eingezählt.",
        "names": [
            ["noten_lesen_01_1"],
            ["noten_lesen_01_2"],
            ["noten_lesen_01_3"]
        ]
    },
    "noten_lesen_02": {
        "product_id": 802,
        "header": "Noten lesen 2",
        "names": [
            ["noten_lesen_02_1"],
            ["noten_lesen_02_2"],
            ["noten_lesen_02_3"]
        ]
    },
    "noten_lesen_03": {
        "product_id": 803,
        "header": "Noten lesen 3",
        "names": [
            ["noten_lesen_03_1"],
            ["noten_lesen_03_2"],
            ["noten_lesen_03_3"]
        ]
    },
    "rhythmus_uebung_01": {
        "product_id": 804,
        "header": "Rhythmus Übung 1",
        "names": [
            ["rhythmus_uebung_01_1"],
            ["rhythmus_uebung_01_2"],
            ["rhythmus_uebung_01_3"]
        ]
    },
    "lieder_01": {
        "product_id": 805,
        "header": "Lieder 1",
        "names": [
            ["lieder_01_1_wo_bist_du", "Wo bist du?"],
            ["lieder_01_2_lauf_lauf", "Lauf, lauf"],
            ["lieder_01_3_ich_will_in_den_garten_gehn",
                "Ich will in den Garten geh'n"]
        ]
    },
    "noten_lesen_04": {
        "product_id": 806,
        "header": "Noten lesen 4",
        "names": [
            ["noten_lesen_04_1"],
            ["noten_lesen_04_2"],
            ["noten_lesen_04_3"]
        ]
    },
    "noten_lesen_05": {
        "product_id": 807,
        "header": "Noten lesen 5",
        "names": [
            ["noten_lesen_05_1"],
            ["noten_lesen_05_2"],
            ["noten_lesen_05_3"]
        ]
    },
    "rhythmus_uebung_02": {
        "product_id": 808,
        "header": "Rhythmus Übung 2",
        "names": [
            ["rhythmus_uebung_02_1"],
            ["rhythmus_uebung_02_2"],
            ["rhythmus_uebung_02_3"]
        ]
    },
    "lieder_02": {
        "product_id": 809,
        "header": "Lieder 2",
        "names": [
            ["lieder_02_1_ding_dong_ding", "Ding Dong Ding"],
            ["lieder_02_2_auf_den_berg", "Auf den Berg"],
            ["lieder_02_3_ich_bin_muede", "Ich bin müde"]
        ]
    },
    "noten_lesen_06": {
        "product_id": 810,
        "header": "Noten lesen 6",
        "names": [
            ["noten_lesen_06_1"],
            ["noten_lesen_06_2"],
            ["noten_lesen_06_3"]
        ]
    },
    "noten_lesen_07": {
        "product_id": 811,
        "header": "Noten lesen 7",
        "names": [
            ["noten_lesen_07_1"],
            ["noten_lesen_07_2"],
            ["noten_lesen_07_3"]
        ]
    },
    "noten_lesen_08": {
        "product_id": 812,
        "header": "Noten lesen 8",
        "names": [
            ["noten_lesen_08_1"],
            ["noten_lesen_08_2"],
            ["noten_lesen_08_3"]
        ]
    },
    "lieder_03": {
        "product_id": 813,
        "header": "Lieder 3",
        "names": [
            ["lieder_03_1_haenschen_klein", "Hänschen klein"]
        ]
    }
}

# List of tempos per Musescore file
tempos = {
    # Tempo 60 => 60 / 60
    "snail": {
        "value": 60,
        "mult": 1
    },
    # Tempo 70 => 70 / 60
    "horse": {
        "value": 70,
        "mult": 1.1666
    },
    # Tempo 80 => 80 / 60
    "cheetah": {
        "value": 80,
        "mult": 1.3333
    }
}

timeSignature = "4_4"
