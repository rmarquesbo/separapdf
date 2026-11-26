import pathlib
import pymupdf


class PdfError(Exception):
    """Business-rule error (invalid page, invalid file, invalid option...)."""


# ---------- Helpers ----------

def next_filename(folder=".", prefix="Document_"):
    folder = pathlib.Path(folder)
    n = 1
    while (folder / f"{prefix}{n:03d}.pdf").exists():
        n += 1
    return folder / f"{prefix}{n:03d}.pdf"


def check_page(doc, page, max_page=None):
    max_page = max_page or len(doc)
    if not 1 <= page <= max_page:
        raise PdfError(f"Invalid page {page}. Valid range: 1 to {max_page}.")


def open_pdf(path_text):
    path = pathlib.Path(path_text.strip().strip('"'))
    if not path.is_file():
        raise PdfError(f"File not found: {path}")
    try:
        doc = pymupdf.open(path)
    except Exception as error:
        raise PdfError(f"Could not open file: {path}") from error
    if not doc.is_pdf:
        raise PdfError(f"Not a PDF file: {path}")
    if doc.needs_pass:
        raise PdfError("Password-protected PDFs are not supported.")
    return doc


def ask_int(prompt):
    text = input(prompt)
    try:
        return int(text)
    except ValueError:
        raise PdfError(f"'{text}' is not a valid number.") from None


# ---------- Operations (receive a document, return PDF bytes) ----------

def merging_pdf(doc, other_doc):
    doc.insert_pdf(other_doc)
    return doc.tobytes()


def dividing_pdf(doc, init_page, end_page):
    check_page(doc, init_page)
    check_page(doc, end_page)
    if init_page > end_page:
        raise PdfError("Initial page must be less than or equal to end page.")
    split_file = pymupdf.open()
    split_file.insert_pdf(doc, from_page=init_page - 1, to_page=end_page - 1)
    return split_file.tobytes()


def compressing_file(doc):
    return doc.tobytes(garbage=3, use_objstms=True, deflate=True)


def rearranging_pages(doc, page, position):
    check_page(doc, page)
    check_page(doc, position)
    pages = list(range(len(doc)))
    moved = pages.pop(page - 1)
    pages.insert(position - 1, moved)
    doc.select(pages)
    return doc.tobytes()


def copying_pages(doc, page, position):
    check_page(doc, page)
    check_page(doc, position, max_page=len(doc) + 1)  # len + 1 = copy goes to the end
    pages = list(range(len(doc)))
    pages.insert(position - 1, page - 1)
    doc.select(pages)
    return doc.tobytes()


# ---------- Command-line interface ----------

MENU = ("\n---- *Functions* -----"
        "\n1 - Merging PDFs"
        "\n2 - Compressing PDFs"
        "\n3 - Dividing PDFs"
        "\n4 - Re-Arranging Pages"
        "\n5 - Copying Pages")


def main():
    try:
        doc = open_pdf(input("Enter pdf file path: "))
        print(MENU)
        option = ask_int("Enter function number: ")

        match option:
            case 1:
                other_doc = open_pdf(input("Enter second pdf file path: "))
                result = merging_pdf(doc, other_doc)
            case 2:
                result = compressing_file(doc)
            case 3:
                result = dividing_pdf(doc,
                                      ask_int("Enter initial page number: "),
                                      ask_int("Enter end page number: "))
            case 4:
                result = rearranging_pages(doc,
                                           ask_int("Enter page to move: "),
                                           ask_int("Enter new position: "))
            case 5:
                result = copying_pages(doc,
                                       ask_int("Enter page to copy: "),
                                       ask_int("Enter position of the copy: "))
            case _:
                raise PdfError("Invalid function number.")

        output = next_filename()
        output.write_bytes(result)
        print(f"Done! Saved as {output}")
    except PdfError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
