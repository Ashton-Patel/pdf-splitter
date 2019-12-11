from tkinter import filedialog, messagebox
from tkinter import *
from tkinter.simpledialog import askstring
import PyPDF2
import os

pg_count = 0
tuplelist = []
passes = 1

root = Tk()
root.withdraw()

# Request user input - File Select
root.filename = filedialog.askopenfilename(
    initialdir="/Downloads",
    title="Select file",
    filetypes=(("PDF to split", "*.pdf"), ("all files", "*.*")),
)

# Request User Input - Page Range Entry
userinput = askstring("Page Ranges", "Enter desired pages ex: 1-2,3-40,41-45")

filepath = root.filename

for i in userinput.split(","):
    tuplelist.append(tuple(map(int, i.split("-"))))

for page in range(len(tuplelist)):
    pdf_writer = PyPDF2.PdfFileWriter()
    pdfReader = PyPDF2.PdfFileReader(filepath)
    start = tuplelist[page][0]
    end = tuplelist[page][1]
    while start <= end:
        pdf_writer.addPage(pdfReader.getPage(start - 1))
        start += 1
    output_filename = "{}__{}.pdf".format(filepath.split("/")[-1].split(".")[0], passes)
    with open(output_filename, "wb") as out:
        pdf_writer.write(out)
    pg_count = pg_count + PyPDF2.PdfFileReader(output_filename).getNumPages()
    passes = passes + 1

orig_count = PyPDF2.PdfFileReader(filepath).getNumPages()

msg = str(pg_count) + "/" + str(orig_count) + " Pages Extracted"
messagebox.showinfo("Information", msg)
