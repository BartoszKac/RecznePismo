import numpy as np
from PIL import Image
import os
import cv2

class WordImageLoader:
    def __init__(self, filepath, size=None):
        """
        filepath: ścieżka do obrazka (.png / .jpg)
        size: (szer, wys), jeśli None → zostaje oryginalny rozmiar
        """
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Plik {filepath} nie istnieje")

        self.filepath = filepath
        self.size = size
        self.image = None
        self.label = None

        self._load_image()

    def _load_image(self):
        # np. hello.png -> label = "hello"
        self.label = os.path.splitext(os.path.basename(self.filepath))[0].split("_")[0]

        img = Image.open(self.filepath).convert("L")  # grayscale

        if self.size:
            img = img.resize(self.size)

        # zapisujemy obraz w uint8 0–255, nie float
        self.image = np.array(img, dtype=np.uint8)
        self.size = self.image.shape[::-1]  # (width, height)

    def getImage(self):
        return self.image

    def getLabel(self):
        return self.label

    def resize(self, new_size):
        """Zmień rozmiar już wczytanego obrazka"""
        img = Image.open(self.filepath).convert("L")
        img = img.resize(new_size)
        self.image = np.array(img, dtype=np.uint8)
        self.size = new_size

    def crop_borders(self, threshold=250):
        """
        Usuwa białe marginesy z obrazka i zostawia tylko największy obiekt (np. napis).
        threshold: (0-255) - im mniejszy tym więcej pikseli uzna za treść
        """
        arr = self.image.copy()

        # odwróć kolory: tło białe=0, napis=1
        _, thresh = cv2.threshold(arr, threshold, 255, cv2.THRESH_BINARY_INV)

        # znajdź wszystkie kontury
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print("⚠️ Uwaga: nie znaleziono obiektu na obrazie.")
            return self

        # wybierz największy obiekt
        biggest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)

        # przytnij do największego obiektu
        cropped = arr[y:y+h, x:x+w]

        # zapisujemy do self
        self.image = cropped
        self.size = (w, h)

        return self

    @staticmethod
    def extract_letters(image: np.ndarray) -> list[np.ndarray]:
        """
        Przyjmuje obraz (np.ndarray, BGR), zwraca listę obrazów liter (28x28).
        """
        # --- 1. Skala szarości + progowanie ---
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY_INV, 21, 20
        )

        # --- 2. Morfologia: łączenie fragmentów liter ---
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 6))
        merged = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # --- 3. Kontury ---
        contours, _ = cv2.findContours(merged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])  # sortowanie L→P

        letters = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 80:  # filtr śmieci
                x, y, w, h = cv2.boundingRect(cnt)
                letter_img = thresh[y:y+h, x:x+w]

                # Dopasowanie do 28x28
                resized = cv2.resize(letter_img, (28, 28), interpolation=cv2.INTER_AREA)
                letters.append(resized)

        return letters
