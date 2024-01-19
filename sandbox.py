import colorama
columnsLetters = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

# The class for the game pieces. Contains board side,
# promotion status, coloring, and symbol.
class Piece():
    def __init__(self, side):
        self.side = side
        self.pms = False
        self.color = colorama.Fore.RED if side == "top" else colorama.Fore.BLUE
        self.bg = colorama.Back.BLACK
        self.symbol = "O"

        def promote():
            self.symbol = "K"

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
    currentPiece = board[starty][startx]
    destPiece = board[desty][destx]
    currentPiece, destPiece = destPiece, currentPiece

def take_turn():
    # The player inputs a row and column value, choosing a piece.
    while True:
        chosenRow = int(input("Row: ")) - 1
        if chosenRow > 8 or chosenRow < 1:
            print("Input a valid row.")
        else:
            break
    while True:
        try:
            chosenColumn = columnsLetters[input("Column: ")]
            break
        except KeyError:
            print("Input a valid column.")
    chosenPiece = board[chosenRow][chosenColumn]
    # Checks whether the player can move left and/or right.
    left = -1 if chosenColumn != 0 else 0
    right = 1 if chosenColumn != 7 else 0
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
    # Determines left/right movement direction
    lrDir = 0
    while True:
        # Checks whether either direction is blocked
        if not left:
            lrDir = 1
            break
        elif not right:
            lrDir = -1
            break
        # If neither directions is blocked, asks for input
        moveChoice = input("Left or right?").lower() 
        if moveChoice == "left":
            lrDir = -1
            break
        elif moveChoice == "right":
            lrDir = 1
            break
        else:
            print("Choose a valid direction.")
    move_piece(chosenColumn, chosenRow, chosenColumn + lrDir, chosenRow + udDir)

# Places the starting pieces on the board. Deletes
# the previous space objects and places pieces in their stead.
for row in range(len(board)):
    for space in range(len(board[i])):
        currentTile = board[row][space]
        if row < 3:
            if (space + num) % 2 == 1:
                del currentTile
                board[row][space] = Piece("top")
        elif row > 4:
            if (space + num) % 2 == 1:
                del currentTile
                board[row][space] = Piece("bottom")
    num += 1

# Sets the first turn
turn = "blue"

while True:
    print(f"{turn[0].upper()}{turn[1:]}'s turn!")
    display_board(board)
    take_turn()
    if turn == "red":
        turn = "blue"
    else:
        turn = "red"


