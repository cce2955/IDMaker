import fitz  # PyMuPDF

def pdf_to_png(pdf_path, png_path):
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = f"{png_path}_{page_num + 1}.png"
        pix.save(image_path)

if __name__ == "__main__":
    pdf_file_path = "./cards.pdf"
    png_file_path = "./image.png"

    pdf_to_png(pdf_file_path, png_file_path)
