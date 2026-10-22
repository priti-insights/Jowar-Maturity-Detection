
from pathlib import Path
import random
import shutil

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

IMAGES_DIR = (
    PROJECT_ROOT / "dataset" / "raw" / "data" / "data"
    / "sorghum" / "images"
)

LABELS_DIR = PROJECT_ROOT / "yolo" / "yolo_dataset" / "labels_all"

OUTPUT_DIR = PROJECT_ROOT / "yolo" / "yolo_dataset" / "dataset"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Reproducible split
RANDOM_SEED = 42
TRAIN_RATIO = 0.80
VAL_RATIO = 0.10

# Find images that have corresponding generated labels
pairs = []

for label_path in LABELS_DIR.glob("*.txt"):
    matching_images = [
        image_path
        for image_path in IMAGES_DIR.glob("*")
        if image_path.is_file()
        and image_path.suffix.lower() in IMAGE_EXTENSIONS
        and image_path.stem == label_path.stem
    ]

    if len(matching_images) == 1:
        pairs.append((matching_images[0], label_path))
    elif len(matching_images) == 0:
        print(f"WARNING: No image found for {label_path.name}")
    else:
        print(f"WARNING: Multiple images found for {label_path.name}")

if not pairs:
    raise RuntimeError("No matching image-label pairs found.")

# Shuffle reproducibly
random.seed(RANDOM_SEED)
random.shuffle(pairs)

total = len(pairs)
train_count = int(total * TRAIN_RATIO)
val_count = int(total * VAL_RATIO)

train_pairs = pairs[:train_count]
val_pairs = pairs[train_count:train_count + val_count]
test_pairs = pairs[train_count + val_count:]

splits = {
    "train": train_pairs,
    "val": val_pairs,
    "test": test_pairs
}

# Prevent accidental mixing with an existing split
if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"\nOutput folder already contains files:\n{OUTPUT_DIR}\n"
        "To avoid overwriting data, rename or remove this generated "
        "dataset folder before running the script again."
    )

# Create directories and copy files
for split_name, split_pairs in splits.items():
    images_out = OUTPUT_DIR / "images" / split_name
    labels_out = OUTPUT_DIR / "labels" / split_name

    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    for image_path, label_path in split_pairs:
        shutil.copy2(image_path, images_out / image_path.name)
        shutil.copy2(label_path, labels_out / label_path.name)

    print(f"{split_name}: {len(split_pairs)} image-label pairs")

# Create YOLO configuration
yaml_path = OUTPUT_DIR / "data.yaml"

yaml_content = f"""path: {OUTPUT_DIR.as_posix()}
train: images/train
val: images/val
test: images/test

names:
  0: panicle
"""

yaml_path.write_text(yaml_content, encoding="utf-8")

print("\n========== DATASET SPLIT SUMMARY ==========")
print(f"Total pairs: {total}")
print(f"Training: {len(train_pairs)}")
print(f"Validation: {len(val_pairs)}")
print(f"Testing: {len(test_pairs)}")
print(f"Dataset folder: {OUTPUT_DIR}")
print(f"YOLO configuration: {yaml_path}")
print("\nOriginal images and labels were not modified.")
