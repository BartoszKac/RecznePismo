from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image
import numpy as np
from Utills.model_utils import *
from Utills.ProgramState import ProgramStates

# ======= STATUS MODELU =======
def odswiez_status(status_label: tk.Label):
    """Odśwież ikonę statusu modelu."""
    status_label.config(text="✅" if ProgramStates.perceptron.w is not None else "⬜")

# ======= FUNKCJE ŁADOWANIA DANYCH =======
def zaladuj_dane_uczace(status_label: tk.Label = None):
    """Załaduj plik .npy i zaktualizuj perceptron."""
    sciezka = filedialog.askopenfilename(
        title="Wybierz plik .npy",
        filetypes=[("NumPy files", "*.npy")]
    )
    if sciezka:
        try:
            macierz = np.load(sciezka)
            ProgramStates.perceptron.w = macierz
            zapisz_sciezke_modelu(sciezka)
            print("Wczytano plik:", sciezka)
            if status_label:
                odswiez_status(status_label)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać modelu:\n{e}")
    else:
        print("Nie wybrano pliku.")

def zaladuj_dane_testowe(okno=None, callback=None):
    """Załaduj dane testowe (.png lub .npy) i opcjonalnie wywołaj callback."""
    plik = filedialog.askopenfilename(
        title="Wybierz dane do sprawdzenia (.npy lub .png)",
        filetypes=[("Pliki PNG", "*.png"), ("NumPy files", "*.npy")]
    )
    if not plik:
        return

    try:
        if plik.endswith(".png"):
            ProgramStates.sciezka_do_obrazka = plik
            img = Image.open(plik).convert("L")
            img1 = img.resize((28, 28), Image.Resampling.LANCZOS)
            tablica_danych = np.array(img1) / 255.0
            tablica_danych = tablica_danych.reshape(-1)
            print(tablica_danych)
            print(tablica_danych.shape)
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            messagebox.showinfo("Obrazek", f"Załadowano obrazek PNG:\n{plik}")

        if callback and okno:
            callback(okno)

    except Exception as e:
        messagebox.showerror("Błąd ładowania", f"Nie udało się załadować pliku:\n{e}")
