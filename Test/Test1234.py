import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import matplotlib.pyplot as plt

from Code.Neuron.Neuron import PerceptronSigmoid
from Code.Utills.ImageLoader import WordImageLoader


# ========================================
# Dialog wyboru pliku
def choose_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Wybierz obraz z liczbą",
        filetypes=[("Obrazy", "*.png;*.jpg;*.jpeg;*.bmp"), ("Wszystkie pliki", "*.*")]
    )
    root.destroy()
    return file_path


# ========================================
# Ręczne przycinanie w Tkinter (bez OpenCV)
def manual_crop_tk(image_path, save_cropped=False, save_path="cropped.png"):
    """
    Otwiera okno, pozwala myszką zaznaczyć prostokąt.
    Zwraca przycięty obraz jako tablicę numpy (skala szarości, uint8).
    """
    # Wczytaj obraz (PIL)
    pil_img = Image.open(image_path).convert("L")  # od razu w skali szarości

    # Ustal maksymalny rozmiar podglądu (okno)
    MAX_W, MAX_H = 1200, 800
    disp_img = pil_img.copy()
    scale = 1.0
    if disp_img.width > MAX_W or disp_img.height > MAX_H:
        disp_img.thumbnail((MAX_W, MAX_H), Image.LANCZOS)
        scale = pil_img.width / disp_img.width  # skala mapująca współrzędne z podglądu do oryginału

    root = tk.Tk()
    root.title("Ręczne przycinanie — zaznacz prostokąt myszką")

    canvas = tk.Canvas(root, width=disp_img.width, height=disp_img.height, cursor="tcross")
    canvas.pack(fill="both", expand=True)

    tk_img = ImageTk.PhotoImage(disp_img)
    canvas.create_image(0, 0, anchor="nw", image=tk_img)

    start = [0, 0]
    rect = [0, 0, 0, 0]  # x0, y0, x1, y1 w przestrzeni podglądu
    rect_id = [None]

    def on_button_press(event):
        start[0], start[1] = event.x, event.y
        rect[0], rect[1], rect[2], rect[3] = event.x, event.y, event.x, event.y
        if rect_id[0] is not None:
            canvas.delete(rect_id[0])
        rect_id[0] = canvas.create_rectangle(rect[0], rect[1], rect[2], rect[3], outline="red", width=2)

    def on_move(event):
        rect[2], rect[3] = event.x, event.y
        canvas.coords(rect_id[0], rect[0], rect[1], rect[2], rect[3])

    selection = {"bbox": None}

    def on_confirm():
        x0, y0, x1, y1 = rect
        # Normalizacja
        x_min, y_min = max(0, min(x0, x1)), max(0, min(y0, y1))
        x_max, y_max = min(disp_img.width, max(x0, x1)), min(disp_img.height, max(y0, y1))
        if x_max - x_min < 2 or y_max - y_min < 2:
            messagebox.showwarning("Uwaga", "Zaznacz większy obszar.")
            return
        selection["bbox"] = (x_min, y_min, x_max, y_max)
        root.destroy()

    def on_cancel():
        selection["bbox"] = None
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(fill="x", pady=6)
    tk.Button(btn_frame, text="Przytnij", command=on_confirm).pack(side="left", padx=4)
    tk.Button(btn_frame, text="Anuluj", command=on_cancel).pack(side="left", padx=4)
    tk.Label(btn_frame, text="Wskazówka: przeciągnij myszą, potem kliknij 'Przytnij'.").pack(side="left", padx=10)

    canvas.bind("<Button-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_move)

    root.mainloop()

    # Jeśli anulowano — zwróć oryginał w skali szarości
    if selection["bbox"] is None:
        cropped = pil_img
    else:
        x_min, y_min, x_max, y_max = selection["bbox"]
        # Przelicz współrzędne z podglądu na oryginał
        x_min = int(round(x_min * scale))
        y_min = int(round(y_min * scale))
        x_max = int(round(x_max * scale))
        y_max = int(round(y_max * scale))
        # Bezpieczeństwo
        x_min = max(0, min(x_min, pil_img.width - 1))
        y_min = max(0, min(y_min, pil_img.height - 1))
        x_max = max(1, min(x_max, pil_img.width))
        y_max = max(1, min(y_max, pil_img.height))
        # Crop
        cropped = pil_img.crop((x_min, y_min, x_max, y_max))

    # (Opcjonalnie) usuń białe marginesy z już wyciętego fragmentu
    cropped = ImageOps.invert(ImageOps.invert(cropped).getbbox() and cropped)  # trick na zachowanie oryginału gdy bbox=None
    bbox = ImageOps.invert(cropped).getbbox()
    if bbox:
        cropped = cropped.crop(bbox)

    if save_cropped:
        try:
            cropped.save(save_path)
            print(f"💾 Zapisano przycięty obraz: {save_path}")
        except Exception as e:
            print("⚠️ Nie udało się zapisać przyciętego obrazu:", e)

    # PIL -> numpy (uint8)
    return np.array(cropped, dtype=np.uint8)


# ========================================
# Główna logika
if __name__ == "__main__":
    # 1) Wybór pliku
    filepath = choose_file()
    if not filepath:
        print("❌ Nie wybrano pliku!")
        raise SystemExit

    # 2) Wybór trybu przycinania
    print("📂 Wybierz tryb przycinania:")
    print("1. Automatyczne (crop_borders z WordImageLoader)")
    print("2. Ręczne (myszką w Tkinter)")
    mode = input("👉 Twój wybór (1/2): ").strip()

    if mode == "2":
        # Ręczne kadrowanie (zapisz też kopię przyciętego pliku)
        word_img = manual_crop_tk(filepath, save_cropped=True, save_path="cropped.png")
    else:
        # Automatyczne przycinanie przez Twój loader
        loader = WordImageLoader(filepath)
        loader.crop_borders()
        word_img = loader.getImage()  # powinno zwrócić obraz w skali szarości (numpy)

    if word_img is None:
        print("❌ Błąd podczas wczytywania obrazu!")
        raise SystemExit

    # 3) Segmentacja na cyfry (przyjmuję, że metoda statyczna akceptuje numpy 2D)
    letters = WordImageLoader.segment_word_to_letters(word_img, target_size=(28, 28))
    print(f"🔢 Znaleziono cyfr: {len(letters)}")

    # 4) Wczytaj perceptron i jego wagi
    perceptron = PerceptronSigmoid()
    weights_path = r"C:/Users/User/Desktop/PythonWorkSpace/Projekt/WagiLiczby0-9.npy"
    perceptron.w = np.load(weights_path)
    print("✅ Wczytano wagi:", perceptron.w.shape)

    # 5) Rozpoznawanie cyfr
    recognized = []
    for i, letter_img in enumerate(letters):
        x = letter_img.flatten()
        x = np.append(x, 1)                   # bias -> (784+1,)
        probs = perceptron.predict(x)
        pred_class = int(np.argmax(probs))
        recognized.append(str(pred_class))

        # Podgląd
        plt.subplot(1, len(letters), i + 1)
        plt.imshow(letter_img, cmap="gray")
        plt.title(recognized[-1])
        plt.axis("off")

    plt.show()

    # 6) Sklej cyfry
    recognized_number = "".join(recognized)
    print("🔎 Rozpoznana liczba:", recognized_number)
