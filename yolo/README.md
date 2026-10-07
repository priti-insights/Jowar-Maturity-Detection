# YOLO - Jowar Panicle Detection

## Purpose

This module detects and localizes Jowar (Sorghum) panicles in field images.

## Dataset

The dataset contains Sorghum panicle images and corresponding binary masks.

- Total images: 3,825
- Training images: 3,060
- Validation images: 765
- Classes: 1
- Class name: sorghum_panicle

## YOLO Dataset

The binary masks are converted into YOLO bounding-box labels.

Each label contains:

class_id x_center y_center width height

All coordinates are normalized between 0 and 1.

## Files

- `convert_masks.py` - Converts segmentation masks into YOLO bounding-box labels.
- `split_dataset.py` - Splits images and labels into training and validation sets.
- `data.yaml` - YOLO dataset configuration.
- `README.md` - Documentation.

## Model

YOLO11n is used for Jowar panicle detection.

## Output

The model detects Jowar panicles using bounding boxes and confidence scores.

## Note

The large dataset is not stored in this GitHub repository because of its size.