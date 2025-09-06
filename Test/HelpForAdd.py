import os
import numpy as np
from PIL import Image
from Code.Utills.LoadData import Loader  # ← Upewnij się, że masz klasę Loader z poprawką poniżej!




# 📂 KATALOG DO ZAPISU
output_dir = "LicterySame"
os.makedirs(output_dir, exist_ok=True)

# 📥 Załaduj dane
loader = Loader('data/letters-test-images', 'data/letters-test-labels')

#loader = Loader('data/Timage', 'data/Ttest')
#loader = Loader('data/mnist-test-images', 'data/mnist-test-labels')
loader.sort_images_and_labels()  # UWAGA: poprawiona wersja poniżej 👇

# 📊 Pobierz dane
labels = loader.getClasTarget()
images = loader.getImage()  # ← zwraca wszystkie obrazy 28x28

# 📌 Liczniki dla nazw plików
counters = {}

# 🔄 Zapisz każdy obraz jako plik PNG
for i in range(len(labels)):
    label = int(labels[i])
       
    if 0 <= label <= 9:
        continue
    
    char = Loader.getTrueValue(label)
    
    if char not in counters:
        counters[char] = 0
    else:
        counters[char] += 1

    img_array = images[i]
    img = Image.fromarray(img_array.astype(np.uint8), mode='L')
    filename = f"{char}_{counters[char]}.png"
    img.save(os.path.join(output_dir, filename))

print(f"✅ Zapisano {len(images)} liter do katalogu '{output_dir}'")
