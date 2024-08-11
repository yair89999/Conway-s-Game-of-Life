import pygame,os,time,random
from win32api import GetSystemMetrics

screen_width,screen_height = 700,700
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (GetSystemMetrics(0)//2 - screen_width//2,GetSystemMetrics(1)//2-screen_width//2) # place the window in the screen( in this example 300 from the left side of the screen and 50 from the top of the screen)
pygame.init()

window = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("The Game Of Life")
font = pygame.font.SysFont('', 30)

class Mechanics:
    def __init__(self):
        self.board = []
        self.generations = 0
        board_size = 35
        for i in range(board_size):
            self.board.append([])
            for j in range(board_size):
                self.board[-1].append(0)

        for i in range(100):
            self.board[random.randint(0,len(self.board)-1)][random.randint(0,len(self.board)-1)] = 1

    def draw(self, mouse_pos, mouse_buttons):
        num_of_rows_and_columns = len(self.board)
        space_between_lines = screen_width//num_of_rows_and_columns
        for x in range(0,screen_width, space_between_lines):
            pygame.draw.line(window, (100,100,100), (x,0), (x,screen_height))
        for y in range(0,screen_height, space_between_lines):
            pygame.draw.line(window, (100,100,100), (0,y), (screen_width,y))
        
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 1:
                    pygame.draw.rect(window, (255,255,255), [space_between_lines*i, space_between_lines*j, space_between_lines, space_between_lines])
        if mouse_buttons[0] == True:
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    rect = pygame.Rect(space_between_lines*i, space_between_lines*j, space_between_lines, space_between_lines)
                    if rect.collidepoint(mouse_pos):
                        self.board[i][j] = 1
        
        window.blit(font.render("Generations:"+str(self.generations),True, (255,255,255)), (10,10))
        num_living_cells = 0
        for row in self.board:
            for cell in row:
                if cell == 1:
                    num_living_cells += 1
        window.blit(font.render("Num Of Living Cells:"+str(num_living_cells),True, (255,255,255)), (10,10 + font.size("A")[1]*1.2))


    def handle_laws(self):
        """
        the laws:
        1. if a cell has less than 2 living neighbours he dies
        Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        2. if a cell has 2 or 3 living neighbours he continue living
        Any live cell with two or three live neighbours lives on to the next generation.
        3. if a cell has more than 3 living neighbours he dies
        Any live cell with more than three live neighbours dies, as if by overpopulation.
        4. if a dead cell has exactly 3 living neighbours he comes to life
        Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        """
        
        new_board = []
        for row in self.board:
            new_board.append(row.copy())
        for i in range(len(self.board)): # row
            for j in range(len(self.board[0])): # column
                num_of_living_neighbours = 0
                neighbours_positions = [
                    (i-1,j-1),(i-1,j),(i-1,j+1),
                    (i,j-1),     (i,j+1),
                    (i+1,j-1),(i+1,j),(i+1,j+1)
                ]
                for pos in neighbours_positions:
                    try:
                        if self.board[pos[0]][pos[1]] == 1:
                            num_of_living_neighbours += 1
                    except:
                        pass
                if self.board[i][j] == 1:
                    if num_of_living_neighbours < 2: # dies
                        new_board[i][j] = 0
                    elif num_of_living_neighbours > 3: # dies
                        new_board[i][j] = 0
                else:
                    if num_of_living_neighbours == 3:
                        new_board[i][j] = 1
        self.board = []
        for row in new_board:
            self.board.append(row)
        self.generations += 1
                
def main():
    game_on = True
    clock = pygame.time.Clock()

    game_mechanics = Mechanics()

    t = time.time()+0.2
    while game_on:
        clock.tick(60)
        window.fill((0,0,0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_on = False

        game_mechanics.draw(mouse_pos, mouse_button)
        if t <= time.time():
            game_mechanics.handle_laws()
            t = time.time()+0.2

        pygame.display.update()
if __name__ == '__main__':
    main()