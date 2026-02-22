from transformers import Mask2FormerForUniversalSegmentation, Mask2FormerImageProcessor
from PIL import Image
import torch
import rasterio
from rasterio.features import shapes
import geopandas as gpd
import numpy as np
import os

input_folder = "/tmp/tif"
output_folder = "/tmp/geojson"
os.makedirs(output_folder, exist_ok=True)

# Load model and processor once
model = Mask2FormerForUniversalSegmentation.from_pretrained("mfaytin/mask2former-satellite")
processor = Mask2FormerImageProcessor.from_pretrained("mfaytin/mask2former-satellite")

Image.MAX_IMAGE_PIXELS = 100_000_000


# Loop over all .tif files
for tif_file in os.listdir(input_folder):
    if (
        not tif_file.lower().endswith(".tif")
        or tif_file.startswith("._")
        or tif_file.startswith(".")
    ):
        continue

    input_path = os.path.join(input_folder, tif_file)
    output_name = os.path.splitext(tif_file)[0] + "_buildings.geojson"
    output_path = os.path.join(output_folder, output_name)

    print(f"Processing {tif_file}...")

    image = Image.open(input_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    # Run inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Post-process to get segmentation map
    segmentation = processor.post_process_semantic_segmentation(
        outputs,
        target_sizes=[image.size[::-1]]  # (height, width)
    )[0]

    seg_map = segmentation.cpu().numpy()
    building_class_id = 7
    mask = (seg_map == building_class_id).astype("uint8")

    # Read georeference info
    with rasterio.open(input_path) as src:
        transform = src.transform
        crs = src.crs

    # Convert mask to polygons
    results = (
        {"properties": {"value": v}, "geometry": s}
        for s, v in shapes(mask, transform=transform)
        if v == 1
    )

    geoms = list(results)
    if not geoms:
        print(f"No buildings found in {tif_file}. Skipping.")
        continue

    gdf = gpd.GeoDataFrame.from_features(geoms, crs=crs)
    gdf["building_id"] = range(len(gdf))
    gdf["area"] = gdf.geometry.area

    # Save GeoJSON
    gdf.to_file(output_path, driver="GeoJSON")
    print(f"Saved {output_path}\n")