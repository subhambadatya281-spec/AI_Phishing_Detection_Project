import easyocr
import os

# OCR Model Load
reader = easyocr.Reader(
    ['en'],
    gpu=False
)

def detect_text_from_image(image_path):

    try:

        if not os.path.exists(image_path):
            return ""

        result = reader.readtext(image_path)

        extracted_text = ""

        for item in result:

            extracted_text += item[1] + " "

        return extracted_text.lower()

    except Exception as e:

        print("OCR ERROR:", e)

        return ""


# Testing
if __name__ == "__main__":

    text = detect_text_from_image(
        "static/website.png"
    )

    print("\nDetected Text:\n")
    print(text)