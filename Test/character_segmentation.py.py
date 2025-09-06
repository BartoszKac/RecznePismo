import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Wybór pliku przez okno dialogowe
Tk().withdraw()  # ukryj główne okno tkinter
file_path = askopenfilename(title="Wybierz obraz", filetypes=[("Obrazy", "*.jpg *.png *.jpeg *.bmp")])

if not file_path:
    print("Nie wybrano pliku!")
    exit()

# Wczytaj obraz w odcieniach szarości
image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

# Wstępne przetwarzanie
_, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)  # binarizacja
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilated_image = cv2.dilate(binary_image, kernel, iterations=1)  # dylatacja

# Znajdź kontury
contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iteracja po konturach
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 5 and h > 5:  # filtracja małych konturów (szum)
        char_image = binary_image[y:y+h, x:x+w]  # wycięcie znaku
        cv2.imshow('Character', char_image)  # wyświetlenie znaku
        cv2.waitKey(0)

cv2.destroyAllWindows()
