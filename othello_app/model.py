import tkinter as tk


BOARD_LEN = 8
DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
)
EMPTY, WHITE, BLACK = 0, 1, -1
DISK_ICONS = ("", "○", "●")

class Model:
    def __init__(self, root: tk.Tk) -> None:
        self.player = tk.IntVar(value=BLACK)
        self.disk_counts = [tk.IntVar() for _ in range(len(DISK_ICONS))]
        self.board_data = [[EMPTY for _ in range(BOARD_LEN)] for _ in range(BOARD_LEN)]
        self.reset()
    
    def on_btn_pressed(self, y: int, x: int) -> None:
        self.place_disk(y, x, self.player.get())
        self.flip(y, x)
        self.count_disk()
        self.turn_end()
    
    def place_disk(self, y: int, x: int, disk_type: int) -> None:
        self.board_data[y][x] = disk_type
    
    def flip(self, y: int, x: int) -> None:
        # 8方向を探索
        for d in DIRECTIONS:
            
            # 1マス目の探索
            y_, x_ = y+d[0], x+d[1]
            
            if (
                not(0 <= y_ < BOARD_LEN and 0 <= x_ < BOARD_LEN)
                or self.board_data[y_][x_] != self.player.get()*-1
            ):
                continue
            
            # 2マス目以降の探索
            opponent_disk_count = 1
            
            for n in range(1, BOARD_LEN):
                y_, x_ = y+d[0]*n, x+d[1]*n
                
                if not(0 <= y_ < BOARD_LEN and 0 <= x_ < BOARD_LEN):
                    break
                
                sqr_data = self.board_data[y_][x_]
                
                if sqr_data == EMPTY:
                    break # 返せる石が無いのでこの方向の探索をやめる
                
                if sqr_data == self.player.get()*-1:
                    opponent_disk_count += 1
                
                elif sqr_data == self.player.get():
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
        for y in range(BOARD_LEN):
            for x in range(BOARD_LEN):
                disk_type = self.board_data[y][x]
                self.disk_counts[disk_type].set(self.disk_counts[disk_type].get()+1)
    
    def reset(self) -> None:
        self.player.set(BLACK)
        self.reset_board_data()
        self.count_disk()
    
    def reset_board_data(self) -> None:
        for y in range(BOARD_LEN):
            for x in range(BOARD_LEN):
                if x in (BOARD_LEN/2, BOARD_LEN/2-1) and y in (BOARD_LEN/2, BOARD_LEN/2-1):
                    disk_type = WHITE if x == y else BLACK
                else :
                    disk_type = EMPTY
                self.place_disk(y, x, disk_type)
    
    def get_placeable_coords(self) -> list[list[int]]:
        return[
            i for i in
            [
                [y, x] if self.is_placeable(y, x) else None
                for x in range(BOARD_LEN)
                for y in range(BOARD_LEN)
            ]
            if i
        ]
    
    def is_game_over(self) -> bool:
        return self.is_board_filled() or self.is_perfect_win()
    
    def is_board_filled(self) -> bool:
        return all(all(data) for data in self.board_data)
    
    def is_perfect_win(self) -> bool:
        return not (self.disk_counts[BLACK].get() and self.disk_counts[WHITE].get())
    
    def is_placeable(self, y: int, x: int) -> bool:
        if self.board_data[y][x] != EMPTY:
            return False
        
        # 8方向を探索
        for d in DIRECTIONS:
            # 1マス目の探索
            y_, x_ = y+d[0], x+d[1]
            
            if (
                not (0 <= y_ < BOARD_LEN and 0 <= x_ < BOARD_LEN)
                or self.board_data[y_][x_] != self.player.get()*-1
            ):
                continue
            
            # 2マス目以降の探索
            is_opponent_disk_exist = False
            
            for n in range(1, BOARD_LEN):
                y_, x_ = y+d[0]*n, x+d[1]*n
                
                if (
                    not (0 <= y_ < BOARD_LEN and 0 <= x_ < BOARD_LEN)
                    or self.board_data[y_][x_] == EMPTY
                ):
                    break
                
                sqr_data = self.board_data[y_][x_]
                
                if sqr_data == EMPTY:
                    break
                
                if sqr_data == self.player.get()*-1:
                    is_opponent_disk_exist = True
                
                elif sqr_data == self.player.get() and is_opponent_disk_exist:
                    return True
    
        return False
