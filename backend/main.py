from .auth import router as auth_router
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from pathlib import Path
import cv2
import numpy as np

app = FastAPI(
    title="Jowar Maturity Detection API",
    description="API for jowar panicle detection and maturity assessment",
    version="1.0.0"
)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "yolo"
    / "runs"
    / "detect"
    / "jowar_yolov8n-2"
    / "weights"
    / "best.pt"
)
model = None

if MODEL_PATH.exists():
    model = YOLO(str(MODEL_PATH))


@app.get("/")
def home():
    return {
        "message": "Jowar Maturity Detection API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "running",
        "model_file_exists": MODEL_PATH.exists(),
        "inference_ready": model is not None
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Upload a JPG, PNG, or WEBP image."
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty."
        )

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image."
        )

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="YOLO model is not available."
        )

    try:
        results = model.predict(
            source=image,
            imgsz=416,
            conf=0.25,
            verbose=False
        )

        result = results[0]
        detections = []

        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                coordinates = box.xyxy[0].tolist()

                detections.append({
                    "class_id": class_id,
                    "class_name": result.names[class_id],
                    "confidence": round(confidence, 4),
                    "bounding_box": [
                        round(float(value), 2)
                        for value in coordinates
                    ]
                })

        return {
            "message": "YOLO prediction completed successfully.",
            "filename": file.filename,
            "image_width": int(image.shape[1]),
            "image_height": int(image.shape[0]),
            "panicle_count": len(detections),
            "detections": detections,
            "model": "YOLOv8n"
        }

    except Exception as error:
        print("YOLO inference error:", error)
        raise HTTPException(
            status_code=500,
            detail="An error occurred during YOLO inference."
        )
