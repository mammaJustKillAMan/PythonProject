#a program to work on pdf in the way that is useful to me - cutting pages to separate pdfs,
#adding pages to a pdf, shuffling pdf files

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


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

    print(f"Decrypted PDF saved to {output_pdf}")

#function to reorder pages of pdf
#after sunning it turns out it also works as a cutter :)
def reorder_pages(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    new_order = input("Enter new order of pages: ")
    #the input has to be split and the countdown starts from 0 in python
    new_order = [int(x)-1 for x in new_order.split(", ")]

    for i in new_order:
        writer.add_page(reader.pages[i])

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"Reordered PDF saved to {output_pdf}")

#function to add pages at the end of the file,
#later on one may use the previous function to sort it :P
def add_pages(input_pdf, extra_pdf, output_pdf):
    main_reader = PdfReader(input_pdf)
    extra_reader = PdfReader(extra_pdf)
    writer = PdfWriter()
    #pages from the original file
    for page in main_reader.pages:
        writer.add_page(page)

    #pages
    for page in extra_reader.pages:
        writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"Added pages to {output_pdf}")

if __name__ == "__main__":
    print("PDF Tool Menu:")
    print("1. Decrypt PDF")
    print("2. Reorder PDF pages")
    print("3. Add pages from another PDF")

    choice = input("Enter your choice (1/2/3): ")

    input_pdf = "MITLockGuide.pdf"
    extra_pdf = "chicken.pdf"
    output_pdf = "output.pdf"

    if choice == "1":
        decryption(input_pdf, output_pdf)
    elif choice == "2":
        reorder_pages(input_pdf, output_pdf)
    elif choice == "3":
        add_pages(input_pdf, extra_pdf, output_pdf)
    else:
        print("Invalid choice.")