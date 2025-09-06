# testlo.py
import cv2
from tkinter import Tk, filedialog
from Code.Utills.ImageLoader import WordImageLoader

# --- Wybór pliku przez okno dialogowe ---
root = Tk()
root.withdraw()  # ukryj główne okno Tkinter
file_path = filedialog.askopenfilename(
    title="Wybierz obrazek z napisem",
    filetypes=[("Obrazy", "*.png;*.jpg;*.jpeg;*.bmp")]
)
root.destroy()

if not file_path:
    print("Nie wybrano pliku. Koniec programu.")
    exit()

# --- Inicjalizacja loadera ---
loader = WordImageLoader(file_path)

print(f"Label (nazwa pliku): {loader.getLabel()}")
print(f"Rozmiar oryginalny: {loader.size}")

# Przytnij marginesy
loader.crop_borders(threshold=250)
print(f"Rozmiar po przycięciu: {loader.size}")

# Wyświetl obraz po przycięciu
cv2.imshow("Przycięty napis", loader.getImage())
cv2.waitKey(0)

# --- Wycinanie liter ---
# extract_letters oczekuje obrazu w BGR
image_bgr = cv2.cvtColor(loader.getImage(), cv2.COLOR_GRAY2BGR)
letters = WordImageLoader.extract_letters(image_bgr)

print(f"Znaleziono liter: {len(letters)}")

# Podgląd liter 28x28
for i, letter in enumerate(letters):
    cv2.imshow(f"Litera {i+1}", letter)
    cv2.waitKey(0)

cv2.destroyAllWindows()
