import os
import numpy as np
from .Constans import DATA_DIR,LAST_MODEL_PATH
from .ProgramState import ProgramStates


def zapisz_sciezke_modelu(sciezka):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LAST_MODEL_PATH, "w", encoding="utf-8") as f:
        f.write(sciezka)

def print_elements_from_start(arr):
    for i in range(len(arr)):
        print(f"{i}: {arr[i]:.9f}")
        
        
def zaladuj_ostatnie_dane_uczace():
    """Ładuje ostatni zapisany model jeśli istnieje."""
    if os.path.exists(LAST_MODEL_PATH):
        try:
            with open(LAST_MODEL_PATH, "r", encoding="utf-8") as f:
                sciezka = f.read().strip()
            if os.path.exists(sciezka):
                ProgramStates.perceptron.w = np.load(sciezka)
                print(f"[INFO] Automatycznie załadowano model: {sciezka}")
                return True
        except Exception as e:
            print(f"[BŁĄD] Nie udało się wczytać ostatniego modelu: {e}")
    return False       
        

