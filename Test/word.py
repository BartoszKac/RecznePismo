import os
from PIL import Image, ImageDraw, ImageFont
import random

# 📂 katalog do zapisu
output_dir = "handwriting_words_dataset"
os.makedirs(output_dir, exist_ok=True)

# 📋 lista słów
words = ["hello", "world", "python", "openai", "neuron", "test"]

# ✍️ czcionki imitujące pismo odręczne (musisz mieć te pliki .ttf w folderze)
fonts = [
    "EduNSWACTCursive-VariableFont_wght.ttf"
]


# 🎲 generowanie obrazków
for i, word in enumerate(words):
    for j in range(20):  # 20 wariantów na słowo
        font = ImageFont.truetype(random.choice(fonts), size=random.randint(30, 50))
        img = Image.new("L", (220, 70), color=255)  # białe tło
        draw = ImageDraw.Draw(img)

        # losowe przesunięcie tekstu
        x_offset = random.randint(5, 20)
        y_offset = random.randint(0, 15)

        # napis w "odręcznej" czcionce
        draw.text((x_offset, y_offset), word, font=font, fill=0)

        # małe zakłócenia (szum) żeby wyglądało bardziej naturalnie
        for _ in range(30):
            x, y = random.randint(0, img.width-1), random.randint(0, img.height-1)
            img.putpixel((x, y), random.choice([0, 255]))

        filename = f"{word}_{j}.png"
        img.save(os.path.join(output_dir, filename))

print(f"✅ Zapisano {len(words)*20} obrazków w katalogu '{output_dir}'")
