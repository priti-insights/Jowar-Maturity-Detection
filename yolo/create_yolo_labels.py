
from pathlib import Path
import cv2
import csv

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

IMAGES_DIR = PROJECT_ROOT / "dataset" / "raw" / "data" / "data" / "sorghum" / "images"
MASKS_DIR = PROJECT_ROOT / "dataset" / "raw" / "data" / "data" / "sorghum" / "masks"

OUTPUT_DIR = PROJECT_ROOT / "yolo" / "yolo_dataset"
LABELS_DIR = OUTPUT_DIR / "labels_all"

LABELS_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

image_files = sorted(
    p for p in IMAGES_DIR.iterdir()
    if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
)

created = 0
empty_masks = []
missing_masks = []
errors = []

for index, image_path in enumerate(image_files, start=1):
    mask_path = MASKS_DIR / (image_path.stem + ".png")
    label_path = LABELS_DIR / (image_path.stem + ".txt")

    if not mask_path.exists():
        missing_masks.append(image_path.name)
        continue

    image = cv2.imread(str(image_path))
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)

    if image is None or mask is None:
        errors.append(image_path.name)
        continue

    image_height, image_width = image.shape[:2]

    if mask.shape[:2] != (image_height, image_width):
        errors.append(image_path.name + " - dimensions mismatch")
        continue

    # Treat every non-zero mask pixel as foreground
    _, binary_mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)

    points = cv2.findNonZero(binary_mask)

    if points is None:
        empty_masks.append(image_path.name)
        continue

    # Overall bounding box of the mask foreground
    x, y, width, height = cv2.boundingRect(points)

    # Convert to YOLO normalized centre coordinates
    x_center = (x + width / 2) / image_width
    y_center = (y + height / 2) / image_height
    norm_width = width / image_width
    norm_height = height / image_height

    # Class 0 = panicle
    with open(label_path, "w", encoding="utf-8") as file:
        file.write(
            f"0 {x_center:.6f} {y_center:.6f} "
            f"{norm_width:.6f} {norm_height:.6f}\n"
        )

    created += 1

    if index % 100 == 0:
        print(f"Processed {index}/{len(image_files)} images")

# Save a summary report
report_path = OUTPUT_DIR / "label_generation_report.csv"

with open(report_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["category", "filename"])
    writer.writerows(["empty_mask", name] for name in empty_masks)
    writer.writerows(["missing_mask", name] for name in missing_masks)
    writer.writerows(["error", name] for name in errors)

print("\n========== LABEL GENERATION SUMMARY ==========")
print(f"Images found: {len(image_files)}")
print(f"Labels created: {created}")
print(f"Empty masks: {len(empty_masks)}")
print(f"Missing masks: {len(missing_masks)}")
print(f"Errors: {len(errors)}")
print(f"Labels folder: {LABELS_DIR}")
print(f"Report: {report_path}")
print("\nOriginal images and masks were not modified.")
