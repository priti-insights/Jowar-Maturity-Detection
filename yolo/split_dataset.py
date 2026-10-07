import os
import shutil
import random

# Original folders
image_folder = r"yolo_dataset\images"
label_folder = r"yolo_dataset\Labels"

# New folders
train_images = r"yolo_dataset\images\train"
val_images = r"yolo_dataset\images\val"

train_labels = r"yolo_dataset\labels\train"
val_labels = r"yolo_dataset\labels\val"

# Create folders
for folder in [train_images, val_images, train_labels, val_labels]:
    os.makedirs(folder, exist_ok=True)

# Get all images
images = [
    f for f in os.listdir(image_folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png")) and os.path.isfile(os.path.join(image_folder, f))
]

# Shuffle images
random.seed(42)
random.shuffle(images)

# 80% training, 20% validation
split_index = int(len(images) * 0.8)

train_list = images[:split_index]
val_list = images[split_index:]

print("Total images:", len(images))
print("Training images:", len(train_list))
print("Validation images:", len(val_list))

# Copy training files
for image in train_list:
    image_name = os.path.splitext(image)[0]
    label = image_name + ".txt"

    shutil.copy(
        os.path.join(image_folder, image),
        os.path.join(train_images, image)
    )

    shutil.copy(
        os.path.join(label_folder, label),
        os.path.join(train_labels, label)
    )

# Copy validation files
for image in val_list:
    image_name = os.path.splitext(image)[0]
    label = image_name + ".txt"

    shutil.copy(
        os.path.join(image_folder, image),
        os.path.join(val_images, image)
    )

    shutil.copy(
        os.path.join(label_folder, label),
        os.path.join(val_labels, label)
    )

print("\nDataset split completed!")
print("Train:", len(train_list))
print("Validation:", len(val_list))