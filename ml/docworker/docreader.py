from docx import Document

def read_docx_in_paragraphs(file_path):
    doc = Document(file_path)
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return paragraphs

file_path = 'Проект договора.docx'
paragraphs = read_docx_in_paragraphs(file_path)

for i, paragraph in enumerate(paragraphs):
    print(f"Абзац {i + 1}: {paragraph}")
