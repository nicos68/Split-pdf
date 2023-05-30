import os
from pypdf import PdfReader, PdfWriter
import argparse
from pathlib import Path

def is_valid_pdf(filepath):
    if not Path(filepath).is_file():
        raise FileNotFoundError
    if Path(filepath).suffix != ".pdf":
        raise ValueError
    return Path(filepath)

parser = argparse.ArgumentParser(
        prog="PDFSplitter",
        usage="%(prog)s pdfToSplit",
        description="Pass one or plus pdf and spit an export of single pages",
        epilog="nique le capitalisme et évidemment.",
        )

parser.add_argument(
        dest="paths",
        action="store",
        type=is_valid_pdf,
        nargs="*",
        metavar="FILE",
        help="Pass one or multiple file path, only pdf",
        )


def split_pdf(path):
    pdf = PdfReader(path)
    for page in range(len(pdf.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page])
        
        output_folder = path.parent.absolute() / "single_page_export"
        output_folder.mkdir(exist_ok=True)
        output_path= output_folder / f"{path.name}_page_{page+1}.pdf"

        with open(output_path, 'wb') as out:
            pdf_writer.write(out)

        print(f'Created: {output_path.name}')

def main():
    args = parser.parse_args()
    files = args.paths
    for one_file in files:
        split_pdf(one_file)

if __name__ == "__main__":
    main()
