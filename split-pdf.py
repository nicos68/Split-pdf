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


def write_single_page(page, pdf, path, output_folder):
    pdf_writer = PdfWriter()
    pdf_writer.add_page(pdf.pages[page])

    output_path = output_folder / f"{path.name.replace('.pdf', '')}_page_{page+1}.pdf"

    write_pdf(output_path, pdf_writer)


def write_pdf(path, writer):
    with open(path, "wb") as out:
        writer.write(out)

    print("Created: {}".format(path.name))


def write_split_pages(page_index, pdf, path, output_folder):
    page = pdf.pages[page_index]
    dimensions = (page.mediabox.right / 2, page.mediabox.top)
    output_file_name_prefix = f"{path.name.replace('.pdf', '')}_page_"

    pdf_writer = PdfWriter()
    output_page = pdf_writer.add_blank_page(page.mediabox.width, page.mediabox.height)
    output_page.merge_page(page)
    output_page.mediabox.upper_right = dimensions
    output_page_index = page_index * 2 + 1
    output_path = output_folder / f"{output_file_name_prefix}{output_page_index}.pdf"

    write_pdf(output_path, pdf_writer)

    pdf_writer = PdfWriter()
    output_page = pdf_writer.add_blank_page(page.mediabox.width, page.mediabox.height)
    output_page.merge_page(page)
    output_page.mediabox.upper_left = dimensions
    output_page_index = (page_index + 1) * 2
    output_path = output_folder / f"{output_file_name_prefix}{output_page_index}.pdf"

    write_pdf(output_path, pdf_writer)


def split_pdf(path, split_pages):
    pdf = PdfReader(path)
    output_folder = path.parent.absolute() / "single_page_export"
    output_folder.mkdir(exist_ok=True)
    for page_index in range(len(pdf.pages)):
        if split_pages:
            write_split_pages(page_index, pdf, path, output_folder)
        else:
            write_single_page(page_index, pdf, path, output_folder)


def main():
    args = parser.parse_args()
    files = args.paths
    for one_file in files:
        split_pdf(one_file, True)


if __name__ == "__main__":
    main()
