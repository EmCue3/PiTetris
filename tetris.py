from random import randrange as rand
import pygame
import sys
import time
# import RPi.GPIO as GPIO

# GPIO pin numbering and definition
# pin 21 = player 1 left movement
# pin 20 = player 1 drop
# pin 16 = player 1 right movement
# pin 12 = player 1 rotation
# pin 24 = player 2 right movement
# pin 25 = player 2 drop
# pin 8 = player 2 left movement
# pin 7 = player 2 rotation

# GPIO Pin setup initializing all 8 pins for input detection
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialize all imported pygame modules
pygame.init()

# board state and scoring system
initialization = {
    'cell_size': 20,
    'cols': 32,
    'rows': 32,
    'delay': 400,
    'fps': 20,
    'score': 0,
}

# colour definition of blocks
colourArray = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (127, 117, 157),
    (80, 255, 80),
    (255, 80, 80),
    (80, 80, 255),
    (13, 45, 90)
]

# all tetris blocks
tetrisShapes = [
    [[1, 0, 1],
     [0, 1, 0]],

    [[0, 2, 2, 0],
     [2, 2, 2, 0]],

    [[3, 3],
     [0, 3]],

    [[4, 0, 0],
     [4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5],
     [0, 0, 5]],

    [[6, 6, 6]],

    [[7, 7, 7, 7],
     [7, 7, 0, 0]],
]

# obstacle shapes
obstacle = [
    [[8, 0, 8],
     [8, 8, 8],
     [8, 0, 8]],

    [[9, 9, 9, 9, 9, 9, 9, 9, 9]],

    [[1, 0, 0, 1],
     [0, 1, 1, 0],
     [1, 0, 0, 1]],
]


# initializes tetris board with 1's as bottom border collision
def new_board():
    board = [[0 for columns in range(initialization['cols'])] for rows in range(initialization['rows'])]
    board += [[1 for x in range(initialization['cols'])]]
    return board


# delete row of blocks when it is filled, resulting in score increase
def remove_row(board, row):
    initialization['score'] += int(10000 * (1 / initialization['delay']))
    del board[row]
    return [[0 for i in range(initialization['cols'])]] + board


# rotate block clockwise
def rotate(block):
    rotated = list(zip(*block[::-1]))
    return rotated


# detect collision with the bottom of the board with side and bottom of blocks
def collision(board, block, disp):
    x_disp, y_disp = disp
    for rownum in range(len(block)):
        blockrow = block[rownum]
        for cellnum in range(len(blockrow)):
            try:
                if blockrow[cellnum] and board[rownum + y_disp][cellnum + x_disp]:
                    return True
            except IndexError:
                return True
    return False


# joins shapes to the board at the bottom when collision is detected
def join_matrices(matrix1, matrix2, matrix2_off):
    x_off, y_off = matrix2_off
    for rownum in range(len(matrix2)):
        mat2_row = matrix2[rownum]
        for cellnum in range(len(mat2_row)):
            matrix1[rownum + y_off - 1][cellnum + x_off] += mat2_row[cellnum]
    return matrix1


