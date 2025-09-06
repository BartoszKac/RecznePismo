import tkinter as tk
from PIL import Image, ImageTk
from Code.Utills.LoadData import Loader
import numpy as np

# --- Załaduj dane ---
loader = Loader('data/letters-test-images', 'data/letters-test-labels')
#loader = Loader('data/Timage', 'data/Ttest')
#loader = Loader('data/mnist-test-images', 'data/mnist-test-labels')

loader.sort_images_and_labels()

# --- Stan aplikacji ---
current_index = 0

def update_image():
    global current_index
    img_array = loader.getImage(current_index)
    label_num = loader.getClasTarget(current_index)
    label_char = loader.getTrueValue_letters(label_num)

    pil_img = Image.fromarray(img_array.astype(np.uint8))
    pil_img = pil_img.resize((200, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(pil_img)

    image_label.config(image=photo)
    image_label.image = photo
    text_label.config(text=f"Index: {current_index} | Klasa: {label_char} (kod: {label_num})")

def move(step):
    global current_index
    max_index = loader.getClasTarget().shape[0] - 1
    new_index = current_index + step
    # Ograniczenie, żeby nie wyjść poza zakres
    current_index = max(0, min(new_index, max_index))
    update_image()

def go_start():
    global current_index
    current_index = 0
    update_image()

def go_end():
    global current_index
    current_index = Loader.getClasTarget().shape[0] - 1
    update_image()

# --- GUI ---
root = tk.Tk()
root.title("Przeglądarka danych")

image_label = tk.Label(root)
image_label.pack(pady=10)

text_label = tk.Label(root, font=("Helvetica", 14))
text_label.pack()

# Kontrolki nawigacji
nav_frame = tk.Frame(root)
nav_frame.pack(pady=10)

# Początek
tk.Button(nav_frame, text="⏮ Początek", font=("Helvetica", 12), command=go_start).grid(row=0, column=0, padx=5)

# Przyciski cofania
tk.Button(nav_frame, text="← 10000", font=("Helvetica", 12), command=lambda: move(-10000)).grid(row=0, column=1, padx=5)
tk.Button(nav_frame, text="← 1000", font=("Helvetica", 12), command=lambda: move(-1000)).grid(row=0, column=2, padx=5)
tk.Button(nav_frame, text="← 100", font=("Helvetica", 12), command=lambda: move(-100)).grid(row=0, column=3, padx=5)
tk.Button(nav_frame, text="← 10", font=("Helvetica", 12), command=lambda: move(-10)).grid(row=0, column=4, padx=5)

# Przyciski do przodu
tk.Button(nav_frame, text="10 →", font=("Helvetica", 12), command=lambda: move(10)).grid(row=0, column=5, padx=5)
tk.Button(nav_frame, text="100 →", font=("Helvetica", 12), command=lambda: move(100)).grid(row=0, column=6, padx=5)
tk.Button(nav_frame, text="1000 →", font=("Helvetica", 12), command=lambda: move(1000)).grid(row=0, column=7, padx=5)
tk.Button(nav_frame, text="10000 →", font=("Helvetica", 12), command=lambda: move(10000)).grid(row=0, column=8, padx=5)

# Koniec
tk.Button(nav_frame, text="Koniec ⏭", font=("Helvetica", 12), command=go_end).grid(row=0, column=9, padx=5)

update_image()
root.mainloop()
