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
        epilog="nique le capitalisme évidemment.",
        )

parser.add_argument(
        dest="paths",
        action="store",
        type=is_valid_pdf,
        nargs="*",
        metavar="FILE",
        help="Pass one or multiple file path, only pdf",
        )

parser.add_argument(
        "--crop",
        "-C",
        action="store_true",
        dest="crop_page",
        help="Flag to set a split in half of each page except first and last.",
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
        #TODO: yield the path

def crop_single_page():
    pass

def main():
    args = parser.parse_args()
    files = args.paths
    crop_page = args.crop_page

    #TODO: add an index to remove the first and the last page from the crop
    for one_file in files:
        #TODO: get the yielded value to further treatment if appropriate flag is set on
        split_pdf(one_file)
        #TODO: move here the console print statement

if __name__ == "__main__":
    main()
