from transformers import Mask2FormerForUniversalSegmentation, Mask2FormerImageProcessor
from PIL import Image
import torch

# Load model and processor
model = Mask2FormerForUniversalSegmentation.from_pretrained("mfaytin/mask2former-satellite")
processor = Mask2FormerImageProcessor.from_pretrained("mfaytin/mask2former-satellite")

# Load and preprocess image
Image.MAX_IMAGE_PIXELS = 100_000_000
image = Image.open('/Users/boi/Desktop/2026projects/HackEDD/images/1.tif').convert("RGB")
inputs = processor(images=image, return_tensors="pt")

# Run inference
with torch.no_grad():
    outputs = model(**inputs)

# Post-process to get segmentation map
segmentation = processor.post_process_semantic_segmentation(
    outputs,
    target_sizes=[image.size[::-1]]  # (height, width)
)[0]

# segmentation is a tensor of shape (H, W) with class IDs
print(f"Segmentation shape: {segmentation.shape}")
print(f"Unique classes: {torch.unique(segmentation).tolist()}")





import matplotlib.pyplot as plt
import numpy as np

# Convert tensor to numpy
seg_map = segmentation.cpu().numpy()

# Create binary mask for class 8 (Building)
building_class_id = 7
building_mask = (seg_map == building_class_id)

# Convert original image to numpy
image_np = np.array(image)

# Create red overlay
overlay = image_np.copy()
overlay[building_mask] = [255, 0, 0]  # Red color

print("Unique classes in segmentation:", torch.unique(segmentation))
print(model.config.id2label)


plt.figure(figsize=(10, 10))
plt.imshow(overlay)
plt.title("Buildings Highlighted in Red")
plt.axis("off")
plt.show()


import rasterio
from rasterio.features import shapes
import geopandas as gpd

building_class_id = 7
mask = (seg_map == building_class_id).astype("uint8")

with rasterio.open("/Users/boi/Desktop/2026projects/HackEDD/images/1.tif") as src:
    transform = src.transform
    crs = src.crs

results = (
    {"properties": {"value": v}, "geometry": s}
    for s, v in shapes(mask, transform=transform)
    if v == 1
)

geoms = list(results)

gdf = gpd.GeoDataFrame.from_features(geoms, crs=crs)
gdf["building_id"] = range(len(gdf))
gdf["area"] = gdf.geometry.area

gdf.to_file("/Users/boi/Desktop/2026projects/HackEDD/images/buildings.geojson", driver="GeoJSON")