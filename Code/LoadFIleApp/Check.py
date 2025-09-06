import numpy as np
import cv2
from Utills.LoadData import Loader
from Utills.ImageLoader import WordImageLoader
from Utills.ProgramState import ProgramStates

def sprawdz(wynik_label):
    """
    Funkcja wykonująca predykcję liter z załadowanego obrazu przy użyciu perceptronu.
    
    Arguments:
        wynik_label (tk.Label): Label w GUI, w którym wyświetlany będzie wynik.
    """
    if ProgramStates.perceptron.w is None:
        wynik_label.config(text="Brak wczytanego modelu")
        return

    if ProgramStates.ImageLoaderObject is None:
        wynik_label.config(text="Brak obrazu do przetworzenia")
        return

    try:
        # Pobranie obrazu w formie numpy
        img_np = ProgramStates.ImageLoaderObject.getImage()
        letters = WordImageLoader.extract_letters(cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR))
        print(f"Znaleziono {len(letters)} liter")

        letters_row = "Litery:    "
        probs_row = "Pewności: "

        for i, l in enumerate(letters):
            # Normalizacja i spłaszczenie wektora wejściowego
            x = l / 255.0
            x = x.flatten()
            x = np.append(x, 1)  # dodanie biasu

            # Predykcja perceptronu
            wyniky = ProgramStates.perceptron.predict(x)
            index = np.argmax(wyniky)
            maxWartosc = wyniky[index]

            # Konwersja indeksu na literę
            predicted_char = Loader.index_to_letter(index)

            # Dodanie do wierszy
            letters_row += f"{predicted_char}\t"
            probs_row += f"{maxWartosc:.2f}\t"

            # Opcjonalnie: wydruk w konsoli
            print(f"Litera {i}: {predicted_char} ({maxWartosc:.2f})")
            print("Wyniki predykcji:", wyniky)

        # Złożenie tekstu w dwie linie
        tekst_wynik = f"{letters_row.strip()}\n{probs_row.strip()}"

        # Aktualizacja label w GUI
        wynik_label.config(text=tekst_wynik)

    except Exception as e:
        wynik_label.config(text=f"Błąd podczas predykcji: {e}")
        print(f"[BŁĄD] {e}")
