import cv2
import os

# ==========================================
# 1. ORIGINAL MASKS
# ==========================================
mask_folder = r"C:\Users\Shruti Fugate\Documents\sem 3 project\data\data\sorghum\masks"

# ==========================================
# 2. YOLO LABELS OUTPUT FOLDER
# ==========================================
label_folder = r"C:\Users\Shruti Fugate\Desktop\Jowar-Maturity-Detection\yolo_dataset\Labels"

# Create Labels folder if it does not exist
os.makedirs(label_folder, exist_ok=True)

# Check whether mask folder exists
if not os.path.exists(mask_folder):
    print("ERROR: Mask folder not found!")
    print("Path checked:")
    print(mask_folder)
    input("Press Enter to close...")
    exit()

print("Mask folder found successfully!")
print("Starting conversion...")
print()

count = 0
skipped = 0

# ==========================================
# 3. READ ALL MASK FILES
# ==========================================
for filename in os.listdir(mask_folder):

    # Only PNG files
    if not filename.lower().endswith(".png"):
        continue

    mask_path = os.path.join(mask_folder, filename)

    # Read mask
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    if mask is None:
        print("Skipped:", filename)
        skipped += 1
        continue

    height, width = mask.shape

    # ==========================================
    # 4. CONVERT MASK TO BINARY
    # ==========================================
    _, binary = cv2.threshold(
        mask,
        127,
        255,
        cv2.THRESH_BINARY
    )

    # ==========================================
    # 5. FIND PANICLE OBJECTS
    # ==========================================
    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Output TXT filename
    txt_name = os.path.splitext(filename)[0] + ".txt"
    label_path = os.path.join(label_folder, txt_name)

    # ==========================================
    # 6. CREATE YOLO LABEL
    # ==========================================
    with open(label_path, "w") as file:

        for contour in contours:

            # Remove very small objects/noise
            area = cv2.contourArea(contour)

            if area < 10:
                continue

            # Bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Convert to YOLO format
            x_center = (x + w / 2) / width
            y_center = (y + h / 2) / height

            box_width = w / width
            box_height = h / height

            # Class 0 = sorghum panicle
            file.write(
                f"0 {x_center:.6f} {y_center:.6f} "
                f"{box_width:.6f} {box_height:.6f}\n"
            )

    count += 1

    # Show progress
    if count % 100 == 0:
        print(f"Processed {count} masks...")


# ==========================================
# 7. FINISHED
# ==========================================
print()
print("======================================")
print("YOLO LABEL CONVERSION COMPLETED!")
print("======================================")
print(f"Total masks processed : {count}")
print(f"Total masks skipped   : {skipped}")
print(f"Labels saved in       : {label_folder}")
print("======================================")