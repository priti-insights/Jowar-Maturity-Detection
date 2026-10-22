
from pathlib import Path
import torch
from ultralytics import YOLO

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_YAML = (
    PROJECT_ROOT / "yolo" / "yolo_dataset"
    / "dataset" / "data.yaml"
)

RUNS_DIR = PROJECT_ROOT / "yolo" / "runs" / "detect"

print("========== YOLOv8 TRAINING ==========")
print("Dataset configuration:", DATA_YAML)
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("Training device: CPU")
print("Image size: 416")
print("Batch size: 2")
print("Epochs: 30")

if not DATA_YAML.exists():
    raise FileNotFoundError(
        f"Dataset configuration not found: {DATA_YAML}"
    )

# Load pretrained YOLOv8 Nano model
# Internet may be needed to download the weights first time.
model = YOLO("yolov8n.pt")

# Train the panicle detector
results = model.train(
    data=str(DATA_YAML),
    epochs=30,
    imgsz=416,
    batch=2,
    device="cpu",
    workers=0,
    cache=False,
    patience=8,
    project=str(RUNS_DIR),
    name="jowar_yolov8n",
    exist_ok=False,
    plots=True,
    verbose=True
)

print("\n========== TRAINING FINISHED ==========")
print("Training results saved under:", RUNS_DIR)
print("Check the run folder for weights/best.pt")
