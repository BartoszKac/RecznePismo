import numpy as np
from tkinter import Tk, filedialog

# Ukryj główne okno tkinter
Tk().withdraw()

# Otwórz okno wyboru pliku
sciezka = filedialog.askopenfilename(
    title="Wybierz plik .npy",
    filetypes=[("NumPy files", "*.npy")]
)

# Wczytaj plik jeśli coś wybrano
if sciezka:
    macierz = np.load(sciezka)
    print("Wczytano plik:", sciezka)
    print("Wymiary macierzy:", macierz.shape)
else:
    print("Nie wybrano pliku.")
