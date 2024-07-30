import tkinter as tk
from typing import Callable
from .constants import (
    BLACK,
    EMPTY,
    TITLE,
    WHITE,
    WINDOW_SIZE,
    FONT,
    FONT_SIZES,
    PLACEABLE_TXT,
    GAME_OVER_MSG,
    PASS_BTN_MSG,
    SIDE_LEN,
    DISK_TYPES,
    ARROW_TYPES,
    SQR_BTN_W,
    SQR_BTN_H,
)


class SuperFrame(tk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        root.title(TITLE)
        root.geometry(WINDOW_SIZE)
        root.resizable(width=False, height=False)
        
        self.btn_texts = [
            [
                tk.StringVar()
                for _ in range(SIDE_LEN)
            ]
            for _ in range(SIDE_LEN)
        ]
        
        # 盤面
        self.board_frame = tk.Frame(self)
        
        self.board_btns = [
            [
                tk.Button(
                    self.board_frame,
                    width=SQR_BTN_W,
                    height=SQR_BTN_H,
                    font=(FONT, FONT_SIZES["m"]),
                    textvariable=self.btn_texts[y][x]
                )
                for x in range(SIDE_LEN)
            ]
            for y in range(SIDE_LEN)
        ]
        
        self.board_frame.pack()
        
        for y in range(SIDE_LEN):
            for x in range(SIDE_LEN):
                self.board_btns[y][x].grid(column=x, row=y)

        # 画面下側
        self.bottom_frame = tk.Frame(self)
        
        self.pass_btn = tk.Button(
            self.bottom_frame,
            font=(FONT, FONT_SIZES["l"]),
            text=PASS_BTN_MSG
        )
        
        self.arrow_lbl = tk.Label(self.bottom_frame, font=(FONT, FONT_SIZES["l"]))
        self.game_over_lbl = tk.Label(
            self.bottom_frame,
            text=GAME_OVER_MSG,
            font=(FONT, FONT_SIZES["l"])
        )
        self.disk_lbls = [
            tk.Label(
                self.bottom_frame,
                font=(FONT, FONT_SIZES["l"]),
                textvariable=tk.StringVar(value=DISK_TYPES[disk_clr])
            )
            for disk_clr in range(len(DISK_TYPES))
        ]
        self.disk_count_lbls = [
            tk.Label(
                self.bottom_frame,
                font=(FONT, FONT_SIZES["l"]),
            )
            for _ in range(len(DISK_TYPES))
        ]

        self.bottom_frame.pack(fill=tk.BOTH)
        
        for disk_clr in BLACK, WHITE:
            s = tk.LEFT if disk_clr == BLACK else tk.RIGHT
            self.disk_count_lbls[disk_clr].pack(side=s)
            self.disk_lbls[disk_clr].pack(side=s)
        
        self.pack()

    def show_pass_btn(self) -> None:
        self.pass_btn.pack()
    
    def game_over(self) -> None:
        self.arrow_lbl.pack_forget()
        self.pass_btn.pack_forget()
        self.game_over_lbl.pack()
    
    def reset(self) -> None:
        self.arrow_lbl.pack_forget()
        self.pass_btn.pack_forget()
        self.game_over_lbl.pack_forget()


class MenuBar(tk.Menu):
    def __init__(
        self,
        root: tk.Tk,
        *,
        reset_cmd: Callable,
        undo_move_cmd: Callable
    ) -> None:
        
        super().__init__(root)
        root.config(menu=self)
        
        self.menu = tk.Menu(self, tearoff=False)
        
        self.add_cascade(label="Menu", menu=self.menu)
        self.menu.add_command(label="Reset Game", command=reset_cmd)
        self.menu.add_command(label="Undo a move", command=undo_move_cmd)