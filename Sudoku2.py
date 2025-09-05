import pygame as pg                                              #import pg library, *USED SHORTHAND FOR EFFICIENCY*
import sys                                                       #import system library
from Constants import *                                          #import all variables from 'Constants.py'
import random                                                    #import random library

pg.font.init()                                                   #initialising num_font
num_font = pg.font.SysFont('Helvetica.ttf', 40)
op_font = pg.font.SysFont('simsum', 30)
but_font = pg.font.SysFont('simsum', 25)

WIDTH, HEIGHT = 1000, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))                    #setting display size
pg.display.set_caption('Sudoku')                                 #set program caption
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)                                        #set program icon

pg.display.init()
lmaccess = pg.image.load('LightModeAccess.png').convert_alpha()
lmaccess = pg.transform.scale(lmaccess, (30,30))
lmerase = pg.image.load('LightModeErase.png').convert_alpha()
lmerase = pg.transform.scale(lmerase, (30,30))
lmsud = pg.image.load('LightModeNew.png').convert_alpha()
lmsud = pg.transform.scale(lmsud, (30,30))

run = True                                                       #arbitrary variable to set running state
play_area = pg.Rect(440, 53, 495, 495)                           #defines what area user can interact with (whole grid)

grid = [['' for _ in range(9)] for _ in range(9)]                #creates empty 9x9 2d array for tracking inputs

cells = [[None for _ in range(9)] for _ in range(9)]             #creates empty 9x9 2d array for tracking rects within cells

for row in range(9):
    for col in range(9):
        x = 440 + col * 55                                       #each collumn is incremented by 55 pixels (size of one cell)
        y = 52 + row * 55                                        #each row is incremented by 55 pixels
        cells[row][col] = pg.Rect(x, y, 55, 55)                  #defines rect for each cell using values in array

selected_cell = None                                             #initialises selected cell variable, indicates no selection

def draw_grid():                                                                              #same as set_screen(), without background
    for x in range(1, 10):
        pg.draw.line(screen, Grey, ((440+x*55), 545), ((440+x*55), 53), width=1)
        pg.draw.line(screen, Grey, (440, (51+x*55)), (934, (51+x*55)), width=1)
    pg.draw.rect(screen, 'black', pg.Rect(440, 53, 495, 495), width=3)
    for x in range(1, 3):
        pg.draw.line(screen, 'black', ((440+x*165), 545), ((440+x*165), 53), width=2)
        pg.draw.line(screen, 'black', (440, (51+x*165)), (934, (51+x*165)), width=2)

def draw_numbers():                                                       #displays inputted numbers on screen in grid
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:                                             #only blits number if index is not empty
                rect = cells[row][col]                                          #fetches necessary rect from 'cells' array
                text = num_font.render(str(grid[row][col]), True, 'black')      #converts int to string for blit
                text_rect = text.get_rect(center=rect.center)                   #creates rectangle around text and centres within selected cell's rect 
                screen.blit(text, text_rect)                                    #blits number as string into center of rect

def draw_highlight():                           #function for highlighting selected cell
    if selected_cell:                           #if selected_cell == True
        row, col = selected_cell                #defines row and column as tuple of selected cell
        rect = cells[row][col]                  #finds rect at row and col of cells array
        pg.draw.rect(screen, Grey, rect)        #draws grey square at rect

def get_selected_cell(pos):                                      #find position of selected cell
    for row in range(9):
        for col in range(9):
            if cells[row][col].collidepoint(pos):                #if mouse cursor collides with rect at specified row and column
                return row, col                                  #return row and column to be used in draw_highlight
    return None                                                  #if no cell selected then return nothing

