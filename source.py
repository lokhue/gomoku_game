import pygame


# Khai báo các biến toàn cục
WIDTH, HEIGHT = 1000, 660
BOARD_SIZE = 20
SQUARE_SIZE = HEIGHT // BOARD_SIZE
lim = 2
blockedOneSide = False
flag = False
board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
moveCounter = 0

#Biến giành cho chức năng count down
time_remaining = 10  # in seconds
clock = pygame.time.Clock()
time_remaining_super_easy_mode = 21
time_remaining_easy_mode = 16
time_remaining_medium_mode = 11
time_remaining_hard_mode = 3.5
time_remaining_nightmare_mode = 2

current_level = time_remaining_super_easy_mode

# Định nghĩa màu
white = (255, 255, 255)
black = (0, 0, 0)
last_move_cell_color = (237, 24, 27)
game_bg_color = (50, 50, 50)
dark_gray = (30, 30, 30)
red = (255,15,15)

# font
pygame.font.init()
custom_font_path = './assets/fonts/TechnoRaceItalic-eZRWe.otf'
custom_font_path_1 = './assets/fonts/BruceForeverRegular-X3jd2.ttf'
custom_font_path_2 = './assets/fonts/dh.otf'

font_size = 70
font_size_200 = 200
font_size_85 = 85
font_size_60 = 60
font = pygame.font.Font(custom_font_path, font_size)
font_1 = pygame.font.Font(custom_font_path_1, font_size_85)
font_2 = pygame.font.Font(custom_font_path_2, font_size_60)

# Khởi tạo Pygame
pygame.init()

# Tạo cửa sổ game
icon = pygame.transform.scale(pygame.image.load(r'./assets/images/icon.png'), (SQUARE_SIZE, SQUARE_SIZE))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro Game")
pygame.display.set_icon(icon)
#class
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

lastMove = Position(0,0)


#âm thanh
pygame.mixer.init()
poc_sound = pygame.mixer.Sound(r"./assets/sounds/poc.wav")
switch_sound = pygame.mixer.Sound(r"./assets/sounds/switch_2.wav")
switch_sound_1 = pygame.mixer.Sound(r"./assets/sounds/switch_1.wav")
lose_sound = pygame.mixer.Sound(r"./assets/sounds/lose.wav")
win_sound = pygame.mixer.Sound(r"./assets/sounds/win.wav")
claps_sound = pygame.mixer.Sound("./assets/sounds/claps.wav")
#Quân cờ
X = pygame.transform.scale(pygame.image.load(r'./assets/images/x.png'), (SQUARE_SIZE - 4, SQUARE_SIZE - 4))
O = pygame.transform.scale(pygame.image.load(r'./assets/images/o.png'), (SQUARE_SIZE - 4, SQUARE_SIZE - 4))

