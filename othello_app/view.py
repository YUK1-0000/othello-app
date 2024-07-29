import tkinter as tk


BOARD_LEN = 8
TITLE = "Othello App"
WINDOW_SIZE = "360x340"
FONT = ""
FONT_SIZES = {
    "m": 16,
    "l": 24
}
SQR_BTN_W, SQR_BTN_H = 3, 1
DISK_ICONS = ("", "○", "●")
ARROW_TYPES = ("", "->", "<-")
HILITE_CLR = "#ff4c4c"
PASS_BTN_MSG = "Pass"
GAME_OVER_MSG = "GAME OVER!"


class SuperFrame(tk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        root.title(TITLE)
        root.geometry(WINDOW_SIZE)
        root.resizable(width=False, height=False)
        
        self.btn_texts = [[tk.StringVar() for _ in range(BOARD_LEN)] for _ in range(BOARD_LEN)]
        
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
                for x in range(BOARD_LEN)
            ]
            for y in range(BOARD_LEN)
        ]
        
        self.board_frame.pack()
        
        for y in range(BOARD_LEN):
            for x in range(BOARD_LEN):
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
                textvariable=tk.StringVar(value=DISK_ICONS[type_])
            )
            for type_ in range(len(DISK_ICONS))
        ]
        self.disk_count_labels = [
            tk.Label(
                self.bottom_frame,
                font=(FONT, FONT_SIZES["l"]),
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
