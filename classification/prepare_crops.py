from pathlib import Path
from PIL import Image
import csv

# Project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Existing YOLO dataset
DATASET_DIR = PROJECT_DIR / "yolo" / "yolo_dataset" / "dataset"

# New classification dataset
OUTPUT_DIR = PROJECT_DIR / "classification" / "panicle_crops"

CSV_PATH = PROJECT_DIR / "classification" / "crop_metadata.csv"

SPLITS = ["train", "val", "test"]

records = []

for split in SPLITS:

    image_dir = DATASET_DIR / "images" / split
    label_dir = DATASET_DIR / "labels" / split

    output_split = OUTPUT_DIR / split
    output_split.mkdir(parents=True, exist_ok=True)

    for image_path in image_dir.glob("*.jpg"):

        label_path = label_dir / f"{image_path.stem}.txt"

        if not label_path.exists():
            continue

        with Image.open(image_path) as img:

            width, height = img.size

            lines = label_path.read_text().strip().splitlines()

            for index, line in enumerate(lines):

                values = line.split()

                if len(values) != 5:
                    continue

                class_id, xc, yc, bw, bh = map(float, values)

                # Convert normalized YOLO coordinates to pixels
                x1 = max(0, int((xc - bw / 2) * width))
                y1 = max(0, int((yc - bh / 2) * height))
                x2 = min(width, int((xc + bw / 2) * width))
                y2 = min(height, int((yc + bh / 2) * height))

                if x2 <= x1 or y2 <= y1:
                    continue

                crop = img.crop((x1, y1, x2, y2))

                crop_name = f"{image_path.stem}_panicle_{index}.jpg"

                crop_path = output_split / crop_name

                crop.save(crop_path, quality=95)

                records.append({
                    "image": str(crop_path.relative_to(PROJECT_DIR)),
                    "original_image": image_path.name,
                    "split": split,
                    "maturity_label": "unlabeled"
                })

                print(f"Saved: {crop_name}")

# Save metadata
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(CSV_PATH, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "image",
            "original_image",
            "split",
            "maturity_label"
        ]
    )

    writer.writeheader()
    writer.writerows(records)

print("\nPanicle cropping completed!")
print(f"Total panicle crops: {len(records)}")
print(f"Metadata saved at: {CSV_PATH}")