import numpy as np
import matplotlib.pyplot as plt
from Code.Utills.ImageLoader import WordImageLoader
import tkinter as tk
from tkinter import filedialog
import cv2


def resize_with_padding(img, target_size=(1300, 1300)):
    h, w = img.shape
    scale = min(target_size[0]/w, target_size[1]/h)
    new_w, new_h = int(w*scale), int(h*scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # Utwórz pusty obraz (białe tło)
    padded = np.ones(target_size, dtype=np.uint8) * 255
    top = (target_size[1] - new_h)//2
    left = (target_size[0] - new_w)//2
    padded[top:top+new_h, left: left+new_w] = resized
    return padded


def main():
    # --- wybór pliku
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(
        title="Wybierz plik PNG z napisem",
        filetypes=[("Pliki PNG", "*.png"), ("Pliki JPG", "*.jpg"), ("Wszystkie pliki", "*.*")]
    )

    if not filepath:
        print("❌ Nie wybrano pliku.")
        return

    # --- 1. Pokaż obraz oryginalny
    loader = WordImageLoader(filepath)
    original_img = loader.getImage()

    plt.figure(figsize=(6, 6))
    plt.imshow(original_img, cmap="gray")
    plt.title("🖼️ Oryginalny obraz (bez obróbki)")
    plt.axis("off")
    plt.show()

    # --- 2. Przytnij krawędzie
    loader.crop_borders()
    cropped_img = loader.getImage()

    plt.figure(figsize=(6, 6))
    plt.imshow(cropped_img, cmap="gray")
    plt.title("✂️ Po crop_borders()")
    plt.axis("off")
    plt.show()

    # --- 3. Przeskaluj z paddingiem (np. do 1300x1300)
    word_img_resized = resize_with_padding(cropped_img)

    plt.figure(figsize=(8, 8))
    plt.imshow(word_img_resized, cmap="gray")
    plt.title("📐 Po resize_with_padding (1300x1300)")
    plt.axis("off")
    plt.show()

    # --- 4. Segmentacja na literki/cyfry
    letters = WordImageLoader.segment_word_to_letters(word_img_resized, target_size=(28, 28))
    print(f"🔠 Znaleziono {len(letters)} segmentów")

    fig, axes = plt.subplots(1, len(letters), figsize=(2*len(letters), 2))
    if len(letters) == 1:
        axes = [axes]

    for i, (ax, letter_img) in enumerate(zip(axes, letters), start=1):
        ax.imshow(letter_img, cmap="gray")
        ax.set_title(f"Litera {i}")
        ax.axis("off")

    plt.show()


if __name__ == "__main__":
    main()
