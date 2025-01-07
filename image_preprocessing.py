from PIL import Image, ImageOps, ImageFilter
import pytesseract
import csv
import os


def preprocess_and_extract_text(image_file):
    # Check if the image file exists
    if not os.path.exists(image_file):
        raise FileNotFoundError(
            f"The file '{image_file}' was not found. Please provide the correct file path.")

    # Load the image
    image = Image.open(image_file)

    # Convert to grayscale
    grayscale_image = ImageOps.grayscale(image)

    # Resize the image to improve resolution
    resized_image = grayscale_image.resize(
        (grayscale_image.width * 3, grayscale_image.height * 3))

    # Apply a Gaussian blur to reduce noise
    blurred_image = resized_image.filter(ImageFilter.GaussianBlur(radius=1))

    # Apply adaptive thresholding for better binarization
    binarized_image = blurred_image.point(lambda x: 0 if x < 150 else 255, '1')

    # Save the processed image
    processed_image_path = "processed_image_q3.png"
    binarized_image.save(processed_image_path)

    # Extract text using pytesseract with optimized configurations
    extracted_text = pytesseract.image_to_string(
        binarized_image, config="--psm 4 --oem 3")

    # Save the extracted text to a CSV file
    csv_filename = "extracted_text_q3.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Filename", "Extracted Text"])
        writer.writerow([image_file, extracted_text])

    print(f"Processed image saved as {processed_image_path}")
    print(f"Extracted text saved in {csv_filename}")
    return extracted_text


# Call the function with the updated image file path
preprocess_and_extract_text("q3.png")
