from PIL import Image
import pytesseract
import tkinter as tk
from tkinter import filedialog

# Jeśli Tesseract nie jest w PATH, odkomentuj i podaj ścieżkę
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Okno dialogowe do wyboru pliku
root = tk.Tk()
root.withdraw()  # Ukrywa główne okno Tkinter
file_path = filedialog.askopenfilename(
    title="Wybierz obraz",
    filetypes=[("Obrazy", "*.png;*.jpg;*.jpeg;*.bmp"), ("Wszystkie pliki", "*.*")]
)

if not file_path:
    print("❌ Nie wybrano pliku.")
    exit()

# Wczytaj obraz
image = Image.open(file_path)

# OCR
extracted_text = pytesseract.image_to_string(image, lang="eng")  # zmień "eng" np. na "pol" jeśli masz polski słownik

# Wynik
print("📄 Tekst z obrazu:")
print(extracted_text.strip())
