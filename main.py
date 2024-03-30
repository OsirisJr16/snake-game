import numpy as np 
import pygame

Block_size =  20 
height , width = 480 , 640

board_w , board_h  = int(width/Block_size), int(height/Block_size)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Snake: 
    def __init__(self) -> None:
        self.direction = np.array([0,0])
        self.position = np.array([[board_w//2 , board_h//2]])
        self.taille = 1  
    
    def move(self) : 
        self.position[1:] = self.position[:-1] 
        self.position[0] += self.direction
   
    def setDirection(self ,direction) :
        if direction == 'UP' :
            self.direction = np.array([0 , -1])
        elif direction =='DOWN' : 
            self.direction = np.array([0, 1])
        elif direction == "LEFT" :
            self.direction = np.array([-1 , 0])
        elif direction =="RIGHT" :
            self.direction = np.array([1 , 0]) 

class Game: 
    def __init__(self) -> None:
        self.board = np.zeros((board_w , board_h))
        self.snake = Snake() 
        self.score = 0 
        self.food = None 
        self.generateFood() 
        self.game_over = False
    
    def generateFood(self):
        while True:
            foodPos = np.random.randint(0, board_w - 1), np.random.randint(0, board_h - 1)
            if self.board[foodPos[0], foodPos[1]] == 0:
                self.food = foodPos
                break
    
    def CheckCollision(self):
        head = self.snake.position[0]
        head_rect = pygame.Rect(head[0] * Block_size, head[1] * Block_size, Block_size, Block_size)
        for pos in self.snake.position[1:]:
            pos_rect = pygame.Rect(pos[0] * Block_size, pos[1] * Block_size, Block_size, Block_size)
            if head_rect.colliderect(pos_rect):
                return True
        return False

    
    def update(self) : 
        self.board.fill(0) 
        self.board[self.food[0] , self.food[1]] = 2 
        for pos in self.snake.position: 
            self.board[pos[0] , pos[1]] = 1 
        self.snake.move()
        if np.array_equal(self.snake.position[0] , self.food) : 
            self.score += 1 
            self.snake.taille += 1
            newHead = self.snake.position[0] + self.snake.direction
            self.snake.position = np.vstack((newHead, self.snake.position)) 
            self.generateFood()
        if self.CheckCollision() or self.outOfBounds():
            self.game_over = True

    def restart(self):
        self.snake = Snake()
        self.score = 0
        self.generateFood()
        self.game_over = False
    
    def outOfBounds(self):
        head = self.snake.position[0]
        return (head[0] < 0 or head[0] >= board_w or head[1] < 0 or head[1] >= board_h)

    def state(self) : 
        return self.board ,self.snake.position[0] , self.food 

pygame.init() 
screen = pygame.display.set_mode((width , height))
clock = pygame.time.Clock() 

game = Game()


font = pygame.font.Font(None, 36)

while True : 
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT  : 
            pygame.quit()
            quit() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game.game_over:
                game.restart()

    if not game.game_over:
        board , snake_pos , food_pos = game.state() 

        headX , headY = snake_pos[0] , snake_pos[1]
        foodX , foodY = food_pos

        if headX < foodX : 
            next_move = "RIGHT"
        elif headX > foodX : 
            next_move = "LEFT"
        elif headY < foodY:
            next_move = "DOWN" 
        else:
            next_move = "UP" 
        game.snake.setDirection(next_move) 
        game.update()

    screen.fill(WHITE)
    for x in range(board_w) : 
        for y in range(board_h) :
            if board[x, y] == 1 :
                if (x, y) == (game.snake.position[0][0], game.snake.position[0][1]):
                    pygame.draw.rect(screen , BLACK, (x * Block_size, y * Block_size, Block_size, Block_size))
                else:
                    pygame.draw.rect(screen , GREEN, (x * Block_size, y * Block_size, Block_size, Block_size))
            elif board[x, y] == 2 :
                pygame.draw.rect(screen, RED, (x * Block_size, y * Block_size, Block_size, Block_size))

    if game.game_over:

        text = font.render("Game Over! Press 'R' to restart.", True, (255, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(10) 
