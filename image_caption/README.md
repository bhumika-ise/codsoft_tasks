# AI Image Caption Generator

An AI-powered image captioning application that automatically generates a meaningful description for an uploaded image.

## Project Description

This project combines **Computer Vision** and **Natural Language Processing (NLP)** to generate captions for images.

The application uses the pre-trained **Salesforce BLIP image captioning model** to understand an image and generate a natural-language caption.

## Features

- Upload an image from your computer
- Display the selected image
- Generate an AI-based caption
- Clear the selected image
- Simple and user-friendly Tkinter interface
- Supports JPG, JPEG, and PNG images

## Technologies Used

- Python
- Tkinter
- PyTorch
- Torchvision
- Hugging Face Transformers
- BLIP (Bootstrapping Language-Image Pre-training)
- Pillow

## Project Structure

```text
image_caption_project/
│
├── images/
│   ├── cat.jpg
│   ├── sport.jpg
│   └── test.jpg
│
├── app.py
├── caption.py
├── README.md
└── requirements.txt
