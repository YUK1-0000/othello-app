import tkinter as tk


LENGTH = 8
EMPTY, WHITE, BLACK = 0, 1, -1
DISK_ICONS = ("", "○", "●")
ARROW_TYPES = ("", "->", "<-")

DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
)

LMB = "Button-<1>"
FONT = ""
FONT_SIZES = {
    "L": 25
}
PASS_BTN_MSG = "Pass"
GAME_OVER_MSG = "GAME OVER!"


class Model:
    def __init__(self, root: tk.Tk) -> None:
        self.player = tk.IntVar(value=BLACK)
        self.disk_counts = [tk.IntVar() for _ in range(len(DISK_ICONS))]
        self.board_data = [[EMPTY for _ in range(LENGTH)] for _ in range(LENGTH)]
        self.reset()
    
    def on_btn_pressed(self, x: int, y: int) -> None:
        if self.is_placeable(x, y):
            self.place_disk(x, y, self.player.get())
            self.flip(x, y)
            self.count_disk()
            self.turn_end()
    
    def place_disk(self, x: int, y: int, disk_type: int) -> None:
        self.board_data[y][x] = disk_type
    
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
                        self.place_disk(x+d[1]*m, y+d[0]*m, self.player.get())
                    break
    
    def turn_end(self) -> None:
        self.change_player()
    
    def change_player(self) -> None:
        self.player.set(self.player.get()*-1)
    
    def count_disk(self) -> None:
        [int_var.set(0) for int_var in self.disk_counts]
        for y in range(LENGTH):
            for x in range(LENGTH):
                disk_type = self.board_data[y][x]
                self.disk_counts[disk_type].set(self.disk_counts[disk_type].get()+1)
    
    def reset(self) -> None:
        self.player.set(BLACK)
        self.reset_board_data()
        self.count_disk()
    
    def reset_board_data(self) -> None:
        for y in range(LENGTH):
            for x in range(LENGTH):
                if x in (LENGTH/2, LENGTH/2-1) and y in (LENGTH/2, LENGTH/2-1):
                    disk_type = WHITE if x == y else BLACK
                disk_type = EMPTY
                if x < 4:
                    disk_type = WHITE
                if x == 4:
                    disk_type = BLACK
                
                #else :
                #    disk_type = EMPTY
                self.place_disk(x, y, disk_type)
    
    def is_game_over(self) -> bool:
        return not self.empty_square_exists() or self.is_perfect_win()
    
    def empty_square_exists(self) -> bool:
        return any(any(data) for data in self.board_data)
    
    def is_perfect_win(self) -> bool:
        return not (self.disk_counts[BLACK].get() and self.disk_counts[WHITE].get())
    
    def placeable_square_exists(self) -> bool:
        return any(
            any(
                self.board_data[y][x] == EMPTY
                and self.is_placeable(x, y)
                for x in range(LENGTH)
            )
            for y in range(LENGTH)
        )
    
    def is_placeable(self, x: int, y: int) -> bool:
        if self.board_data[y][x] != EMPTY:
            return False
        
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
        root.title("Othello")
        root.geometry("360x380")
        root.resizable(width=False, height=False)
        
        self.btn_texts = [[tk.StringVar() for _ in range(LENGTH)] for _ in range(LENGTH)]
        
        # 盤面
        self.board_frame = tk.Frame(self)
        
        self.board_btns = [
            [
                tk.Button(
                    self.board_frame,
                    width=5,
                    height=2,
                    textvariable=self.btn_texts[y][x],
                )
                for x in range(LENGTH)
            ]
            for y in range(LENGTH)
        ]
        
        self.board_frame.pack()
        
        for y in range(LENGTH):
            for x in range(LENGTH):
                self.board_btns[y][x].grid(column=x, row=y)

        # 画面下側
        self.bottom_frame = tk.Frame(self)
        
        self.pass_btn = tk.Button(
            self.bottom_frame,
            font=(FONT, FONT_SIZES["L"]),
            text=PASS_BTN_MSG
        )
        
        self.arrow_label = tk.Label(self.bottom_frame, font=(FONT, FONT_SIZES["L"]))
        self.game_over_label = tk.Label(
            self.bottom_frame,
            text=GAME_OVER_MSG,
            font=(FONT, FONT_SIZES["L"])
        )
        self.disk_labels = [
            tk.Label(
                self.bottom_frame,
                font=(FONT, FONT_SIZES["L"]),
                textvariable=tk.StringVar(value=DISK_ICONS[type_])
            )
            for type_ in range(len(DISK_ICONS))
        ]
        self.disk_count_labels = [
            tk.Label(
                self.bottom_frame,
                font=(FONT, FONT_SIZES["L"]),
            )
            for _ in range(len(DISK_ICONS))
        ]

        self.bottom_frame.pack(fill=tk.BOTH)
        
        for i, s in (zip(range(1, len(DISK_ICONS)), (tk.RIGHT, tk.LEFT))):
            self.disk_count_labels[i].pack(side=s)
            self.disk_labels[i].pack(side=s)
        
        self.pack()
    
    def show_game_over_msg(self) -> None:
        self.arrow_label.pack_forget()
        self.game_over_label.pack()
    
    def reset(self) -> None:
        self.game_over_label.pack_forget()


class MenuBar(tk.Menu):
    def __init__(self, root: tk.Tk, *, reset_command) -> None:
        super().__init__(root)
        root.config(menu=self)
        
        self.menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Menu", menu=self.menu)
        self.menu.add_command(label="Reset Game", command=reset_command)


class Controller:
    def __init__(self, root: tk.Tk) -> None:
        self.model = Model(root)
        self.view = View(root)
        self.menu_bar = MenuBar(root, reset_command=self.reset)
        
        # ボタンにコマンドとテキストの変数を設定
        self.view.pass_btn.configure(command=self.change_player)
        for y in range(LENGTH):
            for x in range(LENGTH):
                self.view.board_btns[y][x].configure(
                    textvariable=self.view.btn_texts[y][x],
                    command=lambda x=x, y=y: self.on_btn_pressed(x, y)
                )
        
        for i in range(len(DISK_ICONS)):
            self.view.disk_count_labels[i].configure(
                textvariable=self.model.disk_counts[i]
            )
        
        self.update()

    # 石を打つときに呼ばれる関数
    def on_btn_pressed(self, x: int, y: int) -> None:
        self.model.on_btn_pressed(x, y)
        self.update()

    def change_player(self) -> None:
        self.model.change_player()
        self.update()

    # 表示の更新
    def update(self) -> None:
        # 石の表示を更新
        for y in range(LENGTH):
            for x in range(LENGTH):
                self.view.btn_texts[y][x].set(DISK_ICONS[self.model.board_data[y][x]])
        
        # 矢印の表示を更新
        self.view.arrow_label.pack_forget()
        self.view.arrow_label.configure(text=ARROW_TYPES[self.model.player.get()])
        self.view.arrow_label.pack(side=tk.RIGHT if self.model.player.get() == WHITE else tk.LEFT)
        
        # パスボタンの表示
        self.view.pass_btn.pack_forget()
        if not self.model.placeable_square_exists():
            self.view.pass_btn.pack()
    
    
    def game_over(self) -> None:
        self.view.show_game_over_msg()
    
    def reset(self) -> None:
        self.model.reset()
        self.update()


def main() -> None:
    root = tk.Tk()
    Controller(root)
    root.mainloop()


if __name__ == "__main__":
    main()