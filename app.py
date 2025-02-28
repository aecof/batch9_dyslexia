import requests
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dyslexia import preprocessing
from dyslexia.io import load_image
from dyslexia.ocr import extract_text_from_image


app = FastAPI(title="OCR API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def text_from_array(image_orig):
    image_no_shadow = preprocessing.remove_shadow(image_orig)
    image_gray = preprocessing.image_to_gray(image_no_shadow, threshold=True)
    image_gray = image_gray.max() - image_gray

    text = extract_text_from_image(image_gray)

    return text


@app.post("/ocr_file/")
async def ocr_file(file: UploadFile = File(...)):
    image_orig = load_image(file.file)
    text = text_from_array(image_orig)
    return {"text": text}


@app.post("/ocr_url/")
async def ocr_url(url: str):
    req = requests.get(url)

    file = io.BytesIO(req.content)

    image_orig = load_image(file)

    file.close()

    text = text_from_array(image_orig)

    return {"text": text}
