import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import os
from Neuron.Neuron import PerceptronSigmoid
from Utills.LoadData import Loader
from Utills.ImageLoader import WordImageLoader
import cv2
from Utills.ProgramState import ProgramStates    
from Utills.model_utils import *
from LoadFIleApp.WindowLoad import zaladuj_dane_uczace, zaladuj_dane_testowe, odswiez_status
from Utills.image_tools import inicjalizuj_zaznaczanie, wytnij_zaznaczenie, automatyczne_przyciecie
from LoadFIleApp.Check import sprawdz


def pokaz_ekran_sprawdzania(okno, pokaz_glowny_ekran):

    for widget in okno.winfo_children():
        widget.destroy()

    # ======= Górny pasek =======
    top_bar = tk.Frame(okno, bg="#ffffff", height=50)
    top_bar.pack(side="top", fill="x")

    btn_back = tk.Button(top_bar, text="← Wróć", command=lambda: pokaz_glowny_ekran(okno),
                         font=("Helvetica", 12), bg="#cccccc", relief="flat", padx=10)
    btn_back.pack(side="left", padx=10, pady=10)

    # ======= Główny content =======
    content = tk.Frame(okno, bg="#f2f2f2")
    content.pack(expand=True, fill="both")

    label_literka = tk.Label(content, font=("Helvetica", 40, "bold"), bg="#f2f2f2")
    label_literka.pack(pady=20)

    # ======= Wyświetlanie obrazu =======
    if ProgramStates.sciezka_do_obrazka is not None:
        try:
            ProgramStates.ImageLoaderObject = WordImageLoader(ProgramStates.sciezka_do_obrazka)

            # Obraz w PIL
            imga = Image.fromarray((ProgramStates.ImageLoaderObject.getImage() * 255).astype('uint8'))

            display_width = 400
            display_height = 400
            imga_resized = imga.resize((display_width, display_height), Image.Resampling.LANCZOS)

            canvas = tk.Canvas(content, width=display_width, height=display_height, bg="#f2f2f2")
            canvas.pack(pady=10)
            photo = ImageTk.PhotoImage(imga_resized)
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.image = photo

            # ======= Zaznaczanie i przycinanie =======
            get_crop_box = inicjalizuj_zaznaczanie(canvas)

            btn_frame = tk.Frame(content, bg="#f2f2f2")
            btn_frame.pack(pady=5)

            btn_auto_crop = tk.Button(btn_frame, text="Automatyczne przycięcie",
                                      command=lambda: automatyczne_przyciecie(canvas, imga, ProgramStates.ImageLoaderObject),
                                      font=("Helvetica", 12), bg="#4CAF50", fg="white")
            btn_auto_crop.pack(side="left", padx=5)

            btn_manual_crop = tk.Button(btn_frame, text="Wytnij zaznaczenie",
                                        command=lambda: wytnij_zaznaczenie(canvas, imga, get_crop_box()),
                                        font=("Helvetica", 12), bg="#FF5722", fg="white")
            btn_manual_crop.pack(side="left", padx=5)

        except Exception as e:
            tk.Label(content, text=f"Błąd ładowania obrazka: {e}", fg="red").pack()
    else:
        label_literka.config(text="Brak wczytanej literki", image="")
        label_literka.image = None

    # ======= Label na wynik =======
    wynik_label = tk.Label(content, text="Wynik: ?", font=("Helvetica", 16), bg="#f2f2f2", fg="#333")
    wynik_label.pack(pady=10)

    # ======= Przycisk sprawdzania liter =======
    btn_sprawdz = tk.Button(content, text="Sprawdź", command=lambda: sprawdz(wynik_label),
                            font=("Helvetica", 14), bg="#4CAF50", fg="white", padx=20, pady=10, relief="flat")
    btn_sprawdz.pack(pady=20)



def pokaz_glowny_ekran(okno):
    for widget in okno.winfo_children():
        widget.destroy()

    # ======= STATUS MODELU =======
    ProgramStates.status_label = tk.Label(okno, text="⬜", font=("Helvetica", 16), fg="green", bg="#f0f0f5")
    ProgramStates.status_label.pack()

    # ======= NAGŁÓWEK =======
    naglowek = tk.Label(okno, text="Wybierz opcję:", font=("Helvetica", 16, "bold"), bg="#f0f0f5", fg="#333")
    naglowek.pack(pady=30)

    # ======= PRZYCISKI =======
    tk.Button(okno, text="Wybierz dane uczące", command=lambda: zaladuj_dane_uczace(ProgramStates.status_label),
              font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=10, relief="flat").pack(pady=10)

    tk.Button(okno, text="Wybierz dane do sprawdzenia", command=lambda: zaladuj_dane_testowe(okno),
              font=("Helvetica", 12), bg="#2196F3", fg="white", padx=20, pady=10, relief="flat").pack(pady=10)

    tk.Button(okno, text="Sprawdź dane", command=lambda: pokaz_ekran_sprawdzania(okno,pokaz_glowny_ekran),
              font=("Helvetica", 12), bg="#FFC107", fg="black", padx=20, pady=10, relief="flat").pack(pady=10)

    tk.Button(okno, text="Wyjdź", command=okno.quit,
              font=("Helvetica", 12), bg="#f44336", fg="white", padx=20, pady=10, relief="flat").pack(pady=10)

    # ======= AUTO-ŁADOWANIE MODELU =======
    if zaladuj_ostatnie_dane_uczace():
        pass
        odswiez_status(ProgramStates.status_label)