# Hàm vẽ ô cờ
def draw_cell(cell_color, border_color, row, col):
    pygame.draw.rect(screen, cell_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0)
    pygame.draw.rect(screen, border_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
# Hàm vẽ bảng cờ
def draw_board():
    pygame.draw.rect(screen, dark_gray, (HEIGHT, 0, WIDTH - HEIGHT, HEIGHT))
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            draw_cell(white, black, row, col)

# vẽ X, O
def draw_x(x, y):
    screen.blit(X, (y*SQUARE_SIZE + 2, x*SQUARE_SIZE + 2))

def draw_o(x, y):
    screen.blit(O, (y*SQUARE_SIZE + 2, x*SQUARE_SIZE + 2))

# kết quả game
def draw_result_with_pc(text):
    screen.fill(game_bg_color)
    text = font_1.render(text, True, "gray")
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()


# kiểm tra tại vị trí x, y người chơi lượt "turn" thắng hay không
def check_win(board, x, y, turn):
    if countRow(board, x, y) >= 5 or \
       countColumn(board, x, y) >= 5 or \
       countMainDiaLine(board, x, y) >= 5 or \
       countSubDiaLine(board, x, y) >= 5:
        return True
    return False

#đổi 1 thành 2, 2 thành 1
def ot(turn):
    return 3 - turn

#tính độ ưu tiên của nước đi tại hàng row và cột col
def priorityMove(b, row, col, turn, lim):
    oppoTurn = ot(turn)
    bClone = [row[:] for row in b]

    bClone[row][col] = oppoTurn
    b[row][col] = turn

    r = countRowInterupt(b, row, col, turn, lim)
    c = countColumnInterupt(b, row, col, turn, lim)
    m = countMainDiaLineInterupt(b, row, col, turn, lim)
    s = countSubDiaLineInterupt(b, row, col, turn, lim)

    r1 = countRowInterupt(bClone, row, col, oppoTurn, lim)
    c1 = countColumnInterupt(bClone, row, col, oppoTurn, lim)
    m1 = countMainDiaLineInterupt(bClone, row, col, oppoTurn, lim)
    s1 = countSubDiaLineInterupt(bClone, row, col, oppoTurn, lim)

    if r1 + c1 == 6 or r1 + m1 == 6 or r1 + s1 == 6 or c1 + s1 == 6 or m1 + s1 == 6 or c1 + m1 == 6:
        print(r1, c1, m1, s1)
    if r + c == 6 or r + m == 6 or r + s == 6 or c + s == 6 or m + s == 6 or c + m == 6:
        print(isFreeMove(b, row, col, turn, 3))

    if check_win(b, row, col, turn):
        b[row][col] = 0
        return 100
    if check_win(bClone, row, col, oppoTurn):
        b[row][col] = 0
        return 99
    if isFreeMove2(b, row, col, 4) >= 1:
        b[row][col] = 0
        return 98
    if isFreeMove2(bClone, row, col, 4) >= 1:
        b[row][col] = 0
        return 97
    if (((r + c == 8 or r + m == 8 or r + s == 8 or c + s == 8 or m + s == 8 or c + m == 8) and isFreeOneSide(b, row, col, turn, 4) >= 2) or r == 5 or c == 5 or m == 5 or s == 5):
        b[row][col] = 0
        return 96
    if (((r1 + c1 == 8 or r1 + m1 == 8 or r1 + s1 == 8 or c1 + s1 == 8 or m1 + s1 == 8 or c1 + m1 == 8) and isFreeOneSide(bClone, row, col, oppoTurn, 4) >= 2) or r1 == 5 or c1 == 5 or m1 == 5 or s1 == 5):
        b[row][col] = 0
        return 95
    if (r + c == 7 or r + m == 7 or r + s == 7 or c + s == 7 or m + s == 7 or c + m == 7) and isFreeMove(b, row, col, turn, 3) >= 1 and isFreeOneSide(b, row, col, turn, 4) >= 1:
        b[row][col] = 0
        return 94
    if (r1 + c1 == 7 or r1 + m1 == 7 or r1 + s1 == 7 or c1 + s1 == 7 or m1 + s1 == 7 or c1 + m1 == 7) and isFreeMove(bClone, row, col, oppoTurn, 3) >= 1 and isFreeOneSide(bClone, row, col, oppoTurn, 4) >= 1:
        b[row][col] = 0
        return 93
    if (r + c == 6 or r + m == 6 or r + s == 6 or c + s == 6 or m + s == 6 or c + m == 6) and isFreeMove(b, row, col, turn, 3) >= 2:
        b[row][col] = 0
        return 92
    if (r1 + c1 == 6 or r1 + m1 == 6 or r1 + s1 == 6 or c1 + s1 == 6 or m1 + s1 == 6 or c1 + m1 == 6) and isFreeMove(bClone, row, col, oppoTurn, 3) >= 2:
        b[row][col] = 0
        return 91

    b[row][col] = 0
    return r + c + m + s + s1 + r1 + c1 + m1

def priorityMove1(b, row, col, turn, lim):
    oppoTurn = ot(turn)
    bClone = [row[:] for row in b]

    bClone[row][col] = oppoTurn
    b[row][col] = turn

    r = countRowInterupt(b, row, col, turn, lim)
    c = countColumnInterupt(b, row, col, turn, lim)
    m = countMainDiaLineInterupt(b, row, col, turn, lim)
    s = countSubDiaLineInterupt(b, row, col, turn, lim)

    r1 = countRowInterupt(bClone, row, col, oppoTurn, lim)
    c1 = countColumnInterupt(bClone, row, col, oppoTurn, lim)
    m1 = countMainDiaLineInterupt(bClone, row, col, oppoTurn, lim)
    s1 = countSubDiaLineInterupt(bClone, row, col, oppoTurn, lim)

    if check_win(b, row, col, turn):
        b[row][col] = 0
        return 100
    if check_win(b, row, col, oppoTurn):
        b[row][col] = 0
        return 99
    if (((r + c == 8 or r + m == 8 or r + s == 8 or c + s == 8 or m + s == 8 or c + m == 8) and isFreeOneSide(b, row, col, turn, 4) >= 2) or r == 5 or c == 5 or m == 5 or s == 5):
        b[row][col] = 0
        return 98
    if (((r1 + c1 == 8 or r1 + m1 == 8 or r1 + s1 == 8 or c1 + s1 == 8 or m1 + s1 == 8 or c1 + m1 == 8) and isFreeOneSide(bClone, row, col, oppoTurn, 4) >= 2) or r1 == 5 or c1 == 5 or m1 == 5 or s1 == 5):
        b[row][col] = 0
        return 97
    if isFreeMove2(b, row, col, 4) >= 1:
        b[row][col] = 0
        return 96
    if isFreeMove2(bClone, row, col, 4) >= 1:
        b[row][col] = 0
        return 95
    if (r + c == 7 or r + m == 7 or r + s == 7 or c + s == 7 or m + s == 7 or c + m == 7) and isFreeMove(b, row, col, turn, 3) >= 1 and isFreeOneSide(b, row, col, turn, 4) >= 1:
        b[row][col] = 0
        return 94
    if (r1 + c1 == 7 or r1 + m1 == 7 or r1 + s1 == 7 or c1 + s1 == 7 or m1 + s1 == 7 or c1 + m1 == 7) and isFreeMove(bClone, row, col, oppoTurn, 3) >= 1 and isFreeOneSide(bClone, row, col, oppoTurn, 4) >= 1:
        b[row][col] = 0
        return 93
    if (r + c == 6 or r + m == 6 or r + s == 6 or c + s == 6 or m + s == 6 or c + m == 6) and isFreeMove(b, row, col, turn, 3) >= 2:
        b[row][col] = 0
        return 92
    if (r1 + c1 == 6 or r1 + m1 == 6 or r1 + s1 == 6 or c1 + s1 == 6 or m1 + s1 == 6 or c1 + m1 == 6) and isFreeMove(bClone, row, col, oppoTurn, 3) >= 2:
        b[row][col] = 0
        return 91
    if (r + c == 5 or r + m == 5 or r + s == 5 or c + s == 5 or m + s == 5 or c + m == 5) and isFreeMove(b, row, col, turn, 3) >= 1 and isFreeMove(b, row, col, turn, 2) >= 1:
        b[row][col] = 0
        return 90
    if (r1 + c1 == 5 or r1 + m1 == 5 or r1 + s1 == 5 or c1 + s1 == 5 or m1 + s1 == 5 or c1 + m1 == 5) and isFreeMove(bClone, row, col, oppoTurn, 3) >= 1 and isFreeMove(bClone, row, col, oppoTurn, 2) >= 1:
        b[row][col] = 0
        return 89
    if (r + c == 4 or r + m == 4 or r + s == 4 or c + s == 4 or m + s == 4 or c + m == 4) and isFreeMove(b, row, col, turn, 2) >= 2:
        b[row][col] = 0
        return 88
    if (r1 + c1 == 4 or r1 + m1 == 4 or r1 + s1 == 4 or c1 + s1 == 4 or m1 + s1 == 4 or c1 + m1 == 4) and isFreeMove(bClone, row, col, oppoTurn, 2) >= 2:
        b[row][col] = 0
        return 87
    if (r + c == 3 or r + m == 3 or r + s == 3 or c + s == 3 or m + s == 3 or c + m == 3) and isFreeMove(b, row, col, turn, 2):
        b[row][col] = 0
        return 86
    if (r1 + c1 == 3 or r1 + m1 == 3 or r1 + s1 == 3 or c1 + s1 == 3 or m1 + s1 == 3 or c1 + m1 == 3) and isFreeMove(bClone, row, col, oppoTurn, 2):
        b[row][col] = 0
        return 85

    b[row][col] = 0
    return 0


#đếm số quân trên 1 hàng, cột,... nếu cách nhau 1 ô vẫn đếm
def countRowInterupt(b, x, y, turn, lim):
    global blockedOneSide, flag
    counter = 0
    i = y + 1
    optur = ot(turn)
    if i < BOARD_SIZE - 1 and i >= 0:
        while b[x][i] != optur and i < BOARD_SIZE - 1 and i < y + lim:
            if b[x][i] == 0 and b[x][i - 1] == 0:
                break
            if b[x][i] == turn:
                counter += 1
            i += 1

        botBlocked = b[x][i] == optur
        i = y - 1

        while b[x][i] != optur and i >= 0 and i > y - lim:
            if b[x][i] == 0 and b[x][i + 1] == 0:
                break
            if b[x][i] == turn:
                counter += 1
            i -= 1

        topBlocked = b[x][i] == optur
        flag = not topBlocked and not botBlocked
        blockedOneSide = (not topBlocked or not botBlocked)
    return counter + 1

def countColumnInterupt(b, x, y, turn, lim):
    global blockedOneSide, flag
    counter = 0
    i = x + 1
    optur = ot(turn)
    if i < BOARD_SIZE - 1 and i >= 0:

        while b[i][y] != optur and i < BOARD_SIZE - 1 and i < x + lim:
            if b[i][y] == 0 and b[i - 1][y] == 0:
                break
            if b[i][y] == turn:
                counter += 1
            i += 1

        botBlocked = b[i][y] == optur
        i = x - 1

        while b[i][y] != optur and i >= 0 and i > x - lim:
            if b[i][y] == 0 and b[i + 1][y] == 0:
                break
            if b[i][y] == turn:
                counter += 1
            i -= 1

        topBlocked = b[i][y] == optur
        flag = not topBlocked and not botBlocked
        blockedOneSide = (not topBlocked or not botBlocked)
    return counter + 1

def countMainDiaLineInterupt(b, x, y, turn, lim):
    global blockedOneSide, flag
    counter = 0
    i = x + 1
    j = y + 1
    optur = ot(turn)

    if i < BOARD_SIZE - 1 and  j < BOARD_SIZE - 1 and i >= 0 and j >= 0:
        while b[i][j] != optur and i < BOARD_SIZE - 1 and j < BOARD_SIZE - 1 and i < x + lim and j < y + lim:
            if b[i][j] == 0 and b[i - 1][j - 1] == 0:
                break
            if b[i][j] == turn:
                counter += 1
            i += 1
            j += 1

        botBlocked = b[i][j] == optur
        i = x - 1
        j = y - 1

        while b[i][j] != optur and i >= 0 and j >= 0 and i > x - lim and j > y - lim:
            if b[i][j] == 0 and b[i + 1][j + 1] == 0:
                break
            if b[i][j] == turn:
                counter += 1
            i -= 1
            j -= 1

        topBlocked = b[i][j] == optur
        flag = not topBlocked and not botBlocked
        blockedOneSide = (not topBlocked or not botBlocked)
    return counter + 1

def countSubDiaLineInterupt(b, x, y, turn, lim):
    global blockedOneSide, flag
    counter = 0
    i = x + 1
    j = y - 1
    optur = ot(turn)
    if i < BOARD_SIZE - 1 and  j < BOARD_SIZE - 1 and i >= 0 and j >= 0:

        while b[i][j] != optur and i < BOARD_SIZE - 1 and j >= 0 and i < x + lim and j > y - lim:
            if b[i][j] == 0 and b[i - 1][j + 1] == 0:
                break
            if b[i][j] == turn:
                counter += 1
            i += 1
            j -= 1

        botBlocked = b[i][j] == optur
        i = x - 1
        j = y + 1
    if i < BOARD_SIZE - 1 and  j < BOARD_SIZE - 1 and i >= 0 and j >= 0:

        while b[i][j] != optur and i >= 0 and j < BOARD_SIZE - 1 and i > x - lim and j < y + lim:
            if b[i][j] == 0 and b[i + 1][j - 1] == 0:
                break
            if b[i][j] == turn:
                counter += 1
            i -= 1
            j += 1

        topBlocked = b[i][j] == optur
        flag = not topBlocked and not botBlocked
        blockedOneSide = (not topBlocked or not botBlocked)
    return counter + 1

#đếm số quân trên 1 hàng, cột,... nhưng phải liên tiếp nhau
def countRow(b, x, y):
    counter = 0
    i = y

    if b[x][y] == 0:
        return 0

    while i + 1 < BOARD_SIZE and b[x][i] == b[x][i + 1] and b[x][i] != 0:
        counter += 1
        i += 1

    right_blocked = (i == BOARD_SIZE - 1 or b[x][i + 1] != 0)
    i = y

    while i - 1 >= 0 and b[x][i] == b[x][i - 1] and b[x][i] != 0:
        counter += 1
        i -= 1

    left_blocked = (i == 0 or b[x][i - 1] != 0)
    global flag
    flag = not left_blocked and not right_blocked

    global blockedOneSide
    blockedOneSide = (not left_blocked or not right_blocked) and not flag

    return counter + 1

def countColumn(b, x, y):
    counter = 0
    i = x

    if b[x][y] == 0:
        return 0

    while i + 1 < BOARD_SIZE and b[i][y] == b[i + 1][y] and b[i][y] != 0:
        counter += 1
        i += 1

    bot_blocked = (i == BOARD_SIZE - 1 or b[i + 1][y] != 0)
    i = x

    while i - 1 >= 0 and b[i][y] == b[i - 1][y] and b[i][y] != 0:
        counter += 1
        i -= 1

    top_blocked = (i == 0 or b[i - 1][y] != 0)
    global flag
    flag = not bot_blocked and not top_blocked

    global blockedOneSide
    blockedOneSide = (not top_blocked or not bot_blocked) and not flag

    return counter + 1

def countMainDiaLine(b, x, y):
    counter = 0
    i, j = x, y

    if b[x][y] == 0:
        return 0

    while i + 1 < BOARD_SIZE and j + 1 < BOARD_SIZE and b[i][j] == b[i + 1][j + 1] and b[i][j] != 0:
        counter += 1
        i += 1
        j += 1

    bot_blocked = (i == BOARD_SIZE - 1 or j == BOARD_SIZE - 1 or b[i + 1][j + 1] != 0)
    i, j = x, y

    while i - 1 >= 0 and j - 1 >= 0 and b[i][j] == b[i - 1][j - 1] and b[i][j] != 0:
        counter += 1
        i -= 1
        j -= 1

    top_blocked = (i == 0 or j == 0 or b[i - 1][j - 1] != 0)
    global flag
    flag = not bot_blocked and not top_blocked

    global blockedOneSide
    blockedOneSide = (not top_blocked or not bot_blocked) and not flag

    return counter + 1

def countSubDiaLine(b, x, y):
    counter = 0
    i, j = x, y

    if b[x][y] == 0:
        return 0

    while i + 1 < BOARD_SIZE and j - 1 >= 0 and b[i][j] == b[i + 1][j - 1] and b[i][j] != 0:
        counter += 1
        i += 1
        j -= 1

    bot_blocked = (i == BOARD_SIZE - 1 or j == 0 or b[i + 1][j - 1] != 0)
    i, j = x, y

    while i - 1 >= 0 and j + 1 < BOARD_SIZE and b[i][j] == b[i - 1][j + 1] and b[i][j] != 0:
        counter += 1
        i -= 1
        j += 1

    top_blocked = (i == 0 or j == BOARD_SIZE - 1 or b[i - 1][j + 1] != 0)
    global flag
    flag = not bot_blocked and not top_blocked

    global blockedOneSide
    blockedOneSide = (not top_blocked or not bot_blocked) and not flag

    return counter + 1

def isFreeMove(b, x, y, turn, t):
    global flag
    flag = False
    counter = 0

    if countRowInterupt(b, x, y, turn, 5) == t and flag:
        counter += 1
        flag = False

    if countColumnInterupt(b, x, y, turn, 5) == t and flag:
        counter += 1
        flag = False

    if countMainDiaLineInterupt(b, x, y, turn, 5) == t and flag:
        counter += 1
        flag = False

    if countSubDiaLineInterupt(b, x, y, turn, 5) == t and flag:
        counter += 1
        flag = False

    return counter

def isFreeMove2(b, x, y, t):
    global flag
    flag = False
    counter = 0
    
    if countRow(b, x, y) == t and flag:
        counter += 1
        flag = False

    if countColumn(b, x, y) == t and flag:
        counter += 1
        flag = False

    if countMainDiaLine(b, x, y) == t and flag:
        counter += 1
        flag = False

    if countSubDiaLine(b, x, y) == t and flag:
        counter += 1
        flag = False

    return counter

def isFreeOneSide(b, x, y, turn, t):
    global blockedOneSide
    blockedOneSide = False
    counter = 0

    if countRowInterupt(b, x, y, turn, 5) == t and blockedOneSide:
        counter += 1
        blockedOneSide = False

    if countColumnInterupt(b, x, y, turn, 5) == t and blockedOneSide:
        counter += 1
        blockedOneSide = False

    if countMainDiaLineInterupt(b, x, y, turn, 5) == t and blockedOneSide:
        counter += 1
        blockedOneSide = False

    if countSubDiaLineInterupt(b, x, y, turn, 5) == t and blockedOneSide:
        counter += 1
        blockedOneSide = False

    return counter

def priorityArray(board, turn):
    pArr = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                pArr[i][j] = priorityMove(board, i, j, turn, lim)
    return pArr

def findMaxPositions(arr):
    maxVal = arr[0][0]
    maxPos = []
    count = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if arr[i][j] > maxVal:
                maxVal = arr[i][j]
                maxPos = []
                count = 0
            if arr[i][j] == maxVal:
                maxPos.append(Position(i, j))
                count += 1
    return (count, maxPos)


def getRandomPosition(positions, sizePosArr, turn):
    if len(positions) == 1:
        return positions[0]
    
    clone = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    clone2 = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    counter = 0
    oppoCounter = 0
    maxVal = 0
    maxi = 0

    for i in range(sizePosArr):
        clone = [row[:] for row in board]
        clone[positions[i].x][positions[i].y] = turn
        clone2 = priorityArray(clone, turn)

        for j in range(BOARD_SIZE):
            for k in range(BOARD_SIZE):
                if clone2[j][k] % 2 == 0:
                    counter += clone2[j][k]
                else:
                    oppoCounter += clone2[j][k]

        if maxVal < counter - oppoCounter:
            maxVal = counter - oppoCounter
            maxi = i
    return positions[maxi]

def refreshBoard():
    global board, lim, moveCounter
    lim = 2
    moveCounter = 0
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def printArrPretty(a):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if a[i][j] == 0:
                if board[i][j] != 0:
                    if board[i][j] == 1:
                        print('X', end='\t')
                    else:
                        print('O', end='\t')
                else:
                    print('', end='\t')
            else:
                print(a[i][j], end="\t")
        print("\n")

#hàm vẽ menu
def menu(title, options, callbacksAndParams):
    title_font_size = 60
    if(len(title) > 15):
        title_font_size = 60
    title_font = pygame.font.Font(custom_font_path_2, title_font_size)
    selected_option = 0  # Index of the currently selected option
    f = True
    line_space = 75
    while f:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = False
            elif event.type == pygame.KEYDOWN:
                switch_sound_1.play()
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == len(options) - 1:
                        f = False
                    else:
                        callback, params = callbacksAndParams[selected_option]
                        callback(*params)
        screen.fill(game_bg_color)
        text = title_font.render(title, True, white)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        screen.blit(text, text_rect)
        # Hiển thị menu
        for i, option in enumerate(options):
            text = font.render(option, True, white if i == selected_option else "gray")
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + i * line_space))
            screen.blit(text, text_rect)
        pygame.display.flip()

