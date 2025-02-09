import ocrmypdf
from PyPDF2 import PdfReader
import os
import docx


def qExtractor(inputPdf):
    count = 0
    if not os.path.isfile("./in/OCR/" + inputPdf):
        ocrmypdf.ocr(
            "./in/" + inputPdf,
            "./in/OCR/" + inputPdf,
            language=["hin", "eng"],
        )
    else:
        return "./out/" + inputPdf.split('.')[0]+".docx"
    reader = PdfReader("./in/OCR/" + inputPdf)
    f = docx.Document()
    f.styles["Normal"].font.name = "Arial"
    print(len(reader.pages))
    page = reader.pages[5]
    text = page.extract_text()
    for page in reader.pages:
        count += 1
        text = page.extract_text()
        out = "\n\n" + str(count) + ") " + text.rstrip()
        print(out)
        f.add_paragraph(out)
    f.save("./out/" + inputPdf.split(".")[0] + ".docx")
    return "./out/" + inputPdf.split(".")[0]+".docx"
