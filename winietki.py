import csv
from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from typing import List, Tuple

# Stałe
CSV_FILE = Path(r"C:\Users\ameli\Documents\Inventor Interoperability\Github\Samorzad_Winietki\winietki.csv")
BACKGROUND_PDF = Path(r"C:\Users\ameli\Documents\Inventor Interoperability\Github\Samorzad_Winietki\template.pdf")
FONT_PATH = Path(r"C:\Users\ameli\Documents\Inventor Interoperability\Github\Samorzad_Winietki\tan-pearl.ttf")
OUTPUT_FOLDER = Path(r"C:\Users\ameli\Documents\Inventor Interoperability\Github\Samorzad_Winietki")

GOLD_COLOR = CMYKColor(0.05, 0.00, 0.48, 0.00)
PDF_WIDTH, PDF_HEIGHT = 96 * 2.83465, 106 * 2.83465  # Konwersja mm na punkty
FONT_SIZE = 15
FONT_NAME = "TanPearl"


def setup_font() -> None:
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def create_pdf(name: str, surname: str, output_path: Path) -> None:
    temp_pdf = output_path.with_name(f'temp_{output_path.stem}.pdf')

    c = canvas.Canvas(str(temp_pdf), pagesize=(PDF_WIDTH, PDF_HEIGHT))
    c.setFont(FONT_NAME, FONT_SIZE)
    c.setFillColor(GOLD_COLOR)

    text = f"{name} {surname}"
    text_width = c.stringWidth(text, FONT_NAME, FONT_SIZE)
    x = (PDF_WIDTH - text_width) / 2
    y = (PDF_HEIGHT / 4) + 7

    c.drawString(x, y, text)
    c.save()

    return temp_pdf


def merge_pdfs(background: Path, content: Path, output: Path) -> None:
    with open(background, "rb") as bg_file, open(content, "rb") as content_file, open(output, "wb") as output_file:
        background_reader = PdfReader(bg_file)
        content_reader = PdfReader(content_file)

        output_writer = PdfWriter()
        background_page = background_reader.pages[0]
        content_page = content_reader.pages[0]
        background_page.merge_page(content_page)
        output_writer.add_page(background_page)
        output_writer.write(output_file)


def process_csv(csv_file: Path) -> List[Tuple[str, str]]:
    data = []
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Pomijamy nagłówek
            for row in reader:
                if len(row) >= 2:
                    name, surname = row[0].strip(), row[1].strip()
                    if name and surname:
                        data.append((name, surname))
                    else:
                        print(f"Pominięto niepełne dane: {row}")
    except FileNotFoundError:
        print(f"Nie znaleziono pliku CSV: {csv_file}")
    except Exception as e:
        print(f"Wystąpił błąd podczas odczytu pliku CSV: {e}")
    return data


def main():
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    setup_font()

    for i, (name, surname) in enumerate(process_csv(CSV_FILE), start=1):
        output_pdf = OUTPUT_FOLDER / f'winietka_{i}_{name}_{surname}.pdf'
        try:
            temp_pdf = create_pdf(name, surname, output_pdf)
            merge_pdfs(BACKGROUND_PDF, temp_pdf, output_pdf)
            temp_pdf.unlink()  # Usuwamy tymczasowy plik
            print(f"Wygenerowano: {output_pdf}")
        except Exception as e:
            print(f"Błąd przy generowaniu winietki dla {name} {surname}: {e}")

    print("Wszystkie pliki zostały wygenerowane!")


if __name__ == "__main__":
    main()
