import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from Code.Utills.ImageLoader import WordImageLoader  # zakładam, że klasa jest w ImageLoader.py

# --- Funkcja główna ---
def main():
    # Utwórz ukryte okno tkinter
    root = tk.Tk()
    root.withdraw()

    # Otwórz okno wyboru pliku
    filepath = filedialog.askopenfilename(
        title="Wybierz obraz z napisem",
        filetypes=[("Pliki PNG", "*.png"), ("Pliki JPG", "*.jpg"), ("Wszystkie pliki", "*.*")]
    )

    if not filepath:
        print("❌ Nie wybrano pliku.")
        return

    # Wczytaj obraz
    img = cv2.imread(filepath)
    if img is None:
        print("❌ Nie udało się wczytać obrazu")
        return

    # --- Wyciągnięcie liter ---
    letters = WordImageLoader.extract_letters(img)
    print(f"✅ Rozpoznano {len(letters)} liter")

    # --- Podgląd wszystkich liter ---
    for i, letter in enumerate(letters):
        cv2.imshow(f"Litera {i}", letter)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
