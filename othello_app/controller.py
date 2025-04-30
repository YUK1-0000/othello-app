import tkinter as tk
from othello_app import Model, SuperFrame, MenuBar
from .constants import PLACEABLE_TXT, SIDE_LEN, BLACK, DISK_TYPES, ARROW_TYPES


class Controller:
    def __init__(self, root: tk.Tk) -> None:
        self.model = Model(root)
        self.super_frame = SuperFrame(root)
        self.menu_bar = MenuBar(
            root,
            reset_cmd=self.reset,
            undo_move_cmd=self.undo_move
        )
        
        # ボタンにコマンドとテキストの変数を設定
        self.super_frame.pass_btn.configure(command=self.on_pass_btn_pressed)
        for y in range(SIDE_LEN):
            for x in range(SIDE_LEN):
                self.super_frame.board_btns[y][x].configure(
                    textvariable=self.super_frame.btn_texts[y][x],
                    command=lambda y=y, x=x: self.on_btn_pressed(y, x)
                )
        
        for disk_type in range(len(DISK_TYPES)):
            self.super_frame.disk_count_lbls[disk_type].configure(
                textvariable=self.model.disk_counts[disk_type]
            )
        
        self.reset()

    # 石を打つときに呼ばれる関数
    def on_btn_pressed(self, y: int, x: int) -> None:
        if not self.model.is_placeable(y, x):
            return
        
        self.model.place_disk(y, x)
        self.model.flip(y, x)
        self.model.change_player()
        
        self.update(hilite_coord=(y, x))
        
        if self.model.is_game_over():
            self.game_over()

    def on_pass_btn_pressed(self) -> None:
        self.model.move_history.append(None)
        self.model.change_player()
        self.update()
    
    def update(self, *, hilite_coord: tuple[int, int] | None=None) -> None:
        self.model.update_disk_count()
        self.update_lbls()
        self.update_btns(hilite_coord=hilite_coord)
    
    def update_btns(self, *, hilite_coord: tuple[int, int] | None=None) -> None:
        for y in range(SIDE_LEN):
            for x in range(SIDE_LEN):
                # データとテキストを同期し、配置可能なマスは強調
                self.super_frame.btn_texts[y][x].set(
                    PLACEABLE_TXT
                    if self.model.is_placeable(y, x)
                    else DISK_TYPES[self.model.board_data[y][x]]
                )
                
                # 引数の座標のマスの枠を強調
                self.super_frame.board_btns[y][x].configure(
                    relief=tk.SOLID
                    if (y, x) == hilite_coord
                    else tk.GROOVE
                )
        
        self.super_frame.pass_btn.pack_forget()
        if not self.model.get_placeable_coords():
            self.super_frame.pass_btn.pack()
    
    def update_lbls(self) -> None:
        self.super_frame.arrow_lbl.pack_forget()
        self.super_frame.arrow_lbl.configure(
            text=ARROW_TYPES[self.model.player.get()]
        )
        self.super_frame.arrow_lbl.pack(
            side=(
                tk.LEFT
                if self.model.player.get() == BLACK
                else tk.RIGHT
            )
        )
    
    def undo_move(self) -> None:
        move_hist = self.model.move_history[:-1]
        self.reset()
        
        if not len(move_hist):
            return
        
        for move in move_hist:
            if move:
                self.model.place_disk(*move)
                self.model.flip(*move)
            self.model.change_player()
        self.update(hilite_coord=(move))
    
    def game_over(self) -> None:
        self.super_frame.game_over()
    
    def reset(self) -> None:
        self.model.reset()
        self.super_frame.reset()
        self.update()