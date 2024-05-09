from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np

from src import Pipeline

app = FastAPI()


@app.get("/healthcheck/")
async def health_check():
    return {"status": "ok"}


@app.post("/upload/")
async def upload_image(image: UploadFile = File(...)):
    # Read the uploaded image
    contents = await image.read()

    # Open the image using PIL
    pil_img = Image.open(io.BytesIO(contents))
    open_cv_image = np.array(pil_img)
    pil_img.close()

    # Return the size as JSON
    return JSONResponse(content=Pipeline()(open_cv_image))