def move(turn, row, col):
    global moveCounter, lastMove
    moveCounter+=1
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == 0:
        board[row][col] = turn
        if moveCounter != 1:
            draw_cell(white, black, lastMove.x, lastMove.y)

            if turn != 1:
                poc_sound.play()
                draw_x(lastMove.x, lastMove.y)
            else:
                switch_sound.play()
                draw_o(lastMove.x, lastMove.y)

            draw_cell(last_move_cell_color, black, row, col)
        lastMove = Position(row, col)
        if turn == 1:
            switch_sound.play()
            draw_x(row, col)
        else:
            poc_sound.play()
            draw_o(row, col)
        pygame.display.flip()

        return True
    else:
        return False
#hàm chờ
def waiting_for_key():
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting_for_key = False
#chế độ chơi với bạn
def playWithFriend():
    global lim, moveCounter
    refreshBoard()
    isPlaying = True
    turn = 1
    draw_board()
    while isPlaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPlaying = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if mouseX < HEIGHT:
                    row = mouseY // SQUARE_SIZE
                    col = mouseX // SQUARE_SIZE
                    if move(turn, row, col):
                        turn = ot(turn)
                    
                    if check_win(board, row, col, turn):
                        win_player = "O" if turn == 1 else "X"
                        claps_sound.play()
                        draw_result_with_pc(f"{win_player} player win!")
                        waiting_for_key()
                        if pyautogui.confirm("Another game?") == "OK":
                            turn = 1
                            refreshBoard()
                            draw_board()
                        else:
                            isPlaying = False
                            return
        # Cập nhật màn hình
        pygame.display.flip()

