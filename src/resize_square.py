# resize_square.py (modo cover)
import os
from PIL import Image

INPUT_DIR = "src/static/images"
OUTPUT_DIR = "src/static/images/square"
SIZE = (1080, 1080)  

os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_square_cover(img, size=SIZE):
    img = img.convert("RGB")
    w, h = img.size
    target_w, target_h = size
    img_ratio = w / h
    target_ratio = target_w / target_h

    if img_ratio > target_ratio:
        new_h = target_h
        new_w = int(new_h * img_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / img_ratio)

    img = img.resize((new_w, new_h), Image.LANCZOS)

    # Recorte centrado
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    right = left + target_w
    bottom = top + target_h
    return img.crop((left, top, right, bottom))


for filename in sorted(os.listdir(INPUT_DIR)):
    if not filename.lower().endswith((".png",".jpg",".jpeg")):
        continue
    if to_process and filename not in to_process:
        continue

    src = os.path.join(INPUT_DIR, filename)
    dst = os.path.join(OUTPUT_DIR, filename)
    with Image.open(src) as im:
        out = make_square_cover(im)
        out.save(dst, "PNG")
        print("✅", dst)
