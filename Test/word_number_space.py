import os
from PIL import Image, ImageDraw, ImageFont
import random

# 📂 katalog do zapisu
output_dir = "handwriting_numbers_datasets_space"
os.makedirs(output_dir, exist_ok=True)

# ✍️ czcionki imitujące pismo odręczne (musisz mieć plik .ttf!)
fonts = [
    "EduNSWACTCursive-VariableFont_wght.ttf"
]

# 🔢 generowanie losowej liczby (1–5 cyfr)
def random_number_string(min_len=1, max_len=5):
    length = random.randint(min_len, max_len)
    return "".join(random.choice("0123456789") for _ in range(length))

# 🎲 generowanie obrazków
for i in range(50):  # 50 różnych liczb
    word = random_number_string()
    for j in range(20):  # 20 wariantów na liczbę
        font_size = random.randint(30, 50)
        font = ImageFont.truetype(random.choice(fonts), size=font_size)
        img = Image.new("L", (250, 80), color=255)  # białe tło
        draw = ImageDraw.Draw(img)

        # startowe przesunięcie
        x_offset = random.randint(5, 15)
        y_offset = random.randint(0, 20)

        # każdą cyfrę rysujemy osobno z odstępami
        for digit in word:
            draw.text((x_offset, y_offset), digit, font=font, fill=0)
            digit_width = font.getbbox(digit)[2]  # szerokość cyfry
            spacing = random.randint(10, 25)      # ODSTĘP między cyframi
            x_offset += digit_width + spacing

        # małe zakłócenia (szum)
        for _ in range(30):
            x, y = random.randint(0, img.width-1), random.randint(0, img.height-1)
            img.putpixel((x, y), random.choice([0, 255]))

        # ➡️ przycięcie do bounding boxu (żeby nie było pustych ramek)
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)

        filename = f"{word}_{j}.png"
        img.save(os.path.join(output_dir, filename))

print(f"✅ Zapisano {50*20} obrazków z liczbami w katalogu '{output_dir}'")
