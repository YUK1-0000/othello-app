import tkinter as tk
from .model import Model
from .view import SuperFrame, MenuBar


BOARD_LEN = 8
EMPTY, WHITE, BLACK = 0, 1, -1
DISK_ICONS = ("", "○", "●")
ARROW_TYPES = ("", "->", "<-")


class Controller:
    def __init__(self, root: tk.Tk) -> None:
        self.model = Model(root)
        self.super_frame = SuperFrame(root)
        self.menu_bar = MenuBar(root, reset_command=self.reset)
        
        # ボタンにコマンドとテキストの変数を設定
        self.super_frame.pass_btn.configure(command=self.change_player)
        for y in range(BOARD_LEN):
            for x in range(BOARD_LEN):
                self.super_frame.board_btns[y][x].configure(
                    textvariable=self.super_frame.btn_texts[y][x],
                    command=lambda y=y, x=x: self.on_btn_pressed(y, x)
                )
        
        for i in range(len(DISK_ICONS)):
            self.super_frame.disk_count_labels[i].configure(
                textvariable=self.model.disk_counts[i]
            )
        
        self.update()

    # 石を打つときに呼ばれる関数
    def on_btn_pressed(self, y: int, x: int) -> None:
        if self.model.is_placeable(y, x):
            self.model.on_btn_pressed(y, x)
            self.update(y, x)

    def change_player(self) -> None:
        self.model.change_player()
        self.update()
    
    # 表示の更新
    def update(self, hilite_x: int | None=None, hilite_y: int | None=None) -> None:
        # 盤面の更新
        self.update_btns(hilite_x, hilite_y)

        # ゲーム終了判定
        if self.model.is_game_over():
            self.game_over()
            return

        # 矢印の更新
        self.super_frame.arrow_label.pack_forget()
        self.super_frame.arrow_label.configure(text=ARROW_TYPES[self.model.player.get()])
        self.super_frame.arrow_label.pack(
            side=tk.RIGHT if self.model.player.get() == WHITE else tk.LEFT
        )
        
        # パスボタンの更新
        self.super_frame.pass_btn.pack_forget()
        if not self.model.get_placeable_coords():
            self.super_frame.pass_btn.pack()

    def update_btns(self, hilite_y: int | None=None, hilite_x: int | None=None) -> None:
        for y in range(BOARD_LEN):
            for x in range(BOARD_LEN):
                # データとテキストを同期し、配置可能なマスは強調
                self.super_frame.btn_texts[y][x].set(
                    "x" if self.model.is_placeable(y, x)
                    else DISK_ICONS[self.model.board_data[y][x]]
                )
                
                # 引数の座標のマスを強調
                self.super_frame.board_btns[y][x].configure(
                    relief=tk.SOLID if y == hilite_y and x == hilite_x else tk.GROOVE
                )
    
    def game_over(self) -> None:
        self.super_frame.show_game_over_msg()
    
    def reset(self) -> None:
        self.model.reset()
        self.update()