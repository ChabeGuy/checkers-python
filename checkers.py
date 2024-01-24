import colorama
columnsLetters = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

# The class for the game pieces. Contains board side,
# promotion status, coloring, and symbol.
class Piece():
    def __init__(self, side):
        self.side = side
        self.pms = False
        self.color = colorama.Fore.RED if side == "red" else colorama.Fore.BLUE
        self.bg = colorama.Back.BLACK
        self.symbol = "O"

# The class for the empty spaces. Contains coloring and symbol.
class Space():
    def __init__(self):
        self.color = colorama.Fore.WHITE
        self.bg = colorama.Back.WHITE
        self.symbol = " "

# Board creation. Generates a full board of spaces.
num = 0
board = []
for i in range(8):
    row = []
    for j in range(8):
        row.append(Space())
    board.append(row)

# The function that displays the board. It checks and changes
# fore and background colors as needed, then prints the board.
def display_board(board = board):
    offset = 0
    print("  " + " ".join([x for x in columnsLetters]))
    for row in range(len(board)):
        for space in range(len(board[row])):
            currentTile = board[row][space]
            if (space + offset) % 2 == 1:
                currentTile.bg = colorama.Back.BLACK
            else:
                currentTile.bg = colorama.Back.WHITE
            if isinstance(currentTile, Space):
                if (space + offset) % 2 == 1:
                    currentTile.color = colorama.Fore.BLACK
                else:
                    currentTile.color = colorama.Fore.WHITE
        offset += 1
        print(f"{row + 1} " + " ".join([f"{x.color}{x.bg}{x.symbol}{colorama.Fore.BLACK}{colorama.Back.BLACK}" for x in board[row]]))

def move_piece(startx, starty, destx, desty, board = board):
    board[desty][destx] = board[starty][startx]
    board[starty][startx] = Space()
    if (turn == "blue" and desty == 0) or (turn == "red" and desty == 7):
        board[desty][destx].pms = True
        board[desty][destx].symbol = "K"
        print("Piece promoted!")

def jump_piece(startx, starty, destx, desty, udDir, lrDir, board = board):
    move_piece(startx, starty, (destx + lrDir), (desty + udDir))
    board[desty][destx] = Space()

def check_jump(piecex, piecey, udDir, board = board):
    while True:
        jumped = False
        if board[piecey][piecex].pms:
            for ud in range(-1, 2, 2):
                if piecey >= 6 and ud == 1: continue
                elif piecey <= 1 and ud == -1: continue
                for lr in range(-1, 2, 2):
                    if piecex <= 1 and lr == -1: continue
                    elif piecex >= 6 and lr == 1: continue
                    if isinstance(board[piecey + ud][piecex + lr], Piece) and isinstance(board[piecey + (2*ud)][piecex + (2*lr)], Space):
                        if board[piecey+ud][piecex+lr].side == turn: continue
                        columnLetter = next(i for i in columnsLetters if columnsLetters[i] == (piecex + lr))
                        while True:
                            jumpChoice = input(f"Would you like to jump the piece at {piecey+1+ud}{columnLetter}? ").lower()
                            if jumpChoice == "yes":
                                jump_piece(piecex, piecey, (piecex + lr), (piecey + ud), ud, lr)
                                jumped = True
                                piecex += (2*lr)
                                piecey += (2*ud)
                                break
                            elif jumpChoice == "no":
                                break
                            else:
                                print("Please choose yes or no.")    
                        if jumped:
                            break
                if jumped:
                    break
        else:
            for lr in range(-1, 2, 2):
                if piecex <= 1 and lr == -1: continue
                elif piecex >= 6 and lr == 1: continue
                if isinstance(board[piecey + udDir][piecex + lr], Piece) and isinstance(board[piecey + (2*udDir)][piecex + (2*lr)], Space):
                    if board[piecey+udDir][piecex+lr].side == turn: continue
                    columnLetter = next(i for i in columnsLetters if columnsLetters[i] == (piecex + lr))
                    while True:
                        display_board(board)
                        jumpChoice = input(f"Would you like to jump the piece at {piecey+1+udDir}{columnLetter}? ").lower()
                        if jumpChoice == "yes":
                            jump_piece(piecex, piecey, (piecex + lr), (piecey + udDir), udDir, lr)
                            jumped = True
                            piecex += (2*lr)
                            piecey += (2*udDir)
                            break
                        elif jumpChoice == "no":
                            break
                        else:
                            print("Please choose yes or no.")
                    if jumped:
                        break
        if not jumped:
            break

