import os
from PIL import Image, ImageDraw, ImageFont
import random

# 📂 katalog do zapisu
output_dir = "handwriting_numbers_datasets"
os.makedirs(output_dir, exist_ok=True)

# ✍️ czcionki imitujące pismo odręczne (musisz mieć plik .ttf!)
fonts = [
    "EduNSWACTCursive-VariableFont_wght.ttf"
]

# 🔢 generowanie "słów", które są liczbami (np. 123, 5049, 7)
def random_number_string(min_len=1, max_len=5):
    length = random.randint(min_len, max_len)
    return "".join(random.choice("0123456789") for _ in range(length))

# 🎲 generowanie obrazków
for i in range(50):  # 50 różnych liczb
    word = random_number_string()
    for j in range(20):  # 20 wariantów na liczbę
        font = ImageFont.truetype(random.choice(fonts), size=random.randint(30, 50))
        img = Image.new("L", (220, 70), color=255)  # białe tło
        draw = ImageDraw.Draw(img)

        # losowe przesunięcie tekstu
        x_offset = random.randint(5, 20)
        y_offset = random.randint(0, 15)

        # napis (tu: liczba)
        draw.text((x_offset, y_offset), word, font=font, fill=0)

        # małe zakłócenia (szum)
        for _ in range(30):
            x, y = random.randint(0, img.width-1), random.randint(0, img.height-1)
            img.putpixel((x, y), random.choice([0, 255]))

        # ➡️ przycięcie do bounding boxu
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)

        filename = f"{word}_{j}.png"
        img.save(os.path.join(output_dir, filename))

print(f"✅ Zapisano {50*20} obrazków z liczbami w katalogu '{output_dir}'")
