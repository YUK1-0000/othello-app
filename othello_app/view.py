import tkinter as tk
from .constants import (
    BLACK,
    EMPTY,
    TITLE,
    WHITE,
    WINDOW_SIZE,
    FONT,
    FONT_SIZES,
    HILITE_CLR,
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
        
        self.btn_texts = [[tk.StringVar() for _ in range(SIDE_LEN)] for _ in range(SIDE_LEN)]
        
        # 盤面
        self.board_frame = tk.Frame(self)
        
        self.board_btns = [
            [
                tk.Button(
                    self.board_frame,
                    width=SQR_BTN_W,
                    height=SQR_BTN_H,
                    font=(FONT, FONT_SIZES["m"]),
                    textvariable=self.btn_texts[y][x],
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
        
        self.arrow_label = tk.Label(self.bottom_frame, font=(FONT, FONT_SIZES["l"]))
        self.game_over_label = tk.Label(
            self.bottom_frame,
            text=GAME_OVER_MSG,
            font=(FONT, FONT_SIZES["l"])
        )
        self.disk_labels = [
            tk.Label(
                self.bottom_frame,
                font=(FONT, FONT_SIZES["l"]),
                textvariable=tk.StringVar(value=DISK_TYPES[type_])
            )
            for type_ in range(len(DISK_TYPES))
        ]
        self.disk_count_labels = [
            tk.Label(
                self.bottom_frame,
                font=(FONT, FONT_SIZES["l"]),
            )
            for _ in range(len(DISK_TYPES))
        ]

        self.bottom_frame.pack(fill=tk.BOTH)
        
        for type_ in BLACK, WHITE:
            s = tk.LEFT if type_ == BLACK else tk.RIGHT
            self.disk_count_labels[type_].pack(side=s)
            self.disk_labels[type_].pack(side=s)
        
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
