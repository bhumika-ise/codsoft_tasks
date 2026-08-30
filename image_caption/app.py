
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration


# ==========================================
# LOAD AI MODEL
# ==========================================

model_name = "Salesforce/blip-image-captioning-base"

processor = BlipProcessor.from_pretrained(model_name)
model = BlipForConditionalGeneration.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

print("Model loaded successfully!")
print("Using device:", device)


# ==========================================
# CREATE WINDOW
# ==========================================

root = tk.Tk()

root.title("AI Image Caption Generator")
root.geometry("800x750")
root.configure(bg="#f2f2f2")

# Prevent the window from becoming too small
root.minsize(700, 650)


# ==========================================
# VARIABLES
# ==========================================

# Original image used by AI
image = None

# Image displayed in Tkinter
photo = None


# ==========================================
# TITLE
# ==========================================

title = tk.Label(
    root,
    text="AI Image Caption Generator",
    font=("Arial", 24, "bold"),
    bg="#f2f2f2",
    fg="black"
)

title.pack(pady=(25, 10))


# ==========================================
# SUBTITLE
# ==========================================

subtitle = tk.Label(
    root,
    text="Upload an image and let AI describe it",
    font=("Arial", 12),
    bg="#f2f2f2",
    fg="#555555"
)

subtitle.pack(pady=(0, 15))


# ==========================================
# IMAGE FRAME
# ==========================================

image_frame = tk.Frame(
    root,
    width=550,
    height=380,
    bg="white",
    relief="solid",
    borderwidth=1
)

image_frame.pack(pady=10)

# Keep the frame size fixed
image_frame.pack_propagate(False)


# ==========================================
# IMAGE DISPLAY LABEL
# ==========================================

image_label = tk.Label(
    image_frame,
    text="No image selected",
    font=("Arial", 14),
    bg="white",
    fg="#555555"
)

image_label.pack(
    expand=True
)


# ==========================================
# CAPTION DISPLAY
# ==========================================

caption_label = tk.Label(
    root,
    text="Your caption will appear here",
    font=("Arial", 15, "bold"),
    wraplength=700,
    bg="#f2f2f2",
    fg="black"
)

caption_label.pack(
    pady=20
)


# ==========================================
# CHOOSE IMAGE FUNCTION
# ==========================================

def choose_image():

    global image
    global photo

    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")
        ]
    )

    if not file_path:
        return

    try:

        # Load original image
        image = Image.open(file_path).convert("RGB")

        # Make a COPY for display
        display_image = image.copy()

        # Resize only the display copy
        display_image.thumbnail(
            (520, 350),
            Image.Resampling.LANCZOS
        )

        # Convert to Tkinter image
        photo = ImageTk.PhotoImage(display_image)

        # Display image
        image_label.config(
            image=photo,
            text=""
        )

        # VERY IMPORTANT:
        # Keep reference to image
        image_label.image = photo

        # Update caption message
        caption_label.config(
            text="Image selected. Click Generate Caption."
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Could not open the image.\n\n{e}"
        )


# ==========================================
# GENERATE CAPTION FUNCTION
# ==========================================

def generate_caption():

    global image

    # Check whether image was selected
    if image is None:

        messagebox.showwarning(
            "No Image",
            "Please choose an image first."
        )

        return

    # Show loading message
    caption_label.config(
        text="Generating caption..."
    )

    # Refresh the window
    root.update_idletasks()

    try:

        # Process original image
        inputs = processor(
            images=image,
            return_tensors="pt"
        )

        # Move inputs to CPU/GPU
        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }

        # Generate caption
        with torch.no_grad():

            output = model.generate(
                **inputs,
                max_new_tokens=30
            )

        # Convert generated tokens to text
        caption = processor.decode(
            output[0],
            skip_special_tokens=True
        )

        # Display caption
        caption_label.config(
            text=caption
        )

    except Exception as e:

        caption_label.config(
            text="Unable to generate caption."
        )

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n\n{e}"
        )


# ==========================================
# CLEAR FUNCTION
# ==========================================

def clear_image():

    global image
    global photo

    # Remove stored images
    image = None
    photo = None

    # Remove image from label
    image_label.config(
        image="",
        text="No image selected"
    )

    # Remove old Tkinter image reference
    image_label.image = None

    # Reset caption
    caption_label.config(
        text="Your caption will appear here"
    )


# ==========================================
# BUTTON FRAME
# ==========================================

button_frame = tk.Frame(
    root,
    bg="#f2f2f2"
)

button_frame.pack(
    pady=15
)


# ==========================================
# CHOOSE IMAGE BUTTON
# ==========================================

choose_button = tk.Button(
    button_frame,
    text="Choose Image",
    command=choose_image,
    font=("Arial", 13, "bold"),
    padx=20,
    pady=10,
    cursor="hand2"
)

choose_button.grid(
    row=0,
    column=0,
    padx=10
)


# ==========================================
# GENERATE CAPTION BUTTON
# ==========================================

generate_button = tk.Button(
    button_frame,
    text="Generate Caption",
    command=generate_caption,
    font=("Arial", 13, "bold"),
    padx=20,
    pady=10,
    cursor="hand2"
)

generate_button.grid(
    row=0,
    column=1,
    padx=10
)


# ==========================================
# CLEAR BUTTON
# ==========================================

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_image,
    font=("Arial", 13, "bold"),
    padx=20,
    pady=10,
    cursor="hand2"
)

clear_button.grid(
    row=0,
    column=2,
    padx=10
)


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()