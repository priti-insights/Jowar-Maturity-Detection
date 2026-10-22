
from pathlib import Path
import random
import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent

images_dir = (
    PROJECT_ROOT / "dataset" / "raw" / "data" / "data"
    / "sorghum" / "images"
)

masks_dir = (
    PROJECT_ROOT / "dataset" / "raw" / "data" / "data"
    / "sorghum" / "masks"
)

# Save previews inside the YOLO project folder
output_dir = Path(__file__).resolve().parent / "verification"
output_dir.mkdir(parents=True, exist_ok=True)

extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

images = {
    p.stem: p for p in images_dir.iterdir()
    if p.is_file() and p.suffix.lower() in extensions
}

masks = {
    p.stem: p for p in masks_dir.iterdir()
    if p.is_file() and p.suffix.lower() in extensions
}

matched = sorted(set(images) & set(masks))

if not matched:
    raise SystemExit("No matching image-mask pairs found.")

# Fixed seed makes the sample repeatable
random.seed(42)
sample_names = random.sample(matched, min(20, len(matched)))

print("Total matching pairs:", len(matched))
print("Masks selected for visual inspection:", len(sample_names))
print("Preview folder:", output_dir)

print("\n========== MASK REGION ANALYSIS ==========")

for name in sample_names:
    image = cv2.imread(str(images[name]), cv2.IMREAD_COLOR)
    mask = cv2.imread(str(masks[name]), cv2.IMREAD_GRAYSCALE)

    if image is None or mask is None:
        print("Could not read:", name)
        continue

    if image.shape[:2] != mask.shape[:2]:
        print("DIMENSION MISMATCH:", name)
        continue

    # Binary foreground: mask pixels greater than zero
    binary = np.uint8(mask > 0)

    # Connected components
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        binary, connectivity=8
    )

    # Exclude component 0, which is the background
    component_areas = stats[1:, cv2.CC_STAT_AREA]
    component_count = len(component_areas)

    # External contours for candidate detection boxes
    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Draw candidate bounding boxes on the original image
    preview = image.copy()
    valid_boxes = 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)

        # Display all contours in this diagnostic preview.
        # Do not apply a final filtering threshold yet.
        cv2.rectangle(
            preview, (x, y), (x + w, y + h), (0, 255, 0), 4
        )
        valid_boxes += 1

    print(f"\n{name}")
    print("  Connected foreground regions:", component_count)
    print("  External contours:", len(contours))
    print(
        "  Largest component areas:",
        sorted(component_areas.tolist(), reverse=True)[:10]
    )
    print("  Candidate boxes drawn:", valid_boxes)

    # Make a three-panel preview: image, mask, and candidate boxes
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    preview_rgb = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)

    # Resize only the previews for easier viewing; originals remain unchanged
    target_width = 900
    scale = target_width / image.shape[1]
    target_height = int(image.shape[0] * scale)

    image_small = cv2.resize(
        image_rgb, (target_width, target_height)
    )
    mask_small = cv2.resize(
        mask, (target_width, target_height),
        interpolation=cv2.INTER_NEAREST
    )
    preview_small = cv2.resize(
        preview_rgb, (target_width, target_height)
    )

    canvas = np.hstack([
        image_small,
        cv2.cvtColor(mask_small, cv2.COLOR_GRAY2RGB),
        preview_small
    ])

    output_path = output_dir / f"{name}_regions.jpg"

    # OpenCV expects BGR for writing
    cv2.imwrite(
        str(output_path),
        cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR),
        [cv2.IMWRITE_JPEG_QUALITY, 90]
    )

print("\nCompleted.")
print("Open the verification folder to review the generated previews.")
print("Original images and masks were not modified.")
