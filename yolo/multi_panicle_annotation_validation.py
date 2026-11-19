from pathlib import Path
import csv
import cv2
import numpy as np
import random

ROOT = Path(__file__).resolve().parent.parent

IMAGES_DIR = (
    ROOT / "dataset" / "raw" / "data" / "data" / "sorghum" / "images"
)

MASKS_DIR = (
    ROOT / "dataset" / "raw" / "data" / "data" / "sorghum" / "masks"
)

OUT_DIR = ROOT / "yolo" / "multi_panicle_review"
PREVIEW_DIR = OUT_DIR / "previews"
PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
PREVIEW_COUNT = 40
RANDOM_SEED = 42

def get_files(folder):
    return {p.stem: p for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in EXTS}

def main():
    print("Images folder exists:", IMAGES_DIR.is_dir(), IMAGES_DIR)
    print("Masks folder exists:", MASKS_DIR.is_dir(), MASKS_DIR)
    if not IMAGES_DIR.is_dir() or not MASKS_DIR.is_dir():
        print("Check the paths at the top of this script.")
        return

    images = get_files(IMAGES_DIR)
    masks = get_files(MASKS_DIR)
    image_names, mask_names = set(images), set(masks)
    matched = sorted(image_names & mask_names)

    print("\\n========== DATASET SUMMARY ==========")
    print("Images:", len(images))
    print("Masks:", len(masks))
    print("Matched pairs:", len(matched))
    print("Images without masks:", len(image_names - mask_names))
    print("Masks without images:", len(mask_names - image_names))

    rng = random.Random(RANDOM_SEED)
    sample = matched.copy()
    rng.shuffle(sample)
    sample = sample[:min(PREVIEW_COUNT, len(sample))]
    rows = []

    for i, name in enumerate(sample, 1):
        image = cv2.imread(str(images[name]), cv2.IMREAD_COLOR)
        mask = cv2.imread(str(masks[name]), cv2.IMREAD_GRAYSCALE)
        if image is None or mask is None:
            print("Read error:", name)
            continue

        ih, iw = image.shape[:2]
        mh, mw = mask.shape[:2]
        binary = np.uint8(mask > 0)
        component_count, labels, stats, centroids = cv2.connectedComponentsWithStats(
            binary, connectivity=8
        )
        areas = stats[1:, cv2.CC_STAT_AREA] if component_count > 1 else np.array([])
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        overlay = image.copy()
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 8)

        target_w = 640
        target_h = int(ih * target_w / iw)
        img_small = cv2.resize(image, (target_w, target_h))
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask_small = cv2.resize(mask_bgr, (target_w, target_h), interpolation=cv2.INTER_NEAREST)
        overlay_small = cv2.resize(overlay, (target_w, target_h))
        panel = np.hstack([img_small, mask_small, overlay_small])
        preview = PREVIEW_DIR / f"{name}_review.jpg"
        cv2.imwrite(str(preview), panel, [cv2.IMWRITE_JPEG_QUALITY, 92])

        rows.append({
            "filename": name,
            "image_width": iw, "image_height": ih,
            "mask_width": mw, "mask_height": mh,
            "dimensions_match": iw == mw and ih == mh,
            "foreground_pixels": int(binary.sum()),
            "connected_components_8": max(0, component_count - 1),
            "external_contours": len(contours),
            "largest_component_area": int(areas.max()) if len(areas) else 0,
            "candidate_boxes_from_mask": len(contours),
            "preview_file": str(preview)
        })
        print(f"[{i}/{len(sample)}] {name}: components={max(0, component_count-1)}, "
              f"contours={len(contours)}, dimensions_match={iw == mw and ih == mh}")

    report = OUT_DIR / "mask_review_report.csv"
    if rows:
        with report.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print("\\nReport:", report)
    print("Previews:", PREVIEW_DIR)
    print("Review whether each mask covers every panicle intended for detection.")
    print("A connected component does not prove it represents one panicle.")
    print("This script does not create training labels or modify original files.")

if __name__ == "__main__":
    main()
