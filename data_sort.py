import os
import shutil

SOURCE_DIRS = [
    "Hazardous/Hazardous",
    "Non-Recyclable/Non-Recyclable",
    "Organic/Organic",
    "Recyclable/Recyclable"
]

TARGET_DIR = "dataset"

os.makedirs(TARGET_DIR, exist_ok=True)

for src_root in SOURCE_DIRS:
    for class_name in os.listdir(src_root):
        src_path = os.path.join(src_root, class_name)
        dst_path = os.path.join(TARGET_DIR, class_name)

        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                shutil.move(src_path, dst_path)
                print(f"✅ Moved {class_name}")
            else:
                print(f"⚠️ Skipped {class_name} (already exists)")

print("\n🎉 Dataset successfully flattened into 18 classes")