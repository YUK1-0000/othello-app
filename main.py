import tkinter as tk
from C import Controller


def main() -> None:
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()


if __name__ == "__main__":
    main()