def reset_time():
    global time_remaining
    clock.tick(15)
    time_remaining = current_level

#chế độ chơi với máy
def playWithPC(firstTurn):
    reset_time()
    refreshBoard()
    global moveCounter, lim, time_remaining
    count_down = False
    time_remaining = current_level
    draw_board()
    if firstTurn == 1:
        count_down = True
        move(1, BOARD_SIZE//2, BOARD_SIZE//2)
        turn = 2
        firstTurn = 10 # để ko lọt vào if này nữa
    else:
        turn = 1

    isPlaying = True
    while isPlaying:
        if count_down:
            clock.tick(15)
            time_remaining -= clock.get_time() / 1000  # convert milliseconds to seconds
            if time_remaining <= 0:
                time_remaining = current_level
                lose_sound.play()
                draw_result_with_pc("Time Is Up!")
                waiting_for_key()
                isPlaying = False

            # Render the countdown timer
            pygame.draw.rect(screen, dark_gray, (HEIGHT, 0, WIDTH - HEIGHT, HEIGHT))

            timer_text = font.render(f"Time: {int(time_remaining) if time_remaining > 1 else round(time_remaining, 2)}", True, white if time_remaining > 1 else red)
            timer_rect = timer_text.get_rect(center=(WIDTH - (WIDTH - HEIGHT)//2, 200))
            screen.blit(timer_text, timer_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPlaying = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos

                row = mouseY // SQUARE_SIZE
                col = mouseX // SQUARE_SIZE
                ######
                if move(turn, row, col):
                    count_down = False
                    time_remaining = current_level
                    if lim < 5 and moveCounter >= 4:
                        lim+=1
                    turn = ot(turn)

                    if check_win(board, row, col, turn):
                        time_remaining = current_level
                        win_sound.play()
                        draw_result_with_pc("You Win!")
                        waiting_for_key()
                        refreshBoard()
                        draw_board()
                        isPlaying = False
                    prioBoard = priorityArray(board, turn)
                    printArrPretty(prioBoard)
                    size, posArr = findMaxPositions(prioBoard)
                    p = getRandomPosition(posArr, size, turn)
                    x = p.x
                    y = p.y
                    if move(turn, x, y):
                        count_down = True
                        if lim < 5 and moveCounter >= 4:
                            lim+=1
                        turn = ot(turn)

                    if check_win(board, x, y, turn):
                        time_remaining = current_level
                        lose_sound.play()
                        draw_result_with_pc("Game Over!")
                        waiting_for_key()
                        refreshBoard()
                        draw_board()
                        isPlaying = False
        pygame.display.flip()
        # clock.tick(60)

def set_level(level):
    global current_level
    current_level = level
    options = ['You move first', 'PC moves first', 'Quit']
    turn = 1
    callbacksAndParams = [(playWithPC, (2,)), (playWithPC, (1,))]
    menu("Who moves first?", options, callbacksAndParams)

def playWithPCMenu():
    level_options = ['Super Easy', 'Easy', 'Medium', 'Hard', 'Nightmare', 'Quit']
    level_callbacks_and_params = [(set_level, (time_remaining_super_easy_mode,)), (set_level, (time_remaining_easy_mode,)), (set_level, (time_remaining_medium_mode,)), (set_level, (time_remaining_hard_mode,)), (set_level, (time_remaining_nightmare_mode,))]
    menu("Level", level_options, level_callbacks_and_params)

def main():
    turn = 1
    options = ['Friend', 'Computer', 'Quit']
    callbacksAndParams = [(playWithFriend, ()), (playWithPCMenu, ())]

    menu("Play with?", options, callbacksAndParams)
    
    

if __name__ == "__main__":
    main()