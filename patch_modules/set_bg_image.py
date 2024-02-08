import tkinter as tk
from PIL import Image, ImageTk

def set_background_with_label(root, image_path):
        # IF USING PILLOW, OPEN THE IMAGE WITH PILLOW AND CONVERT IT TO A FORMAT TKINTER CAN USE
        image = Image.open(image_path)
        # image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(root, image=photo)
        label.place(x=0, y=0, relwidth=1, relheight=1)  # MAKE THE LABEL COVER THE WHOLE WINDOW

        # KEEP A REFERENCE TO THE IMAGE TO PREVENT GARBAGE COLLECTION
        label.image = photo