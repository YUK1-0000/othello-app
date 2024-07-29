import tkinter as tk
from .constants import SIDE_LEN, EMPTY, WHITE, BLACK, DISK_TYPES, DIRECTIONS


class Model:
    def __init__(self, root: tk.Tk) -> None:
        self.player = tk.IntVar(value=BLACK)
        self.disk_counts = [tk.IntVar() for _ in range(len(DISK_TYPES))]
        self.board_data = [[EMPTY for _ in range(SIDE_LEN)] for _ in range(SIDE_LEN)]
        self.move_history: list[tuple[int, int] | None] = []
        self.reset()

    def place_disk(self, y: int, x: int, disk_clr: int) -> None:
        self.board_data[y][x] = disk_clr
        self.move_history.append((y, x))
    
    def flip(self, y: int, x: int) -> None:
        # 8方向を探索
        for d in DIRECTIONS:
            
            # 1マス目の探索
            y_, x_ = y+d[0], x+d[1]
            
            if (
                not(0 <= y_ < SIDE_LEN and 0 <= x_ < SIDE_LEN)
                or self.board_data[y_][x_] != self.player.get()*-1
            ):
                continue
            
            # 2マス目以降の探索
            opponent_disk_count = 1
            
            for n in range(1, SIDE_LEN):
                y_, x_ = y+d[0]*n, x+d[1]*n
                
                if not(0 <= y_ < SIDE_LEN and 0 <= x_ < SIDE_LEN):
                    break
                
                sqr_data = self.board_data[y_][x_]
                
                if sqr_data == EMPTY:
                    break # 返せる石が無いのでこの方向の探索をやめる
                
                if sqr_data == self.player.get()*-1:
                    opponent_disk_count += 1
                
                elif sqr_data == self.player.get():
                    # 石を返す
                    for m in range(1, opponent_disk_count):
                        self.board_data[y+d[0]*m][x+d[1]*m] = self.player.get()
                    break

    def change_player(self) -> None:
        self.player.set(self.player.get()*-1)
    
    def update_disk_count(self) -> None:
        [int_var.set(0) for int_var in self.disk_counts]
        for y in range(SIDE_LEN):
            for x in range(SIDE_LEN):
                disk_clr = self.board_data[y][x]
                self.disk_counts[disk_clr].set(self.disk_counts[disk_clr].get()+1)
    
    def reset(self) -> None:
        self.player.set(BLACK)
        self.reset_board_data()
        self.move_history.clear()
        self.update_disk_count()
    
    def reset_board_data(self) -> None:
        for y in range(SIDE_LEN):
            for x in range(SIDE_LEN):
                if x in (SIDE_LEN/2, SIDE_LEN/2-1) and y in (SIDE_LEN/2, SIDE_LEN/2-1):
                    disk_clr = (
                        WHITE
                        if x == y
                        else BLACK
                    )
                else :
                    disk_clr = EMPTY
                self.board_data[y][x] = disk_clr
    
    def get_placeable_coords(self) -> list[tuple[int, int]]:
        return [
            coord for coord in
            [
                (y, x)
                if self.is_placeable(y, x)
                else None
                for x in range(SIDE_LEN)
                for y in range(SIDE_LEN)
            ]
            if coord
        ]
    
    def is_game_over(self) -> bool:
        return self.is_board_full() or self.is_perfect_win()
    
    def is_board_full(self) -> bool:
        return all(all(data) for data in self.board_data)
    
    def is_perfect_win(self) -> bool:
        return not(self.disk_counts[BLACK].get() and self.disk_counts[WHITE].get())
    
    def is_placeable(self, y: int, x: int) -> bool:
        if self.board_data[y][x] != EMPTY:
            return False
        
        # 8方向を探索
        for d in DIRECTIONS:
            # 1マス目の探索
            y_, x_ = y+d[0], x+d[1]
            
            if (
                not (0 <= y_ < SIDE_LEN and 0 <= x_ < SIDE_LEN)
                or self.board_data[y_][x_] != self.player.get()*-1
            ):
                continue
            
            # 2マス目以降の探索
            is_opponent_disk_exist = False
            
            for n in range(1, SIDE_LEN):
                y_, x_ = y+d[0]*n, x+d[1]*n
                
                if (
                    not (0 <= y_ < SIDE_LEN and 0 <= x_ < SIDE_LEN)
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
