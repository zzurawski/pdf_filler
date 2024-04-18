import os
import PyPDF2
from PyInquirer import prompt


def extract_field_names(pdf_path):
    field_names = []
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            try:
                #annotations = page['/Annots']
                for annotation in page['/Annots']:
                    field_name = annotation.get('/T')
                    if field_name:
                        field_names.append(field_name)
            except KeyError:
                pass
    return field_names

def fill_pdf(pdf_path, filled_pdf_path, field_data):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            for annotation in page['/Annots']:
                if '/T' in annotation:
                    field_name = annotation['/T'][1:-1]
                    if field_name in field_data:
                        if '/V' in annotation:
                            if '/Btn' in annotation['/FT']:
                                if '/Off' in annotation['/V']:
                                    continue
                                page.merge_page(PyPDF2.PdfReader(field_data[field_name]).pages[0])
                            continue
                    page.merge_page(PyPDF2.PdfReader(field_data[field_name]).pages[0])

            pdf_writer.add_page(page)

            with open(filled_pdf_path, 'wb') as filled_pdf_file:
                pdf_writer.write(filled_pdf_file)

        # Write the filled PDF to a new file
            with open(filled_pdf_path, 'wb') as filled_pdf_file:
                pdf_writer.write(filled_pdf_file)

def gather_pdf(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    questions = [
        {
            'type': 'list',
            'name': 'pdf_file',
            'message': 'Select the PDF file to fill:',
            'choices': pdf_files
        }
    ]
    answers = prompt(questions)
    pdf_path = os.path.join(directory, answers['pdf_file'])

    field_names = extract_field_names(pdf_path)
    field_data = {}
    for field_name in field_names:
        questions = [
            {
                'type': 'input',
                'name': field_name,
                'message': f'Enter value for {field_name}:'
            }
        ]
        answers = prompt(questions)
        field_data[field_name] = answers[field_name]

    return pdf_path, field_data


def main():
    directory = './pdfs'
    pdf_path, field_data = gather_pdf(directory)

    filled_pdf_path = os.path.splitext(pdf_path)[0] + '_filled.pdf'
    fill_pdf(pdf_path, filled_pdf_path, field_data)
    print(f'Filled PDF saved to: {filled_pdf_path}')

if __name__ == '__main__':
    main()

