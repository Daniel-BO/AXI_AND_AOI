import os
import tkinter as tk
from tkinter import filedialog, messagebox
from glob import glob
import cv2
import numpy as np

# ---------------------------
# STEP 1: Extract JPEGs from .jpgx single file
# ---------------------------
def extract_jpegs(input_file, output_dir="frames"):
    with open(input_file, "rb") as f:
        data = f.read()

    start_marker = b"\xFF\xD8"
    end_marker   = b"\xFF\xD9"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    index = 0
    count = 0
    while True:
        start = data.find(start_marker, index)
        if start == -1:
            break
        end = data.find(end_marker, start)
        if end == -1:
            break
        end += 2
        jpeg_data = data[start:end]
        count += 1
        filename = os.path.join(output_dir, f"img_{count:03d}.jpg")
        with open(filename, "wb") as out:
            out.write(jpeg_data)
        index = end
    return count


# ---------------------------
# STEP 2: GUI with Tkinter
# ---------------------------
def run_gui():
    def select_file():
        file_path = filedialog.askopenfilename(title="Select file .jpgx",
                                               filetypes=[("JPGX files", "*.jpgx"), ("All", "*.*")])
        if file_path:
            entry_file.delete(0, tk.END)
            entry_file.insert(0, file_path)

    def process():
        archivo = entry_file.get()
        if not os.path.isfile(archivo):
            messagebox.showerror("Error", "Select a valid file")
            return

        n_imgs = extract_jpegs(archivo, "frames")
        if n_imgs == 0:
            messagebox.showerror("Error", "No jpg files found on file")
            return

    root = tk.Tk()
    root.title("Get images from JPGX (X Ray images AXI output file )")

    tk.Label(root, text="File .jpgx:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_file = tk.Entry(root, width=50)
    entry_file.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Explore", command=select_file).grid(row=0, column=2, padx=5, pady=5)


    tk.Button(root, text="Get images", command=process, bg="green", fg="white").grid(row=2, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
