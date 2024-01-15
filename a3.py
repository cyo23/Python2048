import tkinter as tk

# You may import any submodules of tkinter here if you wish
# You may also import anything from the typing module
# All other additional imports will result in a deduction of up to 100% of your A3 mark

from a3_support import *

# Write your classes here

class Model:
    '''Data of 2048'''
    def __init__(self) -> None:
        self._size = NUM_COLS
        self.size = 4
	
        self._cells = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
        self._win = False
	
        self._compressed = False
        self._merged = False
        self.moved = False
	
        self._current_score = 0

    def new_game(self) -> None:
        self._current_score = 0
        self._cells = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
        

    def get_tiles(self):
        return self._cells
        

    def add_tile(self) -> None:
        
        cell = generate_tile(self._cells)
        i = cell[0][0]
        j = cell[0][1]
        print(cell)
        self._cells[i][j] = cell[1]

    def move_left(self) -> None:
	
        self._cells = stack_left(self._cells)
        self._cells = combine_left(self._cells)[0]
        self._cells = stack_left(self._cells)
	

    def move_right(self) -> None:
        self._cells = reverse(self._cells)
        self._cells = stack_left(self._cells)
        self._cells = combine_left(self._cells)[0]
	
        self._moved = self._compressed or self._merged
	
        self._cells = stack_left(self._cells)	
        self._cells = reverse(self._cells)

    def move_up(self) -> None:
        self._cells = transpose(self._cells)
        self._cells = stack_left(self._cells)
        self._cells = combine_left(self._cells)[0]
	
        self._moved = self._compressed or self._merged
	
        self._cells = stack_left(self._cells)
        self._cells = transpose(self._cells)

    def move_down(self) -> None:
        self._cells = transpose(self._cells)
        self._cells = reverse(self._cells)
        self._cells = stack_left(self._cells)
        self._cells = combine_left(self._cells)[0]
	
        self._moved = self._compressed or self._merged
	
        self._cells = combine_left(self._cells)[0]	
        self._cells = reverse(self._cells)
        self._cells = transpose(self._cells)
	
        """
        self._cells = stack_left(self._cells)
        self._cells = combine_left(self._cells)
        self._cells = stack_left(self._cells)
        self._cells = reverse(self._cells)
        self._cells = transpose(self._cells)
        """

    def attempt_move(self, move: str) -> bool:
        self._compressed = False
        self._merged = False
        self._moved = False

    def has_won(self) -> bool:
        for i in range(NUM_COLS):
            for i in range(NUM_ROWS):
                if self._cells[i][j] >= 2048:
                    return True
        return False

    def has_lost(self) -> bool:
        for i in range(NUM_COLS):
            for i in range(NUM_ROWS):
                if self._cells[i][j] == 0:
                    return False
        return True
    
    def has_empty_cells(self):
        for i in range(self.size):
            for j in range(self.size):
                if self._cells[i][j] == 0:
                    return True
        return False
    
    def can_merge(self):
        for i in range(self.size):
            for j in range(self.size - 1):
                if self._cells[i][j] == self._cells[i][j + 1]:
                    return True
        for j in range(self.size):
            for i in range(self.size - 1):
                if self._cells[i][j] == self._cells[i + 1][j]:
                    return True
        return False

    def set_cells(self, cells):
        self.cells = cells
    

