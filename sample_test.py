from PIL import Image
import pytesseract
import csv


def extract_and_save_text(image_file):
    text = pytesseract.image_to_string(Image.open(image_file))
    csv_filename = "q3_extracted_text.csv"

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Filename", "Extracted Text"])
        writer.writerow([image_file, text])

    print(f"Extracted text from {image_file} has been saved to {csv_filename}")


image_file = "q3.png"
extract_and_save_text(image_file)
