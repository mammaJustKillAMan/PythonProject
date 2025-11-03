#a program to work on pdf in the way that is useful to me - cutting pages to separate pdfs,
#adding pages to a pdf, shuffling pdf files

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

#could be and pdf file
input_pdf = "MITLockGuide.pdf"
extra_pdf = "chicken.pdf"
output_pdf = "PDF_decrypted.pdf"

#the reader and writer wil go inside methods bc there might be an instance one uses different files withing the same run
#reader = PdfReader()
#writer = PdfWriter()

#function to decrypt and save the decrypted version of the file for future work
def decryption(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    if reader.is_encrypted:
        password = input("Enter your password: ")
        try:
            if reader.decrypt(password) == 0:
                print("Your password is incorrect")
                return
        except PdfReadError:
            ("Unable to decrypt PDF with provided password.")
            return

        for page in reader.pages:
                writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print("Decrypted PDF saved to " + output_pdf)

#function to reorder pages of pdf
def reorder_pages():
    filename = PdfReader(input_pdf)
    new_order = input("Enter new order of pages: ")
    #the input has to be split and the countdown starts from 0 in python
    new_order = [int(x)-1 for x in new_order.split(", ")]

    for i in new_order:
        writer.add_page(filename.pages[i])

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

#function to add pages at the end of the file,
#later on one may use the previous function to sort it :P
def add_pages():
    filename = input_pdf
    extra = extra_pdf
    #pages from the original file
    for page in filename:
        writer.add_page(page)

    #pages
    for page in extra:
        writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)