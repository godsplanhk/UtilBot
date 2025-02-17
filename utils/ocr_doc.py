import ocrmypdf
from PyPDF2 import PdfReader
import os
import docx
import pypandoc

def convert_docx_to_pdf(input_path, output_path):
    pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)

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
    filename =inputPdf.split(".")[0]
    f.save("./out/" + filename + ".docx")
    convert_docx_to_pdf("./out/"+filename+".docx","./pdf/"+filename+".pdf")
    return "./out/pdf/" + filename+".pdf"
