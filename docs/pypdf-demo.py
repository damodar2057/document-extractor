from pypdf import PdfReader


# Creating a pdf reader object
reader = PdfReader('../rate-confirmation-docs/Bill May 20 TX to Florida LJ Freight .pdf')

# Printing number of pages in pdf file
print(reader.pages)

# Getting a specific page from the pdf file
page = reader.pages[0]

# Extracting text from the page
text = page.extract_text()
print(text)