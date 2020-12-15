import tkinter as tk
from tkinter import filedialog
import glob

from augmentation import augment


def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askdirectory()
    jpgFilenamesList = glob.glob(file_path + '/*.jpg')
    output_folder = file_path + '/augment'
    for item in jpgFilenamesList:
        augment(item, output_folder)

if __name__== "__main__":
   main()