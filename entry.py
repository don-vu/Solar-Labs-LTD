from transformers import Mask2FormerForUniversalSegmentation, Mask2FormerImageProcessor
from PIL import Image
import torch

# Load model and processor
model = Mask2FormerForUniversalSegmentation.from_pretrained("mfaytin/mask2former-satellite")
processor = Mask2FormerImageProcessor.from_pretrained("mfaytin/mask2former-satellite")

# Load and preprocess image
Image.MAX_IMAGE_PIXELS = 100_000_000
image = Image.open('/Users/donvu/Downloads/6.tif').convert("RGB")
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
import matplotlib.cm as cm # Colormaps
import numpy as np

# 1. Get the actual number of classes from the model
num_classes = len(model.config.id2label)
print(f"This model supports {num_classes} classes.")

# 2. Create a dynamic palette using a Matplotlib colormap (e.g., 'viridis' or 'tab20')
# This automatically generates enough colors for every class the model knows
cmap = cm.get_cmap('tab20', num_classes)
palette = (cmap(np.arange(num_classes))[:, :3] * 255).astype(np.uint8)

# 3. Convert tensor to numpy
seg_map = segmentation.cpu().numpy()

# 4. Map the classes to colors
# Now palette[7] will exist because the palette is size 'num_classes'
color_seg = palette[seg_map]

# 5. Visualize
plt.figure(figsize=(10, 10))
plt.imshow(color_seg)
plt.title("Satellite Segmentation (All Classes)")
plt.axis("off")
plt.show()