import tkinter as tk

from puzzle_interface import PuzzleInterface


def main():
    root = tk.Tk()
    PuzzleInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
