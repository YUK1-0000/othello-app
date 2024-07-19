import tkinter as tk


LMB = "<Button-1>"
LENGTH = 8
EMPTY, WHITE, BLACK = 0, 1, -1
DISC_TYPES = ("", "○", "●")
ARROW_TYPES = ("", "->", "<-")


class Model:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        
        self.player = tk.IntVar(value=BLACK)
        self.board_texts = [[tk.StringVar() for _ in range(LENGTH)] for _ in range(LENGTH)]
        self.board_data = [[EMPTY for _ in range(LENGTH)] for _ in range(LENGTH)]
        
        # 中心の4マスに石を置く
        for y in LENGTH/2-1, LENGTH/2:
            for x in LENGTH/2-1, LENGTH/2:
                self.board_data[int(y)][int(x)] = WHITE if x == y else BLACK
    
    def on_button_pressed(self, x: int, y: int) -> None:
        if self.flippable(x, y):
            self.move_disc(x, y)
    
    def move_disc(self, x: int, y: int) -> None:
        self.board_data[y][x] = self.player.get()
        self.flip(x, y)
        self.change_player()
    
    def flippable(self, x: int, y: int) -> bool:
        if self.board_data[y][x] == EMPTY:
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if 0 <= y+i < LENGTH and 0 <= x+j < LENGTH:
                        if self.board_data[y+i][x+j] == self.player.get()*-1:
                            count = 1
                            for n in range(LENGTH):
                                if 0 <= y+i*(n+1) < LENGTH and 0 <= x+j*(n+1) < LENGTH:
                                    if self.board_data[y+i*(n+1)][x+j*(n+1)] == self.player.get()*-1:
                                        count += 1
                                    elif self.board_data[y+i*(n+1)][x+j*(n+1)] == self.player.get():
                                        return True
        return False

    def flip(self, x: int, y: int) -> None:
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if 0 <= y+i < LENGTH and 0 <= x+j < LENGTH:
                    if self.board_data[y+i][x+j] == self.player.get()*-1:
                        count = 1
                        for n in range(LENGTH):
                            if 0 <= y+i*(n+1) < LENGTH and 0 <= x+j*(n+1) < LENGTH:
                                if self.board_data[y+i*(n+1)][x+j*(n+1)] == EMPTY:
                                    break
                                elif self.board_data[y+i*(n+1)][x+j*(n+1)] == self.player.get()*-1:
                                    count += 1
                                elif self.board_data[y+i*(n+1)][x+j*(n+1)] == self.player.get():
                                    for m in range(count):
                                        self.board_data[y+i*(m+1)][x+j*(m+1)] = self.player.get()
                                    break
    
    def change_player(self) -> None:
        self.player.set(self.player.get()*-1)


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
        self.black_disc_label = tk.Label(self.label_frame, text=DISC_TYPES[BLACK], font=("", 25))
        self.white_disc_label = tk.Label(self.label_frame, text=DISC_TYPES[WHITE], font=("", 25))

        self.label_frame.pack(fill=tk.BOTH)
        self.white_disc_label.pack(side=tk.RIGHT)
        self.black_disc_label.pack(side=tk.LEFT)
        
        self.pack()


class Controller:
    def __init__(self, root: tk.Tk) -> None:
        self.view = View(root)
        self.model = Model(root)
        
        # ボタンにコマンドとテキスト変数を設定
        for y, btns in enumerate(self.view.board_btns):
            for x, btn in enumerate(btns):
                btn.configure(
                    textvariable=self.model.board_texts[y][x],
                    command=lambda x=x, y=y: self.on_button_pressed(x, y)
                )
        self.update()

    # 石を打つときに呼ばれる関数
    def on_button_pressed(self, x: int, y: int) -> None:
        self.model.on_button_pressed(x, y)
        self.update()

    # 表示の更新
    def update(self) -> None:
        # 石の表示を更新
        for y, data in enumerate(self.model.board_data):
            for x, datum in enumerate(data):
                self.model.board_texts[y][x].set(DISC_TYPES[datum])
        
        # 矢印の表示を更新
        self.view.arrow_label.pack_forget()
        self.view.arrow_label.configure(text=ARROW_TYPES[self.model.player.get()])
        self.view.arrow_label.pack(side=tk.RIGHT if self.model.player.get() == WHITE else tk.LEFT)


def main() -> None:
    root = tk.Tk()
    Controller(root)
    root.mainloop()


if __name__ == "__main__":
    main()