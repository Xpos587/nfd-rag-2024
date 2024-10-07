import os
import subprocess

import pymupdf4llm
import pypandoc


def convert_to_markdown(file_path):
    # Определяем расширение файла
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    # Функция для конвертации DOC, DOCX и RTF в PDF
    def office_to_pdf(file_path):
        output_dir = os.path.dirname(file_path)
        pdf_file = os.path.join(
            output_dir, os.path.basename(file_path).replace(ext, ".pdf")
        )
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                file_path,
                "--outdir",
                output_dir,
            ],
            capture_output=True,
            text=True,
        )
        return pdf_file

    # Конвертация в Markdown в зависимости от типа файла
    if ext in [".doc", ".docx", ".rtf"]:
        pdf_file = office_to_pdf(file_path)
        return pymupdf4llm.to_markdown(pdf_file)
    elif ext == ".pdf":
        return pymupdf4llm.to_markdown(file_path)
    elif ext == ".html":
        return pypandoc.convert_file(file_path, "md", format="html")
    elif ext in [".xls", ".xlsx"]:
        # Конвертируем Excel в CSV с помощью LibreOffice, затем в Markdown
        csv_file = os.path.join(
            os.path.dirname(file_path),
            os.path.basename(file_path).replace(ext, ".csv"),
        )
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "csv",
                file_path,
                "--outdir",
                os.path.dirname(file_path),
            ],
            capture_output=True,
            text=True,
        )
        return pypandoc.convert_file(csv_file, "md", format="csv")
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
