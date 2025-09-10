import tkinter as tk
from PIL import Image, ImageTk
from . import Interface

# ===== Ustawienia gradientu =====
GRADIENT_START_COLOR = "#6A0DAD"
GRADIENT_END_COLOR = "#E066FF"

# ===== Funkcja tworząca gradient PIL =====
def draw_gradient(canvas, start_color=GRADIENT_START_COLOR, end_color=GRADIENT_END_COLOR):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width <= 0 or height <= 0:
        return

    img = Image.new("RGB", (width, height), start_color)

    r1, g1, b1 = int(start_color[1:3],16), int(start_color[3:5],16), int(start_color[5:7],16)
    r2, g2, b2 = int(end_color[1:3],16), int(end_color[3:5],16), int(end_color[5:7],16)

    for y in range(height):
        ratio = y / height
        r = int(r1*(1-ratio) + r2*ratio)
        g = int(g1*(1-ratio) + g2*ratio)
        b = int(b1*(1-ratio) + b2*ratio)
        for x in range(width):
            img.putpixel((x,y),(r,g,b))

    tk_img = ImageTk.PhotoImage(img)
    canvas.image = tk_img
    canvas.create_image(0, 0, anchor="nw", image=tk_img)

# ===== Funkcja tworząca aplikację =====
def create_app():
    okno = tk.Tk()
    okno.title("Aplikacja – Zarządzanie danymi")

    screen_width = okno.winfo_screenwidth()
    screen_height = okno.winfo_screenheight()
    okno.geometry(f"{screen_width}x{screen_height}+0+0")
    okno.resizable(False, False)

    # ===== Canvas z gradientem =====
    canvas = tk.Canvas(okno, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.bind("<Configure>", lambda event: draw_gradient(canvas))
    draw_gradient(canvas)

    # ===== Ramka na interfejs nad gradientem =====
    frame = tk.Frame(canvas, bg='', highlightthickness=0)
    frame.place(relwidth=1, relheight=1)

    Interface.pokaz_glowny_ekran(frame)

    return okno
