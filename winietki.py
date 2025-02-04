import csv
from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyPDF2 import PdfReader, PdfWriter
import os

# Ścieżki do plików
csv_file = r"C:\Users\ameli\Desktop\winietki\winietki.csv"                        # Tu wpisać swoje scieżki
background_pdf = r"C:\Users\ameli\Desktop\winietki\template.pdf"
font_path = r"C:\Users\ameli\Desktop\winietki\tan-pearl.ttf"
output_folder = r"C:\Users\ameli\Desktop\winietki"

# Rejestracja czcionki
pdfmetrics.registerFont(TTFont('TanPearl', font_path))

# Kolor tekstu
gold_color = CMYKColor(0.05, 0.00, 0.48, 0.00)          # Tu wpisać kolor tekstu

# Wymiary PDF w mm
x = 96                                                                             # Tu wpisać wymiary w mm
y = 106

# Zamiana jednostek
pdf_width = x * 2.83465
pdf_height = y * 2.83465

# Ustawienia tekstu
font_size = 15                                                                      # Tu wpisz rozmiar tekstu
font = "TanPearl"                                                                   # Tu wpisz nazwę czcionki

# Tworzymy folder na pliki PDF
os.makedirs(output_folder, exist_ok=True)

# Otwórz plik CSV i generuj PDF dla każdej osoby
with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader, None)  # Pomijamy nagłówek

    for i, row in enumerate(reader):
        try:
            imie = row[0].strip().replace(" ", "")
            nazwisko = row[1].strip().replace(" ", "")

            if not imie or not nazwisko:
                print(f"Pominięto pustą wartość w wierszu {i + 1}")
                continue

            pdf_file = os.path.join(output_folder, f'winietka_{i + 1}_{imie}_{nazwisko}.pdf')
            temp_pdf = os.path.join(output_folder, f'temp_{i + 1}.pdf')

            c = canvas.Canvas(temp_pdf, pagesize=(pdf_width, pdf_height))

            # Ustawienia czcionki i koloru
            c.setFont(font, font_size)
            c.setFillColor(gold_color)

            # Tekst do wyśrodkowania
            text = f"{imie} {nazwisko}"
            text_width = c.stringWidth(text, font, font_size)
            x = (pdf_width - text_width) / 2
            y = (pdf_height / 4) + 7

            # Dodanie tekstu do PDF
            c.drawString(x, y, text)
            c.save()

            # Połączenie tła i tekstu
            background_reader = PdfReader(background_pdf)
            temp_reader = PdfReader(temp_pdf)

            output_pdf = PdfWriter()
            background_page = background_reader.pages[0]
            temp_page = temp_reader.pages[0]
            background_page.merge_page(temp_page)
            output_pdf.add_page(background_page)

            with open(pdf_file, "wb") as outputStream:
                output_pdf.write(outputStream)

            os.remove(temp_pdf)

            print(f"Wygenerowano: {pdf_file}")
        except Exception as e:
            print(f"Błąd przy wierszu {i + 1}: {e}")

print(" Wszystkie pliki zostały wygenerowane!")