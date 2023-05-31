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
    description="Pass one or more pdfs and spit and export single pages",
    epilog="et nique le capitalisme bien évidemment.",
)


parser.add_argument(
    dest="paths",
    action="store",
    type=is_valid_pdf,
    nargs="*",
    metavar="FILE",
    help="Pass one or multiple file path, only pdf",
)


def write_single_page(page, pdf, output_path):
    pdf_writer = PdfWriter()
    pdf_writer.add_page(pdf.pages[page])

    write_pdf(output_path, pdf_writer)


def write_pdf(path, writer):
    with open(path, "wb") as out:
        writer.write(out)

    print("Created: {}".format(path.name))


def generate_left_page(page, dimensions):
    pdf_writer = PdfWriter()
    output_page = pdf_writer.add_blank_page(page.mediabox.width, page.mediabox.height)
    output_page.merge_page(page)
    output_page.mediabox.upper_right = dimensions
    return pdf_writer


def generate_right_page(page, dimensions):
    pdf_writer = PdfWriter()
    output_page = pdf_writer.add_blank_page(page.mediabox.width, page.mediabox.height)
    output_page.merge_page(page)
    output_page.mediabox.upper_left = dimensions
    return pdf_writer

parser.add_argument(
        "--crop",
        "-C",
        action="store_true",
        dest="crop_page",
        help="Flag to set a split in half of each page except first and last.",
        )
        

def split_pdf(path):
    pdf = PdfReader(path)

    output_folder = path.parent.absolute() / "single_page_export"
    output_folder.mkdir(exist_ok=True)
    widths = {p.mediabox.width for p in pdf.pages}
    max_width = max(widths)
    output_file_count = 0
    for page_index in range(len(pdf.pages)):
        output_file_name_prefix = f"{path.name.replace('.pdf', '')}_page_"
        output_file_count = output_file_count + 1
        output_path = output_folder / f"{output_file_name_prefix}{output_file_count}.pdf"
        if len(widths) > 1 and pdf.pages[page_index].mediabox.width == max_width:
            page = pdf.pages[page_index]
            dimensions = (page.mediabox.right / 2, page.mediabox.top)

            writer = generate_left_page(page, dimensions)
            write_pdf(output_path, writer)

            output_file_count = output_file_count + 1
            output_path = output_folder / f"{output_file_name_prefix}{output_file_count}.pdf"
            writer = generate_right_page(page, dimensions)
            write_pdf(output_path, writer)

        else:
            write_single_page(page_index, pdf, output_path)



def main():
    args = parser.parse_args()
    files = args.paths
    crop_page = args.crop_page

    for one_file in files:
        split_pdf(one_file)

if __name__ == "__main__":
    main()
