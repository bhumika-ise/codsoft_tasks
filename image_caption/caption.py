import re
import torch
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# 1. Select CPU because your PyTorch installation is CPU-only
device = "cpu"

# 2. Load the pre-trained BLIP image-captioning model
model_name = "Salesforce/blip-image-captioning-base"

print("Loading model...")

processor = AutoProcessor.from_pretrained(model_name)
model = BlipForConditionalGeneration.from_pretrained(model_name)

model.to(device)

print("Model loaded successfully!")

# 3. Load your image
from tkinter import Tk, filedialog

Tk().withdraw()

image_path = filedialog.askopenfilename(
    title="Select an image",
    filetypes=[
        ("Image files", "*.jpg *.jpeg *.png")
    ]
)
image = Image.open(image_path).convert("RGB")

# 4. Convert the image into the format required by the model
inputs = processor(images=image, return_tensors="pt")
inputs = {key: value.to(device) for key, value in inputs.items()}

# 5. Generate the caption
print("Generating caption...")

with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=30)

# 6. Convert model output into normal text
caption = processor.decode(output[0], skip_special_tokens=True)
words = caption.split()
clean_words = []

for word in words:
    if not clean_words or word != clean_words[-1]:
        clean_words.append(word)

caption = " ".join(clean_words)

# Remove repeated consecutive words
caption = re.sub(r'\b(\w+)(?:\s+\1\b)+', r'\1', caption, flags=re.IGNORECASE)

print("\nImage Caption:")
print(caption)