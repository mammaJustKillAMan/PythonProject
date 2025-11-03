#this file is for fuuuun
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


#function to count pages
def count_pages(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    return len(pdf_reader.pages)

#function to extract text and save it as txt
def extract_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    #words = text.split() #do i need it? NOPE the program recommended
    with open("text.txt", "w", encoding="utf-8") as text_file: #unicoode transformation format -8bit, thanks to that we can arrange not only english, chinese is ok too
        text_file.write(text)

    print("Text extracted and saved to text.txt")

#counting images
def count_images(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    count = 0
    for page in pdf_reader.pages:
        if "\XObject" in page["\Resources"]:
            xobject = page["\Resources"["\XObject"]]
            for obj in xobject:
                if xobject[obj]["/Type"] == "/Image":
                    count += 1
    print("Image count is {}".format(count))
    return count

#counting how many certain words are in the pdf
def count_words(pdf_path, word):
    pdf_reader = PdfReader(pdf_path)
    count = 0
    for page in pdf_reader.pages:
        text = page.extract_text() or ""
        count += text.lower().count(word.lower())
    print(f"The word '{word}' appears {count} times in the PDF.")
    return count

#function to add text within the pdf in certain place with default
def add_text(pdf_path, output_path, phrase, page_number=0, x=50, y=50):
    pdf_reader = PdfReader(pdf_path)

    packet = BytesIO() #temporary in-memory file
    can = canvas.Canvas(packet, pagesize=A4) #blanck page
    can.drawPage(x, y, phrase) #write on page
    can.save() #save it!!!!, no fire

    packet.seek(0)
    new = PdfReader(packet)
    new_page = new.pages[0]

    writer = PdfWriter()

    for i, page in enumerate(pdf_reader.pages):
        if i == page_number:
            page.merge_page(new_page)
        writer.add_page(page)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    print(f"Text added to PDF and saved to {output_path}")

#here was supposed to be a main with menu but i have no more strength rn, still ill
if __name__ == "__main__":
    print("___PDF FUNCTIONS MENU___")
    print("Please, choose carefully, for wrongful usage the programmer does not take credit")
    print("1. Count pages")
    print("2. Extract text")
    print("3. Count images")
    print("4. Count words")
    print("5. Add text")
    print("6. Exit")

    answer = input("Enter your choice: ")
    if answer == "6":
        exit()

    pdf_path = input("Enter path to PDF: ")
    output_path = input("Enter path to output PDF: ")
    if answer == "1":
        print("Page count:", count_pages(pdf_path))
    elif answer == "2":
        extract_text(pdf_path)
    elif answer == "3":
        count_images(pdf_path)
    elif answer == "4":
        word = input("Enter word to count: ")
        count_words(pdf_path, word)
    elif answer == "5":
        phrase = input("Enter phrase to add: ")
        add_text(pdf_path, output_path, phrase)
    else:
        print("Invalid choice.")