def check_win(board = board):
    for row in board:
        for space in row:
            if isinstance(space, Piece):
                if space.side != turn:
                    return False
    return True

def take_turn():
    while True:
        # The player inputs a row and column value, choosing a piece.
        while True:
            while True:
                try:
                    chosenRow = int(input("Row: "))
                    if chosenRow > 8 or chosenRow < 1:
                        print("Input a valid row.")
                    else:
                        chosenRow -= 1
                        break
                except ValueError:
                    print("Input a valid row.")
            while True:
                try:
                    chosenColumn = columnsLetters[input("Column: ")]
                    break
                except KeyError:
                    print("Input a valid column.")
            if isinstance(board[chosenRow][chosenColumn], Piece): 
                if board[chosenRow][chosenColumn].side == turn: 
                    break
                else:
                    print("Choose one of your own pieces!")
            else:
                print("Please choose a valid piece.")
        chosenPiece = board[chosenRow][chosenColumn]
        # Checks whether the player can move left and/or right.
        forcedLeft = True if chosenColumn == 7 else False
        forcedRight = True if chosenColumn == 0 else False
        # Determines up/down movement direction
        if not chosenPiece.pms:
            udDir = -1 if turn == "blue" else 1
        else:
            if chosenRow == 0:
                udDir = 1
            elif chosenRow == 7:
                udDir = -1
            else:
                while True:
                    chooseDir = input("Move up or down?").lower()
                    if chooseDir == "up":
                        udDir = -1
                    elif chooseDir == "down":
                        udDir  = 1
                    else:
                        print("Choose a valid direction.")
                        continue
                    break
        # Determines left/right movement direction and movement type
        lrDir = 0
        movementType = "move"
        while True:
            # Checks whether either direction is blocked
            if forcedRight:
                lrDir = 1
            elif forcedLeft:
                lrDir = -1
            # If neither direction is blocked, asks for input
            else:
                moveChoice = input("Left or right? ").lower() 
                if moveChoice == "left":
                    lrDir = -1
                elif moveChoice == "right":
                    lrDir = 1
                else:
                    print("Choose a valid direction.")
                    continue
            # Checks if there's a piece to jump over.
            if not isinstance(board[chosenRow + udDir][chosenColumn + lrDir], Space):
                if board[chosenRow + udDir][chosenColumn + lrDir].side != turn and isinstance(board[chosenRow + (2 * udDir)][chosenColumn + (2 * lrDir)], Space):
                    if turn == "blue" and not board[chosenRow][chosenColumn].pms and chosenRow != 1:
                        movementType = "jump"
                    elif turn == "red" and not board[chosenRow][chosenColumn].pms and chosenRow != 6:
                        movementType = "jump"
                    else:
                        print("You can't move in that direction!")
                        movementType = "none"
                else:
                    print("You can't move in that direction!")
                    movementType = "none"
            break
        # Depending on the result, either moves, jumps, or asks again for inputs.
        if movementType == "move":
            move_piece(chosenColumn, chosenRow, chosenColumn + lrDir, chosenRow + udDir)
            break
        elif movementType == "jump":
            check_jump(chosenColumn, chosenRow, udDir)
            if not isinstance(board[chosenRow][chosenColumn], Piece): break
            else: continue
        else:
            continue

# Places the starting pieces on the board. Deletes
# the previous space objects and places pieces in their stead.
for row in range(len(board)):
    for space in range(len(board[i])):
        currentTile = board[row][space]
        if row < 3:
            if (space + num) % 2 == 1:
                del currentTile
                board[row][space] = Piece("red")
        elif row > 4:
            if (space + num) % 2 == 1:
                del currentTile
                board[row][space] = Piece("blue")
    num += 1

# Sets the first turn
turn = "blue"

# Main gameplay loop.
try:
    while True:
        turnColor = colorama.Fore.BLUE if turn == "blue" else colorama.Fore.RED
        print(f"{turnColor}{turn[0].upper()}{turn[1:]}'s turn!{colorama.Fore.BLACK}")
        display_board(board)
        take_turn()
        if check_win:
            break
        if turn == "red":
            turn = "blue"
        else:
            turn = "red"
except KeyboardInterrupt:
    print("Game cancelled.")

print(f"{turnColor}{turn[0].upper()}{turn[1:]} wins!{colorama.Fore.BLACK}")


