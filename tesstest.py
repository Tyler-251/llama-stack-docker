import pytesseract

# https://pypi.org/project/pytesseract/
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
print(pytesseract.image_to_data('./temp/screenshots/screenshot.png'))

