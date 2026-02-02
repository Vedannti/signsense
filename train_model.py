import cv2
import os
import numpy as np

dataset_path = "dataset"

labels = []
features = []

label_map = {
    "A": 0,
    "B": 1,
    "C": 2
}

print("📊 Loading dataset...")

for label in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, label)

    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (64, 64))
        img = img.flatten()

        features.append(img)
        labels.append(label_map[label])

features = np.array(features, dtype=np.float32)
labels = np.array(labels)

print("🤖 Training KNN model...")

knn = cv2.ml.KNearest_create()
knn.train(features, cv2.ml.ROW_SAMPLE, labels)

knn.save("gesture_knn.yml")

print("✅ Model trained successfully!")
print("💾 Saved as gesture_knn.yml")
