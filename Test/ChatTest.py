import easyocr
from tkinter import Tk, filedialog

# Wybór pliku
Tk().withdraw()
file_path = filedialog.askopenfilename(
    title="Wybierz obraz z tekstem odręcznym",
    filetypes=[("Obrazy", "*.png;*.jpg;*.jpeg;*.bmp"), ("Wszystkie pliki", "*.*")]
)

if not file_path:
    print("❌ Nie wybrano pliku.")
    exit()

# Inicjalizacja OCR (angielski, ale można dodać 'pl' dla polskiego)
reader = easyocr.Reader(['en', 'pl'])

# Rozpoznanie tekstu
results = reader.readtext(file_path)

# Wynik
print("📄 Rozpoznany tekst:")
for (bbox, text, prob) in results:
    print(f"- {text} (pewność: {prob:.2f})")
