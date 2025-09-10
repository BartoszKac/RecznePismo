import numpy as np
import cv2
from Utills.LoadData import Loader
from Utills.ImageLoader import WordImageLoader
from Utills.ProgramState import ProgramStates

def sprawdz(wynik_label):
    """
    Funkcja wykonująca predykcję liter z załadowanego obrazu przy użyciu perceptronu.
    Wynik jest prezentowany w formie tabelki tekstowej w Labelu.
    """
    if ProgramStates.perceptron.w is None:
        wynik_label.config(text="Brak wczytanego modelu")
        return

    if ProgramStates.ImageLoaderObject is None:
        wynik_label.config(text="Brak obrazu do przetworzenia")
        return

    try:
        # Pobranie obrazu
        img_np = ProgramStates.ImageLoaderObject.getImage()
        letters = WordImageLoader.extract_letters(cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR))
        print(f"Znaleziono {len(letters)} liter")

        litery = []
        prawdop = []

        for i, l in enumerate(letters):
            x = l / 255.0
            x = x.flatten()
            x = np.append(x, 1)

            wyniky = ProgramStates.perceptron.predict(x)
            index = np.argmax(wyniky)
            maxWartosc = wyniky[index]

            predicted_char = Loader.index_to_letter(index)

            litery.append(predicted_char)
            prawdop.append(f"{maxWartosc:.2f}")

            print(f"Litera {i}: {predicted_char} ({maxWartosc:.2f})")
            print("Wyniki predykcji:", wyniky)

        # ustalamy szerokość kolumn
        col_width = 8
        letters_row = "Litery:    " + "".join(l.ljust(col_width) for l in litery)
        probs_row   = "Prawdop.: " + "".join(p.ljust(col_width) for p in prawdop)

        tekst_wynik = f"{letters_row}\n{probs_row}"

        # Label z monospace (Courier), żeby się nie rozjeżdżało
        wynik_label.config(text=tekst_wynik, font=("Courier", 14), justify="left")

    except Exception as e:
        wynik_label.config(text=f"Błąd podczas predykcji: {e}")
        print(f"[BŁĄD] {e}")