class GameGrid:

    def __init__(self, master: tk.Tk, **kwargs) -> None:
        self.root = tk.Tk()
	
        self.grid = master
        self.root.title('CSSE1001/7030 2022 Semester 2 A3')
        self.root.resizable(False, False)
        self.size = 4
	

        self.background = tk.Frame(self.root, bg=BACKGROUND_COLOUR)
        self.cell_labels = []

	#bbox
        for i in range(4):
            row_labels = []
            for j in range(4):
                label = tk.Label(self.background, text='',
		                 bg=COLOURS[None],
		                 justify=tk.CENTER, font=TILE_FONT,
		                 width=4, height=2)
                label.grid(row=i, column=j, padx=10, pady=10)
                row_labels.append(label)
            self.cell_labels.append(row_labels)
	#bbox
	    
        self.background.pack(side=tk.TOP)

    
    def drawing(self):

        for i in range(4):
            for j in range(self.size):
                if self.grid._cells[i][j] == None:
                    self.cell_labels[i][j].configure(
		         text='',
		         bg=COLOURS[None])
                else:
                    cell_text = int(self.grid._cells[i][j])
                    if self.grid._cells[i][j] != None:
                        bg_color = COLOURS.get(cell_text)
                        fg_color = FG_COLOURS.get(cell_text)
                    self.cell_labels[i][j].configure(
			text=cell_text,
			bg=bg_color, fg=fg_color)
                    # self.grid._cells[i][j] > 2048:
                    #    bg_color = COLOURS[None].get('beyond')
                    #    fg_color = FG_COLOURS.get('beyond')

    
    
    def _get_midpoint(self, position: tuple[int, int]) -> tuple[int, int]:
        """Return the graphics coordinates for the center of the cell at the given (row, col) position."""
        pass    
    
    def clear(self) -> None:
        """Clear all items"""
        pass   
    
    #def redraw(self, tiles: list[list[Optional[int]]]) -> None:
        """Clears and redraws the entire grid based on the given tiles."""
    #    pass     


class Game:
    """You must implement a class for the controller, called Game. 
    This class should be instantiated in your main function 
    to cause the game to be created and run.
     maintaining the model and view classes, binding some event handlers
     and facilitating communication between model and view classes"""
    
    
    def __init__(self, master) -> None:
        """create a Model instance, set the window title, create the title label and create instances of any view classes packed into master. It should also bind key press events to an appropriate handler, and cause the initial GUI to be drawn."""
        self.start_cells_num = 2
	
        self.grid = master
        self.panel = GameGrid(self.grid)
        self.over = False
        self.won = False
        self.keep_playing = False

    def is_game_terminated(self):
        return self.over or (self.won and (not self.keep_playing))    
    
    
    def draw(self) -> None:
        """Redraws any view classes based on the current model state"""
        """需要把model和gui里的内容进行统合"""
        pass
    
    def attempt_move(self, event: tk.Event) -> None:
        """Attempt a move if the event represents a key press on character ‘a’, ‘w’, ‘s’, or ‘d’. """
        key_value = event.keysym
        if key_value in UP: #==
            self.grid.move_up()
            self.grid.add_tile()
        elif key_value in LEFT:
            self.grid.move_left()
            self.grid.add_tile()
        elif key_value in DOWN:
            self.grid.move_down()
            self.grid.add_tile()
        elif key_value in RIGHT:
            self.grid.move_right()
            self.grid.add_tile()
        else:
            pass
        self.panel.drawing()
	
	
        if self.grid.moved:
            self.grid.add_tiles()

        self.panel.drawing()
        if not self.can_move():
            self.over = True
            self.game_over()	
    
    def new_tile(self) -> None:
        """Adds a new tile to the model and redraws.  """

        for i in range(self.start_cells_num):
            self.grid.add_tile()

	
    def start(self):
        self.add_start_cells()
        self.panel.drawing()
        self.panel.root.bind('<Key>', self.attempt_move)
        self.panel.root.mainloop()

    def add_start_cells(self):
        for i in range(self.start_cells_num):
            self.grid.add_tile()   
	    
    def can_move(self):
        return self.grid.has_empty_cells() or self.grid.can_merge()
    
def play_game(root):
	# Add a docstring and type hints to this function
	# Then write your code here
    #grid = Model()
    #panel = GameGrid(grid)
    #game2048 = Game(panel)
    
    #panel.root.mainloop()
    #return game2048
    pass



if __name__ == '__main__':
    grid = Model()

    game2048 = Game(grid)
    game2048.start()
