import os
import PyPDF2


def merge_pdfs(folder_path, output_filename):
    pdf_writer = PyPDF2.PdfMerger()

    # Pobranie listy plików PDF i posortowanie ich wg numeru
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

    for pdf in pdf_files:
        pdf_path = os.path.join(folder_path, pdf)
        pdf_writer.append(pdf_path)

    output_path = os.path.join(folder_path, output_filename)
    pdf_writer.write(output_path)
    pdf_writer.close()
    print(f"Połączono {len(pdf_files)} plików PDF w jeden: {output_path}")


if __name__ == "__main__":
    folder_path = os.path.dirname(os.path.abspath(__file__))  # Pobiera ścieżkę katalogu, gdzie znajduje się skrypt
    merge_pdfs(folder_path, "output.pdf")