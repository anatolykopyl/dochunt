import pytesseract
from PIL import Image
import io
import requests

def detect(url):
    response = requests.get(url)
    try:
        img = Image.open(io.BytesIO(response.content))
    except OSError:
        return ''

    return pytesseract.image_to_string(img, lang='rus', timeout=30).lower()
