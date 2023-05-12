# from mpdf import Mpdf
import os
import time
import subprocess
from config import audioDir, pages, tempos

os.chdir(audioDir)

# Files for which tiptoi is created
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

if __name__ == '__main__':

    start_time = time.time()
    for page in activePages:
        data = pages[page]

        product_id = data["product_id"]
        print(
            f'Create print and sheet pdf files for project {product_id}-{page}')

        # HTML fuer TT-PDF-Datei mit Codes erstellen: Ueberschrift oben
        html = f'<table><tr><td class="t_l"><h1>{data["header"]}</h1></td>'

        # Anmelde-Symbol
        html += f'<td style="width:100px" class="t_r"><img src="oid-{product_id}-START.png" /></td>'
        html += "</tr></table>"

        # Info anzeigen, falls gesetzt (z.B. andere Taktart, Auftakt, etc.)
        info = data.get("info", "")
        if info:
            html += "<h2>Info</h2>" + info

        # Stop-Symbol
        html += f'<h2>Stop</h2><img src="oid-{product_id}-stop.png" />'

        # Yaml-Datei erzeugen
        yaml_file = f"{product_id}-{page}.yaml"
        with open(yaml_file, "w") as f:
            f.write(f"product-id: {product_id}\n\n")
            f.write('comment: "Notenbuch von Martin Helfer"\n\n')
            f.write("gme-lang: GERMAN\n\n")
            f.write(f'welcome: start,header_{page}\n\n')
            f.write("media-path: audio/%s\n\n")
            f.write("scripts:\n")

            for i, name in enumerate(data["names"]):
                # Heading of the exercise ("Exercise 1" vs "Right Hand")
                label = name[1] if len(name) > 1 else "Übung " + str(i+1)
                html += "<div><h2>" + label + "</h2>"

                # Collect tempos of an exercise in a table
                td_row = ""

                # Iterate through tempos of an exercise
                for tempoId, tempoData in tempos.items():
                    # Code naming for YAML file and code images
                    code_id = name[0] + "_" + tempoId

                    # Tempo image, OID code + checkbox
                    td_row += f'<td><img style=!margin-left: 20px; margin-bottom: 3px! src="png/speed_{tempoId}.png" /><br>'
                    td_row += f'<img src="oid-{product_id}-{code_id}.png" />'

                    svg_path = os.path.join(
                        os.path.dirname(__file__), "checkbox.svg")
                    td_row += f'<img class="checkbox" width=20 height=20 src="{svg_path})" /></td>'

                    # Store playback code in YAML file as script
                    f.write(f'  {code_id}: P({code_id})\n')

                    # Create a table for this exercise
                    html += f'<table><tr>{td_row}</tr></table></div>'

                    os.system(f'tttool assemble {yaml_file}')
                    os.system(
                        f'tttool oid-codes {yaml_file} --pixel-size 5 --code-dim 20')

            # create new mpdf object
            # mpdf = Mpdf(default_font='Grundschrift')
            # mpdf.img_dpi = 1200

            # read stylesheet
            # stylesheet = open(__DIR__ + '/styles.css').read()

            # write HTML and stylesheet to pdf
            # mpdf.WriteHTML(stylesheet, \Mpdf\HTMLParserMode.HEADER_CSS)
            # mpdf.WriteHTML(html, \Mpdf\HTMLParserMode.HTML_BODY)

            # set footer with current date
            # mpdf.SetHTMLFooter("<small>" + datetime.utcnow().strftime("%d.%m.%Y") + "</small>")

            # save pdf file
            # mpdf.Output(product_id + "-" + page + " (codes).pdf")

            # convert mscz file to pdf
            mscz_file = f'{audioDir}/mscz-sheet/{page}.mscz'
            mscz_to_pdf_command = f'MuseScore4.exe "{mscz_file}" -o "{audioDir}/{product_id}-{page} (sheet).pdf"'
            subprocess.run(mscz_to_pdf_command, shell=True)
