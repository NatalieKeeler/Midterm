# chess.py
# Full chess game with rules, timer, winner, and piece sprites
# edits include Castling and a rewording the turn indicator
# Although people reported that players couldn’t get out of check by capturing a piece, I found
# that a color could be in check and still capture a piece.
# 25 Feb 2026

BOARD_SIZE = 8
SQUARE = 80

WIDTH = BOARD_SIZE * SQUARE
HEIGHT = BOARD_SIZE * SQUARE + 60

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

turn = "White"
selected = None

wk_moved = False
bk_moved = False
wr_moved_qs = False
wr_moved_ks = False
br_moved_qs = False
br_moved_ks = False

is_castling = False

white_time = 300  # 5 minutes
black_time = 300

game_over = False
winner = ""

# -----------------------------------
# Board setup
# -----------------------------------
board = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp"]*8,
    [".."]*8,
    [".."]*8,
    [".."]*8,
    [".."]*8,
    ["wp"]*8,
    ["wr","wn","wb","wq","wk","wb","wn","wr"]
]

# Load piece images
piece_images = {}
for color in ["w","b"]:
    for ptype in ["p","r","n","b","q","k"]:
        key = color+ptype
        piece_images[key] = key

# -----------------------------------
# Draw board
# -----------------------------------

def draw_row(row_index, c1, c2):
    y = row_index * SQUARE
    for col in range(BOARD_SIZE):
        x = col * SQUARE
        color = c1 if col % 2 == 0 else c2
        rect = Rect(x, y, SQUARE, SQUARE)
        screen.draw.filled_rect(rect, color)

def draw_board():
    for row in range(BOARD_SIZE):
        if row % 2 == 0:
            draw_row(row, LIGHT, DARK)
        else:
            draw_row(row, DARK, LIGHT)

# -----------------------------------
# Draw pieces
# -----------------------------------

def draw_pieces():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece = board[r][c]
            if piece != "..":
                screen.blit(piece, (c*SQUARE, r*SQUARE))

# Notice that: Screen coordinates use (x, y)
# x = horizontal = column(c), y = vertical = row(r)

# -----------------------------------
# Draw selection
# -----------------------------------

def draw_selection():
    if selected:
        r, c = selected
        rect = Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE)
        screen.draw.rect(rect, (0,255,0)) #draw green rectangle around selected square

