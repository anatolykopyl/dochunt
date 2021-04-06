import pytesseract
from PIL import Image
import io
import requests

def detect(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    return pytesseract.image_to_string(img).lower()