class Button:                                                                                                                       #creating class 'Button'
    def __init__(self, x, y, w, h, text, font, bg_color, text_color, value=None, hover_color=None, label_pos=None):                 #initialising class and specifying parameters
        self.rect = pg.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.bg_color = bg_color                                                                                                    #background colour of button
        self.text_color = text_color
        self.value = value                                                                                                          #assigns numerical value to each button
        self.hover_color = hover_color if hover_color else bg_color                                                                 #button changes colour when hovered, else no change
        self.label_pos = label_pos                                                                                                  #changes position of text within button

    def draw(self, screen):                                                                                                         #function to draw button on screen
        mouse_pos = pg.mouse.get_pos()                                                                                              #retrieves mouse position every iteration
        if self.rect.collidepoint(mouse_pos):                                                                                       #detects if mouse position collides with button
            pg.draw.rect(screen, self.hover_color, self.rect, border_radius=10)                                                     #changes colour if detected
        else:
            pg.draw.rect(screen, self.bg_color, self.rect, border_radius=10)                                                        #remains same if not

        pg.draw.rect(screen, "black", self.rect, 2, border_radius=10)                                                               #creates rounded edges of button

        text_surface = self.font.render(self.text, True, self.text_color)                                                           
        text_rect = text_surface.get_rect(center=self.rect.center)

        if self.label_pos == "center":                                                                                              #option to center text in button
            text_rect.center = self.rect.center
        elif self.label_pos == "left":                                                                                              #option to align text to left in button
            text_rect.midleft = (self.rect.left + 18, self.rect.centery)
        
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):                                                                                                    #function to detect mouse clicks
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
def draw_text(text, font, text_col, x, y):                                                                                          #function to easily display text on screen
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

one = Button(100, 160, 60, 60, '1', num_font, 'white', 'black', 1, hover_color = Grey)                                              #creating number buttons
two = Button(180, 160, 60, 60, '2', num_font, 'white', 'black', 2, hover_color = Grey)
three = Button(260, 160, 60, 60, '3', num_font, 'white', 'black', 3, hover_color = Grey)
four = Button(100, 240, 60, 60, '4', num_font, 'white', 'black', 4, hover_color = Grey)
five = Button(180, 240, 60, 60, '5', num_font, 'white', 'black', 5, hover_color = Grey)
six = Button(260, 240, 60, 60, '6', num_font, 'white', 'black', 6, hover_color = Grey)
seven = Button(100, 320, 60, 60, '7', num_font, 'white', 'black', 7, hover_color = Grey)
eight = Button(180, 320, 60, 60, '8', num_font, 'white', 'black', 8, hover_color = Grey)
nine = Button(260, 320, 60, 60, '9', num_font, 'white', 'black', 9, hover_color = Grey)
access = Button(20, 20, 200, 40, 'Accessibility', op_font, 'white', 'black', hover_color = Grey, label_pos = 'left')                #creating function buttons
clear = Button(240, 20, 100, 40, 'Clear', op_font, 'white', 'black', hover_color = Grey)
erase = Button(100, 400, 60, 60, '', num_font, Blue, 'black', 0, hover_color = Grey)
new = Button(260, 400, 60, 60, '', num_font, Blue, 'black', 0, hover_color = Grey)


def generate(board):                                                         #generating random valid board with shuffled numbers
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:                                         #only fills cell if cell empty
                    numbers = [1,2,3,4,5,6,7,8,9]
                    random.shuffle(numbers)                                  #shuffles list to ensure 'randomness'
                    for number in numbers:
                        if valid(board, number, row, col):                   #only fills cell if number is valid
                            board[row][col] = number
                            if generate(board):
                                return True
                            else:
                                board[row][col] = 0
                    return False                                             #returns False if cell not empty
    return True                                                              #returns True when board is generated