# -----------------------------------
# Chess Logic
# -----------------------------------
def path_clear(sr, sc, tr, tc):
    dr = tr - sr
    dc = tc - sc
    steps = max(abs(dr), abs(dc))
    step_r = (dr // steps) if dr != 0 else 0
    step_c = (dc // steps) if dc != 0 else 0

# -----------------------------------
	# •	sr = start row
	# •	sc = start column
	# •	tr = target row
	# •	tc = target column
  # When determining movement direction on the board,
  # the values of step_r (row step) and step_c (column step)
  # indicate how the position changes at each step along the path.
  # 1. moving to the right means there is no change in rows but an increase in columns,
  #    so step_r = 0 and step_c = 1.
  # 2. Moving to the left also keeps the row the same but decreases the column,
  #    giving step_r = 0 and step_c = -1.
  # 3. Moving down increases the row while keeping the column unchanged,
  #    so step_r = 1 and step_c = 0,
  # 4. moving up decreases the row with no column change,
  #    resulting in step_r = -1 and step_c = 0.
  # 5. For a diagonal movement such as down-right,
  #    both the row and column increase together,
  #    so step_r = 1 and step_c = 1.
  # These step values allow the program to advance square-by-square in the correct direction
  # when checking movement paths.
# -----------------------------------

    for i in range(1, steps): #repeat for each square, except the starting and ending squares
        r = sr + i*step_r
        c = sc + i*step_c
        if board[r][c] != "..": #checks if a piece is on the square being checked
            return False
    return True

def can_piece_reach(sr, sc, tr, tc):
    piece = board[sr][sc]
    # if statement checks if a piece is at the starting location
    if piece == "..":
        return False

    p = piece[1]  # identify piece type
    dr = tr - sr  # calculate vertical distance
    dc = tc - sc  # calculate horizontal distance

    # pawn
    if p == "p":
        color = piece[0] # get pawn color
        direction = -1 if color == "w" else 1 # legal movement direction based on color
        return abs(dc) == 1 and dr == direction

    # rook
    if p == "r":
        return (sr == tr or sc == tc) and path_clear(sr, sc, tr, tc)

    # Bishop
    if p == "b":
        return abs(dr) == abs(dc) and path_clear(sr, sc, tr, tc)

    # queen
    if p == "q":
        return (sr == tr or sc == tc or abs(dr) == abs(dc)) and path_clear(sr, sc, tr, tc)

    # Knight
    if p == "n":
        return (abs(dr), abs(dc)) in [(2,1),(1,2)]

    # king
    if p == "k":
        return max(abs(dr), abs(dc)) == 1 and path_clear(sr, sc, tr, tc)

    return False

def is_square_attacked(row, col, by_color):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE): #check all squares on the board
            piece = board[r][c]
            if piece != ".." and piece[0] == by_color:
                # can the opposing piece reach the square from the selected position
                if can_piece_reach(r,c,row,col):
                    return True
    return False

def find_king(color):
    king_piece = ("w" if color=="White" or color=="w" else "b") + "k"
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == king_piece:
                return (r,c)
    return None

def is_in_check(color):
    king_pos = find_king(color)
    if king_pos is None:
        return False
    opponent = "b" if color == "White" or color == "w" else "w"
    return is_square_attacked(king_pos[0], king_pos[1], opponent)

def would_be_in_check(sr, sc, tr, tc, color):
    original_piece = board[tr][tc] # save the original state of the target sqaure

    #temporaly make the supposed move
    board[tr][tc] = board[sr][sc]
    board[sr][sc] = ".."

    in_check = is_in_check(color)

    # reset the board after checking
    board[sr][sc] = board[tr][tc]
    board[tr][tc] = original_piece

    return in_check


def can_castle(color,side):

    if color == "w" and wk_moved == False:
        if side == "ks" and wr_moved_ks == False:
            if can_piece_reach(7, 7, 7, 4) and is_square_attacked(7,3,"Black"):
                return True
        if side == "qs" and wr_moved_qs == False:
            if can_piece_reach(7, 0, 7, 4) and is_square_attacked(7,5,"Black"):
                return True

    if color == "b" and bk_moved == False:
        if side == "ks" and br_moved_ks == False:
            if can_piece_reach(0,7,0,4) and is_square_attacked(7,3,"White"):
                return True
        if side == "qs" and br_moved_qs == False:
            if can_piece_reach(0, 0, 0, 4) and is_square_attacked(7,5,"White"):
                return True
    return False



def valid_move(sr, sc, tr, tc):
    global is_castling
    piece = board[sr][sc]
    target = board[tr][tc]

    if piece == "..":
        return False

    color = piece[0]
    p = piece[1]

    # can't capture your own pieces or a king
    if target != ".." and target[0] == color:
        return False

    if target != ".." and target[1] == "k":
        return False

    dr = tr - sr
    dc = tc - sc
    is_legal = False
    is_castling = False

    if p == "p":
        direction = -1 if color=="w" else 1
        start_row = 6 if color=="w" else 1

        if dc==0 and dr==direction and target=="..":
            is_legal=True
        elif dc==0 and sr==start_row and dr==2*direction and board[sr+direction][sc]==".." and target=="..":
            is_legal=True
        elif abs(dc)==1 and dr==direction and target!="..":
            is_legal=True

    elif p == "r":
        if (sr==tr or sc==tc) and path_clear(sr,sc,tr,tc):
            is_legal=True

    elif p == "b":
        if abs(dr)==abs(dc) and path_clear(sr,sc,tr,tc):
            is_legal=True

    elif p == "q":
        if (sr==tr or sc==tc or abs(dr)==abs(dc)) and path_clear(sr,sc,tr,tc):
            is_legal=True

    elif p == "n":
        if (abs(dr),abs(dc)) in [(2,1),(1,2)]:
            is_legal=True

    elif p == "k":
        opponent = "b" if color=="w" else "w"
        if max(abs(dr),abs(dc))==1 and not is_square_attacked(tr,tc,opponent):
            is_legal=True
        if dr == 0 and dc == 2 and can_castle(color,"ks"):
            if not (is_square_attacked(tr, tc, opponent) or is_in_check(color)):
                is_legal=True
                is_castling = True
        if dr == 0 and dc == -2 and can_castle(color,"qs"):
            if not (is_square_attacked(tr, tc, opponent) or is_in_check(color)):
                is_legal=True
                is_castling = True

    if not is_legal:
        return False


    if would_be_in_check(sr,sc,tr,tc,color):
        return False

    return True

# check if any of a player's pieces can move legally
def has_legal_moves(color):
    for sr in range(BOARD_SIZE):
        for sc in range(BOARD_SIZE):
            piece = board[sr][sc]
            if piece!=".." and ((color=="White" and piece[0]=="w") or (color=="Black" and piece[0]=="b")):
                for tr in range(BOARD_SIZE):
                    for tc in range(BOARD_SIZE):
                        if valid_move(sr,sc,tr,tc):
                            return True
    return False

# -----------------------------------
# Mouse input
# -----------------------------------

def on_mouse_down(pos):
    global selected, turn, game_over, winner, is_castling
    global wk_moved, wr_moved_ks, wr_moved_qs, br_moved_ks, br_moved_qs, bk_moved

    # dont accept inputs if the game has ended
    if game_over:
        return

    # determine selected square (pos stores mouse position as a coordinate pair)
    c = int(pos[0]//SQUARE)
    r = int(pos[1]//SQUARE)

    if selected is None:
        piece = board[r][c]
        if piece!=".." and ((turn=="White" and piece[0]=="w") or (turn=="Black" and piece[0]=="b")):
            selected=(r,c)
    else:
        sr,sc = selected
        if valid_move(sr,sc,r,c):

            # Move piece
            board[r][c] = board[sr][sc]
            board[sr][sc] = ".."

            # ✅ Pawn Promotion
            # Pawns can promote to any piece exept a pawn or king,
            # but people usually promote to a queen
            moved_piece = board[r][c]
            if moved_piece == "wp" and r == 0:
                board[r][c] = "wq"
            elif moved_piece == "bp" and r == 7:
                board[r][c] = "bq"

            # logic for determining if kings/rooks have moved
            elif moved_piece == "wk":
                wk_moved = True
            elif moved_piece == "wr" and sc == 7:
                wr_moved_ks = True
            elif moved_piece == "wr" and sc == 0:
                wr_moved_qs = True
            elif moved_piece == "bk":
                bk_moved = True
            elif moved_piece == "br" and sc == 7:
                br_moved_ks = True
            elif moved_piece == "br" and sc == 0:
                br_moved_qs = True

            # if castling, move the rook
            if is_castling == True:
                if r == 7 and c == 6:
                    board[7][5] = board[7][7]
                    board[7][7] = ".."
                if r == 0 and c == 6:
                    board[0][5] = board[0][7]
                    board[0][7] = ".."
                if r == 7 and c == 2:
                    board[7][3] = board[7][0]
                    board[7][0] = ".."
                if r == 0 and c == 2:
                    board[0][3] = board[0][0]
                    board[0][0] = ".."
                is_castling = False


            # Next player's turn
            turn = "Black" if turn=="White" else "White"

            # if the next player cant move and is in check, they lose
            # if they arnt in check, the game ends in a draw
            if not has_legal_moves(turn):
                game_over=True
                if is_in_check(turn):
                    winner = "Black" if turn=="White" else "White"
                else:
                    winner="draw"

        # Reset the selection
        selected=None

# -----------------------------------
# Timer update
# -----------------------------------

def update():
    global white_time, black_time, game_over, winner

    # stop timing when the game ends
    if game_over:
        return

    if turn=="White":
        white_time -= 1/60 # Update runs 60 times a second
        if white_time<=0:
            winner="Black"
            game_over=True
    else:
        black_time -= 1/60
        if black_time<=0:
            winner="White"
            game_over=True

# -----------------------------------
# Draw everything
# -----------------------------------

def draw():
    screen.clear()
    draw_board()
    draw_selection()
    draw_pieces()

    # Show whose turn it is
    screen.draw.text(f"{turn} to move", (10, HEIGHT-55), fontsize=30, color="White")
    # Show each player's remaining time (in seconds)
    screen.draw.text(f"W:{int(white_time)}  B:{int(black_time)}", (200, HEIGHT-55), fontsize=30, color="White")

    # tell the current player if they are in check
    if not game_over and is_in_check(turn):
        screen.draw.text("CHECK!", (WIDTH-150, HEIGHT-55), fontsize=35, color="red")

    # Show who won when the game ends
    if game_over:
        if winner=="draw":
            screen.draw.text("STALEMATE!", center=(WIDTH/2, HEIGHT-25), fontsize=40, color="yellow")
        else:
            screen.draw.text(f"{winner.upper()} WINS!", center=(WIDTH/2, HEIGHT-25), fontsize=40, color="yellow")