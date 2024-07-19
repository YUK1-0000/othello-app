import tkinter as tk


LMB = "<1>"
LENGTH = 8
EMPTY, WHITE, BLACK = 0, 1, -1
DISC_TYPES = ("", "○", "●")
ARROW_TYPES = ("", "->", "<-")


class View(tk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        self.root = root
        self.root.title("Othello")
        self.root.geometry("360x380")
        self.root.resizable(width=False, height=False)

        self.board_frame = tk.Frame(self)
        self.board_btns = [
            [
                tk.Button(
                    self.board_frame,
                    width=5, height=2,
                )
                for x in range(LENGTH)
            ]
            for y in range(LENGTH)
        ]
        
        self.board_frame.pack()
        for y, btns in enumerate(self.board_btns):
            for x, b in enumerate(btns):
                b.grid(column=x, row=y)

        self.label_frame = tk.Frame(self)
        self.arrow_label = tk.Label(self.label_frame, font=("", 25))
        black_disc_label = tk.Label(self.label_frame, text=DISC_TYPES[BLACK], font=("", 25))
        white_disc_label = tk.Label(self.label_frame, text=DISC_TYPES[WHITE], font=("", 25))

        self.label_frame.pack(fill=tk.BOTH)
        white_disc_label.pack(side=tk.RIGHT)
        black_disc_label.pack(side=tk.LEFT)
        
        self.pack()


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.view = View(self.root)
        self.player = tk.IntVar(value=BLACK)
        
        self.board_data = [[EMPTY for _ in range(LENGTH)] for _ in range(LENGTH)]
        for y in LENGTH/2-1, LENGTH/2:
            for x in LENGTH/2-1, LENGTH/2:
                self.board_data[int(y)][int(x)] = WHITE if x == y else BLACK

        self.board_texts = [[tk.StringVar() for _ in range(LENGTH)] for _ in range(LENGTH)]
        
        # ボタンにコマンドとテキスト変数を設定
        for y, btns in enumerate(self.view.board_btns):
            for x, btn in enumerate(btns):
                btn.configure(
                    textvariable=self.board_texts[y][x],
                    command=lambda x=x, y=y: self.move_disc(x, y)
                )
        
        self.update()

    def move_disc(self, x: int, y: int) -> None:
        self.board_data[y][x] = self.player.get()
        self.change_player()
        self.update()

    def change_player(self) -> None:
        self.player.set(self.player.get() * -1)

    def update(self) -> None:
        # 石の表示を更新
        for y, data in enumerate(self.board_data):
            for x, datum in enumerate(data):
                self.board_texts[y][x].set(DISC_TYPES[datum])
        
        # 矢印の表示を更新
        self.view.arrow_label.pack_forget()
        self.view.arrow_label.configure(text=ARROW_TYPES[self.player.get()])
        self.view.arrow_label.pack(side=tk.RIGHT if self.player.get() == WHITE else tk.LEFT)

def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()