# generate background image as sprite and prepare for blit to screen in game loop
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# main game class
class TetrisMain(object):
    def __init__(self):  # initialize values in game
        pygame.init()
        self.width = initialization['cell_size'] * initialization['cols']
        self.height = initialization['cell_size'] * initialization['rows']
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.update()
        self.init_game()

    def init_game(self):  # initial object initialization on game startup
        self.board = new_board()
        self.new_block()
        self.new_block2()
        self.new_obstacle()
        self.new_obstacle2()
        self.new_obstacle3()
        self.new_obstacle4()
        self.new_obstacle5()
        self.new_obstacle6()
        self.new_obstacle7()
        self.new_obstacle8()
        self.vertical_obstacle()
        self.vertical_obstacle2()

    def point_counter(self):
        myfont = pygame.font.SysFont('Times New Roman', 20)
        textsurface = myfont.render("Team points: {0}".format(initialization['score']), True, (0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (int(self.width / 2.44), 15, 140, 25))
        self.screen.blit(textsurface, (int(self.width / 2.44), 15))

    # obstacle creation to increase difficulty for the players
    def new_obstacle(self):
        self.obstacle = obstacle[rand(len(obstacle))]
        self.yobstacle = rand(initialization['rows'] - 2)
        self.xobstacle = rand(initialization['cols'])

    def new_obstacle2(self):
        self.obstacle2 = obstacle[rand(len(obstacle))]
        self.yobstacle2 = rand(initialization['rows'] - 2)
        self.xobstacle2 = rand(initialization['cols'])

    def new_obstacle3(self):
        self.obstacle3 = obstacle[rand(len(obstacle))]
        self.yobstacle3 = rand(initialization['rows'] - 2)
        self.xobstacle3 = rand(initialization['cols'])

    def new_obstacle4(self):
        self.obstacle4 = obstacle[rand(len(obstacle))]
        self.yobstacle4 = rand(initialization['rows'] - 2)
        self.xobstacle4 = rand(initialization['cols'])

    def new_obstacle5(self):
        self.obstacle5 = obstacle[rand(len(obstacle))]
        self.yobstacle5 = rand(initialization['rows'] - 2)
        self.xobstacle5 = rand(initialization['cols'])

    def new_obstacle6(self):
        self.obstacle6 = obstacle[rand(len(obstacle))]
        self.yobstacle6 = rand(initialization['rows'] - 2)
        self.xobstacle6 = rand(initialization['cols'])

    def new_obstacle7(self):
        self.obstacle7 = obstacle[rand(len(obstacle))]
        self.yobstacle7 = rand(initialization['rows'] - 2)
        self.xobstacle7 = rand(initialization['cols'])

    def new_obstacle8(self):
        self.obstacle8 = obstacle[rand(len(obstacle))]
        self.yobstacle8 = rand(initialization['rows'] - 2)
        self.xobstacle8 = rand(initialization['cols'])

    def vertical_obstacle(self):
        self.vobstacle = obstacle[rand(len(obstacle))]
        self.yvertical_obstacle = (initialization['rows'])
        self.xvertical_obstacle = rand(initialization['cols'])

    def vertical_obstacle2(self):
        self.vobstacle2 = obstacle[rand(len(obstacle))]
        self.yvertical_obstacle2 = (initialization['rows'])
        self.xvertical_obstacle2 = rand(initialization['cols'])

    def new_block(self):  # initialize block for player 1 at 1/4 the width of the screen
        self.block = tetrisShapes[rand(len(tetrisShapes))]
        self.xblock = int(initialization['cols'] / 4 - len(self.block[0]) / 2)
        self.yblock = 0

        if collision(self.board, self.block, (self.xblock, self.yblock)):
            self.gameover = True

    def new_block2(self):  # initialize block for player 2 at 3/4 the width of the screen
        self.block2 = tetrisShapes[rand(len(tetrisShapes))]
        self.xblock2 = int((initialization['cols'] * 3) / 4 - len(self.block2[0]) / 2)
        self.yblock2 = 0

        if collision(self.board, self.block2, (self.xblock2, self.yblock2)):
            self.gameover = True

    def draw_matrix(self, matrix, disp):  # draw block
        x_disp, y_disp = disp
        for rownum in range(len(matrix)):
            matrixrow = matrix[rownum]
            for matrixvalue in range(len(matrixrow)):
                if matrixrow[matrixvalue]:
                    pygame.draw.rect(self.screen, colourArray[matrixrow[matrixvalue]], pygame.Rect(
                        (x_disp + matrixvalue) * initialization['cell_size'],
                        (y_disp + rownum) * initialization['cell_size'], initialization['cell_size'],
                        initialization['cell_size']), 0)

    def draw_obstacle(self, matrix, disp):  # draw obstacle
        x_disp, y_disp = disp
        for rownum in range(len(matrix)):
            matrixrow = matrix[rownum]
            for matrixvalue in range(len(matrixrow)):
                if matrixrow[matrixvalue]:
                    pygame.draw.rect(self.screen, colourArray[rand(len(tetrisShapes))], pygame.Rect(
                        (x_disp + matrixvalue) * initialization['cell_size'],
                        (y_disp + rownum) * initialization['cell_size'], initialization['cell_size'],
                        initialization['cell_size']), 0)

    def move(self, xmovement):  # move block for p1
        if not self.gameover:
            xnew = self.xblock + xmovement
            if xnew < 0:
                xnew = 0
            if xnew > int(initialization['cols'] / 2) - len(self.block[0]):
                xnew = int(initialization['cols'] / 2) - len(self.block[0])
            if collision(self.board, self.block, (xnew, self.yblock)) is False:
                self.xblock = xnew

    def move2(self, xmovement):  # move block for p2
        if not self.gameover:
            xnew = self.xblock2 + xmovement
            if xnew < int(initialization['cols'] / 2):
                xnew = int(initialization['cols'] / 2)
            if xnew > initialization['cols'] - len(self.block2[0]):
                xnew = initialization['cols'] - len(self.block2[0])
            if collision(self.board, self.block2, (xnew, self.yblock2)) is False:
                self.xblock2 = xnew

    def rotate_block(self):  # rotate p1 block
        if not self.gameover:
            new_block = rotate(self.block)
            if collision(self.board, new_block, (self.xblock, self.yblock)) is False:
                self.block = new_block

    def rotate_block2(self):  # rotate p2 block
        if not self.gameover:
            new_block2 = rotate(self.block2)
            if collision(self.board, new_block2, (self.xblock2, self.yblock2)) is False:
                self.block2 = new_block2

    def drop(self):  # move block down for p1
        if not self.gameover:
            self.yblock += 1
            if collision(self.board, self.block, (self.xblock, self.yblock)):
                self.board = join_matrices(self.board, self.block, (self.xblock, self.yblock))
                self.new_block()
                while True:
                    for rownum, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(self.board, rownum)
                            break
                    else:
                        break

    def drop2(self):  # move block down for p2
        if not self.gameover:
            self.yblock2 += 1
            if collision(self.board, self.block2, (self.xblock2, self.yblock2)):
                self.board = join_matrices(self.board, self.block2, (self.xblock2, self.yblock2))
                self.new_block2()

    # move obstacles across screen
    def move_obstacle(self):
        if not self.gameover:
            self.xobstacle += rand(1, 5)
            if self.xobstacle > initialization['cols'] - len(obstacle[0]):
                self.new_obstacle()

    def move_obstacle2(self):
        if not self.gameover:
            self.xobstacle2 -= rand(1, 5)
            if self.xobstacle2 < 0:
                self.new_obstacle2()

    def move_obstacle3(self):
        if not self.gameover:
            self.xobstacle3 += rand(1, 5)
            if self.xobstacle3 > initialization['cols'] - len(obstacle[0]):
                self.new_obstacle3()

    def move_obstacle4(self):
        if not self.gameover:
            self.xobstacle4 -= rand(1, 5)
            if self.xobstacle4 < 0:
                self.new_obstacle4()

    def move_obstacle5(self):
        if not self.gameover:
            self.xobstacle5 += rand(1, 5)
            if self.xobstacle5 > initialization['cols'] - len(obstacle[0]):
                self.new_obstacle5()

    def move_obstacle6(self):
        if not self.gameover:
            self.xobstacle6 -= rand(1, 5)
            if self.xobstacle6 < 0:
                self.new_obstacle6()

    def move_obstacle7(self):
        if not self.gameover:
            self.xobstacle7 += rand(1, 5)
            if self.xobstacle7 > initialization['cols'] - len(obstacle[0]):
                self.new_obstacle7()

    def move_obstacle8(self):
        if not self.gameover:
            self.xobstacle8 -= rand(1, 5)
            if self.xobstacle8 < 0:
                self.new_obstacle8()

    def move_vertical_obstacle(self):
        if not self.gameover:
            self.yvertical_obstacle -= rand(1, 5)
            if self.yvertical_obstacle < 0:
                self.vertical_obstacle()

    def move_vertical_obstacle2(self):
        if not self.gameover:
            self.yvertical_obstacle2 -= rand(1, 5)
            if self.yvertical_obstacle2 < 0:
                self.vertical_obstacle2()

    # function to render message during gameover and quit
    def center_msg(self, msg):
        msgfont = pygame.font.SysFont('Times New Roman', 25)
        textsurface = msgfont.render(msg, True, (0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (int(self.width / 3.255), int(self.height / 2.5), 230, 25))
        self.screen.blit(textsurface, (int(self.width / 3.255), int(self.height / 2.5)))

    # end the game
    def quitgame(self):
        self.center_msg("Hope you had fun!")
        self.gameover = True
        pygame.display.update()
        sys.exit()

    # main game run loop
    def start(self):
        pygame.display.set_caption("Advanced Dual Blocks")
        self.gameover = False

        pygame.time.set_timer(pygame.USEREVENT + 1, initialization['delay'])
        gameclock = pygame.time.Clock()  # used with fps to change game speed
        while 1:
            self.screen.fill((0, 0, 0))
            backGround = Background('polyomino.png', [0, 0])
            self.screen.blit(backGround.image, backGround.rect)  # refresh screen
            if (self.gameover):
                self.center_msg("Game Over! Nice Try!")
            pygame.draw.rect(self.screen, (0, 0, 0), (self.width / 2, 0, 3, self.height))  # background for text box
            # player1_left = GPIO.input(21)
            # player1_drop = GPIO.input(20)
            # player1_right = GPIO.input(16)
            # player1_rotate = GPIO.input(12)
            # player2_rotate = GPIO.input(7)
            # player2_left = GPIO.input(8)
            # player2_drop = GPIO.input(25)
            # player2_right = GPIO.input(24)
            # if not player1_left:
            #     self.move(-1)
            # if not player1_drop:
            #     self.drop()
            # if not player1_right:
            #     self.move(1)
            # if not player1_rotate:
            #     self.rotate_block()
            # if not player2_left:
            #     self.move2(-1)
            # if not player2_drop:
            #     self.drop2()
            # if not player2_right:
            #     self.move2(1)
            # if not player2_rotate:
            #     self.rotate_block2()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.move(-1)
            if keys[pygame.K_d]:
                self.move(1)
            if keys[pygame.K_w]:
                self.rotate_block()
            if keys[pygame.K_s]:
                self.drop()
            if keys[pygame.K_LEFT]:
                self.move2(-1)
            if keys[pygame.K_RIGHT]:
                self.move2(1)
            if keys[pygame.K_UP]:
                self.rotate_block2()
            if keys[pygame.K_DOWN]:
                self.drop2()

            time.sleep(0.1)
            self.point_counter()
            if self.gameover:
                pygame.display.set_caption("Your Final Score was: {0}".format(initialization['score']))
            else:  # draw objects if not gameover
                self.draw_matrix(self.board, (0, 0))
                self.draw_matrix(self.block, (self.xblock, self.yblock))
                self.draw_matrix(self.board, (0, 0))
                self.draw_matrix(self.block2, (self.xblock2, self.yblock2))
                self.draw_obstacle(self.obstacle, (self.xobstacle, self.yobstacle))
                self.draw_obstacle(self.obstacle2, (self.xobstacle2, self.yobstacle2))
                self.draw_obstacle(self.obstacle3, (self.xobstacle3, self.yobstacle3))
                self.draw_obstacle(self.obstacle4, (self.xobstacle4, self.yobstacle4))
                self.draw_obstacle(self.obstacle5, (self.xobstacle5, self.yobstacle5))
                self.draw_obstacle(self.obstacle6, (self.xobstacle6, self.yobstacle6))
                self.draw_obstacle(self.obstacle7, (self.xobstacle7, self.yobstacle7))
                self.draw_obstacle(self.obstacle8, (self.xobstacle8, self.yobstacle8))
                self.draw_obstacle(self.vobstacle, (self.xvertical_obstacle, self.yvertical_obstacle))
                self.draw_obstacle(self.vobstacle2, (self.xvertical_obstacle2, self.yvertical_obstacle2))

            pygame.display.update()

            for event in pygame.event.get():  # move objects every tick
                if event.type == pygame.USEREVENT + 1:
                    self.drop()
                    self.drop2()
                    self.move_obstacle()
                    self.move_obstacle2()
                    self.move_obstacle3()
                    self.move_obstacle4()
                    self.move_obstacle5()
                    self.move_obstacle6()
                    self.move_obstacle7()
                    self.move_obstacle8()
                    self.move_vertical_obstacle()
                    self.move_vertical_obstacle2()

                elif event.type == pygame.QUIT:
                    self.quitgame()
            gameclock.tick(initialization['fps'])


# start game
if __name__ == '__main__':
    App = TetrisMain()
    App.start()

# this is the keyboard input that can be used instead of tactile button input if desired

# keys = pygame.key.get_pressed()
# if keys[pygame.K_a]:
#     self.move(-1)
# if keys[pygame.K_d]:
#     self.move(1)
# if keys[pygame.K_w]:
#     self.rotate_block()
# if keys[pygame.K_s]:
#     self.drop()
# if keys[pygame.K_LEFT]:
#     self.move2(-1)
# if keys[pygame.K_RIGHT]:
#     self.move2(1)
# if keys[pygame.K_UP]:
#     self.rotate_block2()
# if keys[pygame.K_DOWN]:
#     self.drop2()