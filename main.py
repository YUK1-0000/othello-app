import tkinter as tk


LMB = "<Button-1>"
LENGTH = 8
EMPTY, WHITE, BLACK = 0, 1, -1
DISK_TYPES = ("", "○", "●")
ARROW_TYPES = ("", "->", "<-")
DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
)


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
        print("Button pressed:", x, y)
        if self.board_data[y][x] == EMPTY and self.neighbor_flippable_disk_exists(x, y):
            self.place_disk(x, y)
    
    def place_disk(self, x: int, y: int) -> None:
        print("Move disk:", "White" if self.player.get() == WHITE else "Black", x, y)
        self.board_data[y][x] = self.player.get()
        self.flip(x, y)
        self.turn_over()
    
    def flip(self, x: int, y: int) -> None:
        # 8方向を探索
        for d in DIRECTIONS:
            # 1マス目の探索
            y_, x_ = y+d[0], x+d[1]
            
            if (
                not(0 <= y_ < LENGTH and 0 <= x_ < LENGTH)
                or self.board_data[y_][x_] != self.player.get()*-1
            ):
                continue
            
            # 2マス目以降の探索
            opponent_disk_count = 1
            
            for n in range(1, LENGTH):
                y_, x_ = y+d[0]*n, x+d[1]*n
                
                if not(0 <= y_ < LENGTH and 0 <= x_ < LENGTH):
                    break
                
                square_data = self.board_data[y_][x_]
                
                if square_data == EMPTY:
                    break # 返せる石が無いのでこの方向の探索をやめる
                
                if square_data == self.player.get()*-1:
                    opponent_disk_count += 1
                
                elif square_data == self.player.get():
                    # 石を返す
                    for m in range(1, opponent_disk_count):
                        print("Flip:", x+d[1]*m, y+d[0]*m)
                        self.board_data[y+d[0]*m][x+d[1]*m] = self.player.get()
                    break
    
    def turn_over(self) -> None:
        self.change_player()
        if not self.flippable_disk_exists():
            self.change_player()
        
        if not self.empty_square_exists():
            self.reset_game()
    
    def change_player(self) -> None:
        self.player.set(self.player.get()*-1)
    
    def reset_game(self) -> None:
        print("Reset game")
        self.player.set(BLACK)
        self.reset_board_texts()
        self.reset_board_data()
    
    def reset_board_texts(self) -> None:
        for y, text_list in enumerate(self.board_texts):
            for x, text in enumerate(text_list):
                if x == LENGTH/2 or y == LENGTH/2:
                    if x == y:
                        
                text.set(value=value)
    
    def reset_board_data(self) -> None:
        for data in self.board_data:
            for datum in data:
                datum = EMPTY
    
    def empty_square_exists(self) -> bool:
        return any(any(data) for data in self.board_data)
    
    def flippable_disk_exists(self) -> bool:
        return any(
            any(
                self.neighbor_flippable_disk_exists(x, y)
                for x in range(LENGTH)
            )
            for y in range(LENGTH)
        )
    
    def neighbor_flippable_disk_exists(self, x: int, y: int) -> bool:
        # 8方向を探索
        for d in DIRECTIONS:
            # 1マス目の探索
            y_, x_ = y+d[0], x+d[1]
            
            if (
                not (0 <= y_ < LENGTH and 0 <= x_ < LENGTH)
                or self.board_data[y_][x_] != self.player.get()*-1
            ):
                continue
            
            # 2マス目以降の探索
            is_opponent_disk_exist = False
            
            for n in range(1, LENGTH):
                y_, x_ = y+d[0]*n, x+d[1]*n
                
                if (
                    not (0 <= y_ < LENGTH and 0 <= x_ < LENGTH)
                    or self.board_data[y_][x_] == EMPTY
                ):
                    break
                
                square_data = self.board_data[y_][x_]
                
                if square_data == EMPTY:
                    break
                
                if square_data == self.player.get()*-1:
                    is_opponent_disk_exist = True
                
                elif square_data == self.player.get() and is_opponent_disk_exist:
                    return True
    
        return False


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
        self.black_disk_label = tk.Label(self.label_frame, text=DISK_TYPES[BLACK], font=("", 25))
        self.white_disk_label = tk.Label(self.label_frame, text=DISK_TYPES[WHITE], font=("", 25))

        self.label_frame.pack(fill=tk.BOTH)
        self.white_disk_label.pack(side=tk.RIGHT)
        self.black_disk_label.pack(side=tk.LEFT)
        
        self.pack()


class Controller:
    def __init__(self, root: tk.Tk) -> None:
        self.view = View(root)
        self.model = Model(root)
        
        # ボタンにコマンドとテキストの変数を設定
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
            for x, square_data in enumerate(data):
                self.model.board_texts[y][x].set(DISK_TYPES[square_data])
        
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