def valid(board, number, row, col):
    if number in board[row] == True:                                         #returns False if same number found in same row 
        return False
    elif number in [board[x][col] for x in range(9)]:                        #returns False if same number found in same column
        return False
    startrow = 0
    startcol = 0
    startrow, startcol = (3*(row//3)), (3*(col//3))                          #defines the first row/first column in each 3x3 box within grid
    for c in range(startcol, startcol + 3):                                  #searches each column in 3x3 box
        for r in range(startrow, startrow+3):                                #searches each row in 3x3 box
            if board[r][c] == number:                                        #detects if number is found multiple times in same box
                return False                                                
    return True                                                              #if valid, return True

def board_setup():                                                           #creates array and fills with numbers from generate() function
    board = [[0 for _ in range(9)] for _ in range(9)]
    generate(board)
    return board

def solutions(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                sol = 0                                                                         #count variable for number of solutions
                for number in range(1,10):
                    if valid(board, number, row, col):                                          #if valid, fill number in cell
                        board[row][col] = number
                        sol = sol + solutions(board)
                        board[row][col] = 0
                        if 1 < sol: 
                            return sol                                                          #breaks loop and returns amount of solutions
                return sol
    return 1                                                                                    #returns '1' to indicate 1 unique solution found

def partial_board(board, cells=40):                                                             #function to create puzzle by removing certain cells
    while cells > 0:
        row = random.randint(0, 8)                                                              #choose random row
        col = random.randint(0, 8)                                                              #choose random function
        if board[row][col] != 0:                                                                #only acts if cell contains number
            board[row][col] = 0                                                                 #delete number from cell
            cells = cells - 1
        else:
            continue                                                                            #if cell is empty, choose another
    return board                                                                                #return new board with deleted cells

complete_board = board_setup()
grid = partial_board(complete_board, cells=40)                                                  #transfers puzzle to 'grid' variable, so user can interact while program runs

screen.fill(LightMode)                                                                          #fill background with pre-defined colour
while run:                                                                                      #only iterates while running
    pos = pg.mouse.get_pos()                                                                    #get mouse position on screen
    for event in pg.event.get():                                                    
        if event.type == pg.QUIT:                                                               #if user quits, end program
            run = False
            pg.quit()
            sys.exit()

        elif event.type == pg.MOUSEBUTTONDOWN and play_area.collidepoint(pos):                  #if user clicks while on grid then retrive row and col
            selected_cell = get_selected_cell(pos)

        elif event.type == pg.KEYDOWN and event.unicode.isdigit() and selected_cell:            #detects if user inputs number
            row, col = selected_cell                                                            
            grid[row][col] = int(event.unicode)                                                 #event.unicode represents inputted number, stores in grid array 

        for button in [one, two, three, four, five, six, seven, eight, nine]:
            if button.is_clicked(event) and selected_cell:
                row, col = selected_cell
                grid[row][col] = int(button.text)
        
        if access.is_clicked(event) and selected_cell:
            row, col = selected_cell
            grid[row][col] = int(button.text)
        
        if clear.is_clicked(event) and selected_cell:
            grid = [['' for _ in range(9)] for _ in range(9)] 
            screen.fill(LightMode)
            draw_grid

    print(grid)
    pg.draw.rect(screen, LightMode, pg.Rect(440, 53, 495, 495))                                 #redraws background of grid for each frame/iteration                                        
    draw_highlight()                                                                            
    draw_grid()                                                                                 #redraws grid separately from background so overlay highlighted cells
    draw_numbers()
    pg.draw.rect(screen, LightMode, pg.Rect(100, 469, 60, 50))
    draw_text('Erase', but_font, 'black', 106, 470)
    pg.draw.rect(screen, LightMode, pg.Rect(270, 469, 60, 50))
    draw_text('New', but_font, 'black', 273, 468) 
    pg.draw.rect(screen, LightMode, pg.Rect(750, 0, 200, 50))
    draw_text('Accessible Sudoku', op_font, 'black', 750, 20) 
    one.draw(screen)          
    two.draw(screen)          
    three.draw(screen) 
    four.draw(screen)
    five.draw(screen)
    six.draw(screen)
    seven.draw(screen)
    eight.draw(screen)
    nine.draw(screen)
    erase.draw(screen)
    pg.Surface.blit(screen, lmerase, (114,413)) 
    new.draw(screen) 
    pg.Surface.blit(screen, lmsud, (275, 414))
    access.draw(screen) 
    pg.Surface.blit(screen, lmaccess, (180,24))
    clear.draw(screen)                                 
    pg.display.flip()                                                                           #updates display


pg.quit()                                                                                       #quits game
