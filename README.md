# Jowar Maturity Detection System

## Overview

The Jowar Maturity Detection System is an AI-based system designed to detect Jowar panicles from field images or video frames, classify their maturity stage, and provide harvest-readiness information to the farmer.

## Project Objectives

1. Acquire and store Jowar field images from live camera, captured photographs, and uploaded images.
2. Detect and localize Jowar panicles using YOLO-based object detection.
3. Classify Jowar maturity stages and determine harvest readiness using deep learning models.
4. Provide real-time and explainable predictions through a farmer-facing interface.

## System Pipeline

Farmer Input
- Live Camera
- Capture Photo
- Upload Image

↓

Image/Frame Storage and Unique ID

↓

Image Preprocessing

↓

YOLO Panicle Detection

↓

Detected Panicle ROI

↓

Maturity Classification

↓

Harvest Readiness

↓

Grad-CAM / Explainable AI

↓

Farmer UI

## Project Modules

- `dataset/` – Dataset information and dataset-related resources
- `yolo/` – Jowar panicle detection
- `classification/` – Maturity-stage classification
- `preprocessing/` – Image preprocessing
- `explainability/` – Grad-CAM and XAI
- `ui/` – Farmer-facing interface
- `database/` – Image and prediction storage
- `integration/` – Integration of all system modules
- `docs/` – Project documentation

## Technology Stack

- Python
- PyTorch
- YOLO
- OpenCV
- Streamlit
- SQLite
- GitHub
- Jira

## Team Responsibilities

| Member | Responsibility |
|---|---|
| Rinku | Dataset & Research |
| Shruti | YOLO Panicle Detection |
| Trupti | Maturity Classification |
| Priti | UI & System Integration |

## Development Workflow

Each team member works on their assigned Git branch.

```text
dataset
yolo
classification
ui
