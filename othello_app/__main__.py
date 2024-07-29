def main() -> None:
    root = tk.Tk()
    Controller(root)
    root.mainloop()


if __name__ == "__main__":
    import tkinter as tk
    from othello_app import Controller
    main()