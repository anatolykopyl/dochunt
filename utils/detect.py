import pytesseract
from PIL import Image
import io
import requests

def detect(url):
    response = requests.get(url)
    try:
        img = Image.open(io.BytesIO(response.content))
        string = pytesseract.image_to_string(img, lang='rus', timeout=30).lower()
    except OSError: # Happens when whatever we get is not an image and cant be opened as such
        string = ''
    
    return string
