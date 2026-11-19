"""
Create contact sheets from already-extracted jowar panicle crops.

Reads:
  classification/panicle_crops/train
  classification/panicle_crops/val
  classification/panicle_crops/test

Writes:
  classification/contact_sheets/train
  classification/contact_sheets/val
  classification/contact_sheets/test
  classification/contact_sheets/contact_sheet_manifest.csv

Each sheet contains 20 crops. Original crops and crop_metadata.csv are not modified.
"""

from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import csv

PROJECT_ROOT = Path(__file__).resolve().parent
CROP_ROOT = PROJECT_ROOT / "classification" / "panicle_crops"
OUTPUT_ROOT = PROJECT_ROOT / "classification" / "contact_sheets"
METADATA_CSV = PROJECT_ROOT / "classification" / "crop_metadata.csv"

SPLITS = ("train", "val", "test")
BATCH_SIZE = 20
COLUMNS = 4
ROWS = 5
CELL_W, CELL_H = 370, 345
THUMB_W, THUMB_H = 340, 285
MARGIN = 20
HEADER_H = 75
EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def get_font(size, bold=False):
    candidates = (
        ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf"]
        if bold else
        ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"]
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    try:
        return ImageFont.truetype(
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size
        )
    except OSError:
        return ImageFont.load_default()


def load_metadata():
    """Map crop filename and split to original image metadata, if available."""
    metadata = {}
    if not METADATA_CSV.exists():
        print(f"Note: metadata CSV not found: {METADATA_CSV}")
        return metadata

    with METADATA_CSV.open("r", newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            key = (row.get("split", ""), Path(row.get("image", "")).name)
            metadata[key] = row
    return metadata


def make_sheet(items, split, batch_no, total, first_global_id):
    width = MARGIN * 2 + COLUMNS * CELL_W
    height = HEADER_H + MARGIN + ROWS * CELL_H + MARGIN
    sheet = Image.new("RGB", (width, height), (245, 247, 246))
    draw = ImageDraw.Draw(sheet)

    title_font = get_font(26, True)
    info_font = get_font(15)
    name_font = get_font(13, True)
    id_font = get_font(13)

    draw.text((MARGIN, 16), f"Jowar Panicle Crops - {split.upper()} - Batch {batch_no:03d}",
              fill=(30, 40, 36), font=title_font)
    draw.text((MARGIN, 51), f"{len(items)} crops | Split total: {total}",
              fill=(90, 105, 98), font=info_font)

    for offset, image_path in enumerate(items):
        row, col = divmod(offset, COLUMNS)
        x = MARGIN + col * CELL_W
        y = HEADER_H + row * CELL_H
        draw.rounded_rectangle(
            (x, y, x + CELL_W - 10, y + CELL_H - 10),
            radius=9, fill=(255, 255, 255), outline=(215, 222, 218), width=2
        )

        crop_id = first_global_id + offset
        try:
            with Image.open(image_path) as im:
                thumb = ImageOps.exif_transpose(im).convert("RGB")
                thumb.thumbnail((THUMB_W, THUMB_H), Image.Resampling.LANCZOS)
            px = x + (CELL_W - 10 - thumb.width) // 2
            py = y + 8 + (THUMB_H - thumb.height) // 2
            sheet.paste(thumb, (px, py))
        except Exception as exc:
            draw.text((x + 12, y + 130), f"Image read error: {exc}"[:42],
                      fill=(170, 30, 30), font=name_font)

        filename = image_path.name
        if len(filename) > 37:
            filename = filename[:34] + "..."
        label_y = y + 305
        draw.text((x + 12, label_y), f"ID {crop_id:06d}",
                  fill=(25, 95, 70), font=id_font)
        draw.text((x + 110, label_y), filename,
                  fill=(30, 40, 36), font=name_font)

    return sheet


def main():
    if not CROP_ROOT.exists():
        raise FileNotFoundError(
            f"Panicle crop folder not found:\n{CROP_ROOT}\n"
            "Place this script in your project root."
        )

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    metadata = load_metadata()
    manifest_rows = []
    global_id = 1
    total_all = 0

    for split in SPLITS:
        split_dir = CROP_ROOT / split
        if not split_dir.exists():
            print(f"Skipping missing split folder: {split_dir}")
            continue

        images = sorted(
            p for p in split_dir.iterdir()
            if p.is_file() and p.suffix.lower() in EXTENSIONS
        )
        total_all += len(images)
        split_output = OUTPUT_ROOT / split
        split_output.mkdir(parents=True, exist_ok=True)

        # Remove old generated sheets in this split only.
        for old in split_output.glob("contact_sheet_*.jpg"):
            old.unlink()

        batches = [images[i:i + BATCH_SIZE] for i in range(0, len(images), BATCH_SIZE)]
        print(f"\n{split}: {len(images)} crops -> {len(batches)} contact sheets")

        for batch_no, start in enumerate(range(0, len(images), BATCH_SIZE), start=1):
            batch = images[start:start + BATCH_SIZE]
            sheet = make_sheet(batch, split, batch_no, len(images), global_id)
            sheet_name = f"contact_sheet_{batch_no:03d}.jpg"
            sheet.save(split_output / sheet_name, "JPEG", quality=94, optimize=True)

            for offset, crop_path in enumerate(batch):
                crop_id = global_id + offset
                meta = metadata.get((split, crop_path.name), {})
                manifest_rows.append({
                    "crop_id": f"{crop_id:06d}",
                    "split": split,
                    "crop_filename": crop_path.name,
                    "crop_path": str(crop_path.relative_to(PROJECT_ROOT)),
                    "original_image": meta.get("original_image", ""),
                    "maturity_label": meta.get("maturity_label", "unlabeled"),
                    "contact_sheet": str((split_output / sheet_name).relative_to(PROJECT_ROOT)),
                })

            print(f"  Created {split}/{sheet_name} ({len(batch)} crops)")
            global_id += len(batch)

    manifest_path = OUTPUT_ROOT / "contact_sheet_manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8-sig") as f:
        fields = [
            "crop_id", "split", "crop_filename", "crop_path",
            "original_image", "maturity_label", "contact_sheet"
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(manifest_rows)

    print("\nContact sheet generation complete.")
    print(f"Total panicle crops: {total_all}")
    print(f"Total contact sheets: {sum(1 for _ in OUTPUT_ROOT.rglob('contact_sheet_*.jpg'))}")
    print(f"Output folder: {OUTPUT_ROOT}")
    print(f"Manifest: {manifest_path}")
    print("\nUpload sheets in order, beginning with train/contact_sheet_001.jpg.")
    print("Do not mix train, val, and test sheets when sending labels for review.")


if __name__ == "__main__":
    main()
