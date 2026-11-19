
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent

images_dir = (
    PROJECT_ROOT / "dataset" / "raw" / "data" / "data"
    / "sorghum" / "images"
)

masks_dir = (
    PROJECT_ROOT / "dataset" / "raw" / "data" / "data"
    / "sorghum" / "masks"
)

extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

print("\n========== PATH CHECK ==========")
print("Images folder exists:", images_dir.is_dir())
print("Masks folder exists:", masks_dir.is_dir())

if not images_dir.is_dir() or not masks_dir.is_dir():
    raise SystemExit("ERROR: Check the folder paths.")

images = sorted(
    p for p in images_dir.iterdir()
    if p.is_file() and p.suffix.lower() in extensions
)

masks = sorted(
    p for p in masks_dir.iterdir()
    if p.is_file() and p.suffix.lower() in extensions
)

image_map = {p.stem: p for p in images}
mask_map = {p.stem: p for p in masks}

matched = sorted(set(image_map) & set(mask_map))
images_without_masks = sorted(set(image_map) - set(mask_map))
masks_without_images = sorted(set(mask_map) - set(image_map))

print("\n========== FILE COUNTS ==========")
print("Total images:", len(images))
print("Total masks:", len(masks))
print("Matching pairs:", len(matched))
print("Images without masks:", len(images_without_masks))
print("Masks without images:", len(masks_without_images))

print("\nFirst 10 image filenames:")
for p in images[:10]:
    print(p.name)

print("\nFirst 10 mask filenames:")
for p in masks[:10]:
    print(p.name)

print("\n========== IMAGE AND MASK DETAILS ==========")

for name in matched[:10]:
    with Image.open(image_map[name]) as im:
        image_size = im.size
        image_mode = im.mode

    with Image.open(mask_map[name]) as im:
        mask_size = im.size
        mask_mode = im.mode
        mask_array = np.asarray(im)

    values, counts = np.unique(mask_array, return_counts=True)

    print(f"\nPair: {name}")
    print("Image dimensions:", image_size)
    print("Image mode:", image_mode)
    print("Mask dimensions:", mask_size)
    print("Mask mode:", mask_mode)
    print("Dimensions match:", image_size == mask_size)
    print("Mask array shape:", mask_array.shape)
    print("Mask data type:", mask_array.dtype)
    print("Unique mask pixel values:", len(values))
    print("Pixel values (up to 20):", values[:20].tolist())

    if len(values) <= 20:
        print("Pixel counts:", dict(zip(values.tolist(), counts.tolist())))

print("\n========== VISUAL INSPECTION ==========")

sample_names = matched[:6]

if sample_names:
    fig, axes = plt.subplots(
        len(sample_names), 2,
        figsize=(12, 4 * len(sample_names)),
        squeeze=False
    )

    for row, name in enumerate(sample_names):
        with Image.open(image_map[name]) as im:
            image_array = np.asarray(im.convert("RGB"))

        with Image.open(mask_map[name]) as im:
            mask_array = np.asarray(im)

        axes[row, 0].imshow(image_array)
        axes[row, 0].set_title(f"Original image: {name}")
        axes[row, 0].axis("off")

        axes[row, 1].imshow(mask_array, cmap="gray")
        axes[row, 1].set_title(f"Original mask: {name}")
        axes[row, 1].axis("off")

    plt.tight_layout()
    plt.show()
else:
    print("No matching filename pairs found.")

print("\nInspection completed. Original files were not modified.")
