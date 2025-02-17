import ocrmypdf
from PyPDF2 import PdfReader
import os
import docx
import pypandoc

WNS_COLS_NUM = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num"
def convert_docx_to_pdf(input_path, output_path):
    pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)


def set_number_of_columns(section, cols):
    """ sets number of columns through xpath. """
    section._sectPr.xpath("./w:cols")[0].set(WNS_COLS_NUM, str(cols))
def qExtractor(inputPdf):
    count = 0
    if not os.path.isfile("./in/OCR/" + inputPdf):
        ocrmypdf.ocr(
            "./in/" + inputPdf,
            "./in/OCR/" + inputPdf,
            language=["hin", "eng"],
        )
    else:
        if os.path.isfile("./out/"+inputPdf.split('.')[0]+'.docx'):
            return "./out/" + inputPdf.split('.')[0]+".docx"
    reader = PdfReader("./in/OCR/" + inputPdf)
    f = docx.Document()
    f.styles["Normal"].font.name = "Arial"
    paragraph_format = f.styles['Normal'].paragraph_format
    paragraph_format.line_spacing = 1
    print(len(reader.pages))
    section = f.sections[0]
    set_number_of_columns(section, 2)
    for page in reader.pages:
        count += 1
        text = page.extract_text()
        out =  str(count) + ") " + text.rstrip()
        print(out)
        f.add_paragraph(out)
    filename =inputPdf.split(".")[0]
    f.save("./out/" + filename + ".docx")
    convert_docx_to_pdf("./out/"+filename+".docx","./pdf/"+filename+".pdf")
    return "./out/pdf/" + filename+".pdf"
