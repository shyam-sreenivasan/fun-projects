from PIL import Image

def convert_images_to_pdf(image_paths, output_pdf_path):
    images = []
    for path in image_paths:
        img = Image.open(path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        images.append(img)

    if not images:
        raise ValueError("No valid images found")

    images[0].save(output_pdf_path, save_all=True, append_images=images[1:])