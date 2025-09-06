import tkinter as tk
from PIL import Image, ImageTk

def inicjalizuj_zaznaczanie(canvas):
    rect = None
    start_x = start_y = 0
    crop_box = None

    def on_button_press(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def on_move_press(event):
        if rect:
            canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_button_release(event):
        nonlocal crop_box
        crop_box = (min(start_x, event.x), min(start_y, event.y),
                    max(start_x, event.x), max(start_y, event.y))

    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    def get_crop_box():
        return crop_box

    return get_crop_box


def wytnij_zaznaczenie(canvas, imga, crop_box):
    if crop_box:
        imga_cropped = imga.crop(crop_box)
        photo = ImageTk.PhotoImage(imga_cropped)
        canvas.delete("all")
        canvas.config(width=imga_cropped.width, height=imga_cropped.height)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo
        print("Obszar został przycięty ręcznie.")


def automatyczne_przyciecie(canvas, imga, ImageLoaderObject):
    try:
        c = ImageLoaderObject.crop_borders().getImage()
        imga_cropped = Image.fromarray((c * 255).astype('uint8'))
        photo = ImageTk.PhotoImage(imga_cropped)
        canvas.delete("all")
        canvas.config(width=imga_cropped.width, height=imga_cropped.height)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo
        print("Obraz przycięty automatycznie.")
    except Exception as e:
        print(f"Błąd przy automatycznym przycięciu: {e}")
