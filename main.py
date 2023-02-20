import PySimpleGUI as sg
import os

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger, PageObject

working_directory = os.getcwd()

layout = [
    [sg.Text("Select PDF file")],
    [sg.InputText(key="-FILE_PATH-"),
     sg.FileBrowse("Choose file", initial_folder=working_directory, file_types=[("PDF Files", "*.pdf")])],
    [sg.Button("Run"), sg.Exit("Exit")]
]

window = sg.Window("PDF Splitter", layout)


def pdf_splitter(path):
    try:
        fname = os.path.splitext(os.path.basename(path))[0]
        doc_name = path.split('/')[-1].lower().split('.pdf')[0]
        print(doc_name)
        pdf = PdfFileReader(path)
        input_paths = []
        pdf_pages_number = pdf.getNumPages()

        for page in range(pdf_pages_number):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))

            output_filename = '{}_{}.pdf'.format(doc_name, page + 1)
            input_paths.append(output_filename)
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)

            print('Created: {}'.format(output_filename))
    except Exception as ex:
        print("An error occurred while processing the PDF\r\nError: " + str(ex), "Error")


while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == "Run":
        pdf_address = values["-FILE_PATH-"]
        if not ".pdf" in pdf_address.lower():
            pdf_address += ".pdf"
        pdf_splitter(pdf_address)

window.close()
