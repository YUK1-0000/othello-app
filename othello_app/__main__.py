def main() -> None:
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()


if __name__ == "__main__":
    import tkinter as tk
    from .controller import Controller
    main()