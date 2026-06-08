import tkinter as tk
import shutil
from os import startfile as start
from pathlib import Path

def install_file(filename):
    try:
        src = Path(__file__).resolve().parent / filename
        dest = Path.home() / "Desktop"
        shutil.copy2(src, dest)
    except:
        pass

def quick_play():
    start(Path(__file__).resolve().parent / "אוצרות או צרות.html")
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Installer")
    root.geometry("400x150")
    tk.Label(root, text="Welcome to the Installer", font=("Arial", 16, "bold")).pack(side="top", pady=15)
    buttons = tk.Frame(root)
    buttons.pack()
    tk.Button(buttons, text="Install EXE", font=("Arial", 14), command=lambda: install_file("אוצרות או צרות.exe")).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(buttons, text="Install HTML", font=("Arial", 14), command=lambda: install_file("אוצרות או צרות.html")).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Quick play", font=("Arial", 14), command=lambda: quick_play()).pack()
    root.mainloop()