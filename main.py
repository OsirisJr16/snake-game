import numpy as np 
import pygame

Block_size =  20 
height , width = 480 , 640

board_w , board_h  = int(width/Block_size), int(height/Block_size)


class Snake : 
    def __init__(self) -> None:
        self.direction = np.array([0,0])
        self.position = np.array([[board_w//2 , board_h//2]])
        self.taille = 1  
    def move(self) : 
        self.position[1:] = self.position[:-1] 
        self.position[0] +=self.direction
   
    def setDirection(self ,direction) :
        if direction == 'UP' :
            self.direction= np.array([0 , -1])
        elif direction =='DOWN' : 
            self.direction= np.array([0, 1])
        elif direction == "LEFT" :
            self.direction = np.array([-1 , 0])
        elif direction =="RIGHT" :
            self.direction = np.array([1 , 0]) 
class Game : 
    def __init__(self) -> None:
        self.board = np.zeros((board_w , board_h))
        self.snake = Snake() 
        self.score = 0 
        self.food = None 
        self.generateFood() 
    def generateFood(self):
        while True:
            foodPos = np.random.randint(0, board_w - 1), np.random.randint(0, board_h - 1)
            if self.board[foodPos[0], foodPos[1]] == 0:
                self.food = foodPos
                break
    def CheckCollision(self) : 
        head = self.snake.position[0]
        for pos in self.snake.position[1:]:
            if np.array_equal(head, pos):
                return True
        return False
    def update(self) : 
        self.board.fill(0) 
        self.board[self.food[0] , self.food[1]] = 2 
        for pos in self.snake.position: 
            self.board[pos[0] , pos[1]] = 1 
        self.snake.move()
        if np.array_equal(self.snake.position[0] , self.food) : 
            self.score+=1 
            self.snake.taille+=1
            newHead = self.snake.position[0] + self.snake.direction
            self.snake.position = np.vstack((newHead, self.snake.position)) 
            self.generateFood()
        if self.CheckCollision() :
            self.gameOver()
    def gameOver(self) :
        print('GAME OVER')
        pygame.quit() 

    def state(self) : 
        return self.board ,self.snake.position[0] , self.food 
    

pygame.init() 
screen = pygame.display.set_mode((width , height))
clock = pygame.time.Clock() 

game = Game()
while True : 
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT  : 
            pygame.quit()
            quit() 
    board , snake_pos , food_pos = game.state() 

    headX , headY = snake_pos[0] , snake_pos[1]
    foodX , foodY = food_pos
    # algorithm 
    if headX<foodX : 
        next_move = "RIGHT"
    elif headX>foodX : 
        next_move = "LEFT"
    elif headY<foodY:
        next_move  = "DOWN" 
    else:
        next_move = "UP" 
    game.snake.setDirection(next_move) 
    game.update()
    screen.fill((255 , 255 ,255))
    for x in range(board_w) : 
        for y in range(board_h) :
            if board[x, y] == 1 :
                pygame.draw.rect(screen , (0 ,255 , 0),(x*Block_size , y*Block_size , Block_size , Block_size))
            elif board[x, y ]==2 :
                pygame.draw.rect(screen, (255 , 0 ,0) , (x*Block_size,y*Block_size , Block_size,Block_size))
    pygame.display.update()
    clock.tick(20) 