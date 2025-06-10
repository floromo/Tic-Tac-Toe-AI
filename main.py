from ai import call_gpt
from graphics import Canvas

# ========== const variables ==========
canvasWidth = 600
canvasHeight = 600
border = 100


# ========== main ==========
def main():
    canvas = Canvas(canvasWidth, canvasHeight)
    drawTitle(canvas)
    drawBoard(canvas)

    tryAgain = canvas.create_text(canvasWidth-200, canvasHeight-50, text = "Try Again.", font_size = 30, color = "red")
    canvas.set_hidden(tryAgain, True)

    turn = canvas.create_text(30, canvasHeight-50, text = "Your turn.", font_size = 30, color = "red")
    yourTurn = 1

    board = [["","",""],["","",""],["","",""]]

    while not fullCheck(board) and not winCheck(board, "OOO") and not winCheck(board, "XXX"):                     # while the board is not full
        if yourTurn == 1:
            you(canvas, board, yourTurn, tryAgain, turn)
        else:
            opp(canvas, board, yourTurn, turn)
        yourTurn *= -1
    if winCheck(board, "OOO"):
        print("You win!")
        canvas.change_text(turn, "You win!")
    elif winCheck(board, "XXX"):
        print("You lose!")
        canvas.change_text(turn, "You lose!")
    else:
        print("It's a tie!")
        canvas.change_text(turn, "It's a tie!")


# ========== draw canvas ==========
def drawTitle(canvas):
    title = canvas.create_text(30, 30, text = "Tic Tac Toe", font_size = 30)

def drawTurn(canvas, yourTurn, turn):
    if yourTurn == 1:
        canvas.change_text(turn, "Your turn.")
    else:
        canvas.change_text(turn, "AI's turn.")

def drawX(canvas, x, y):
    size = 100
    cross = canvas.create_text(x-25,y-size/2, text="x", font_size=size)

def drawO(canvas, x, y):
    size = 100
    cross = canvas.create_text(x-25,y-size/2, text="o", font_size=size)

def drawBoard(canvas):
    vert2 = canvas.create_line(canvasWidth/3+27, border, canvasWidth/3+27, canvasHeight-border)
    vert3 = canvas.create_line(2*canvasWidth/3-27, border, 2*canvasWidth/3-27, canvasHeight-border)
    vert4 = canvas.create_line(3*canvasWidth/3-border, border, 3*canvasWidth/3-border, canvasHeight-border)
    vert1 = canvas.create_line(canvasWidth/3-border, border, canvasWidth/3-border, canvasHeight-border)
    horz2 = canvas.create_line(border, canvasHeight/3+27, canvasWidth-border, canvasHeight/3+27)
    horz3 = canvas.create_line(border, 2*canvasHeight/3-27, canvasWidth-border, 2*canvasHeight/3-27)
    horz1 = canvas.create_line(border, canvasHeight/3-border, canvasWidth-border, canvasHeight/3-border)
    horz4 = canvas.create_line(border, 3*canvasHeight/3-border, canvasWidth-border, 3*canvasHeight/3-border)


# ========== input ==========

def rowPosition(click):
    if click[0] > canvasWidth/3-border and click[0] < canvasWidth/3+27:
        return 160
    elif click[0] > canvasWidth/3+27 and click[0] < 2*canvasWidth/3-27:
        return 300
    elif click[0] > 2*canvasWidth/3-27 and click[0] < 3*canvasWidth/3-border:
        return 435
    else:
        return -1

def colPosition(click):
    if click[1] > canvasHeight/3-border and click[1] < canvasHeight/3+27:
        return 160
    elif click[1] > canvasHeight/3+27 and click[1] < 2*canvasHeight/3-27:
        return 300
    elif click[1] > 2*canvasHeight/3-27 and click[1] < 3*canvasHeight/3-border:
        return 435
    else:
        return -1

def colInput(click):
    if click[0] > canvasWidth/3-border and click[0] < canvasWidth/3+27:
        return 0
    elif click[0] > canvasWidth/3+27 and click[0] < 2*canvasWidth/3-27:
        return 1
    elif click[0] > 2*canvasWidth/3-27 and click[0] < 3*canvasWidth/3-border:
        return 2

def rowInput(click):
    if click[1] > canvasHeight/3-border and click[1] < canvasHeight/3+27:
        return 0
    elif click[1] > canvasHeight/3+27 and click[1] < 2*canvasHeight/3-27:
        return 1
    elif click[1] > 2*canvasHeight/3-27 and click[1] < 3*canvasHeight/3-border:
        return 2

def you(canvas, board, yourTurn, tryAgain, turn):
    canvas.wait_for_click()
    click = canvas.get_last_click() 
    clickCondition = checkClick(click)
    while not clickCondition:
        canvas.wait_for_click()
        click = canvas.get_last_click() 
        clickCondition = checkClick(click)
    row = rowInput(click)
    col = colInput(click)
    moveCondition = checkMove(row, col, board)
    while not moveCondition:
        canvas.set_hidden(tryAgain, False)
        canvas.wait_for_click()
        click = canvas.get_last_click()
        row = rowInput(click)
        col = colInput(click)
        moveCondition = checkMove(row, col, board)
    canvas.set_hidden(tryAgain, True)
    board[row][col] = "O"
    drawO(canvas,rowPosition(click),colPosition(click))
    drawTurn(canvas, yourTurn, turn)

def checkMove(row, col, board):
    if board[row][col] == "":
        return True
    else:
        return False

def checkClick(click):
    if rowPosition(click) == -1 or colPosition(click) == -1:
        return False
    else:
        return True
        
def opp(canvas, board, yourTurn, turn):
    response = call_gpt(f"Play tic tac toe given the following board (given in the form of a numpy matrix): {board}. You are player X and you are trying to win and prevent me from winning. To play your turn, please return 2 numbers in the following format: row, column. DO NOT RETURN ANYTHING ELSE, JUST THOSE TWO NUMBERS IN THAT FORMAT. ALSO, DO NOT OVERRIDE A PLAYER'S MOVE.")     
    arr = stringToIntArr(response)
    condition = checkMove(arr[0], arr[1], board)
    while not condition:
        response = call_gpt(f"Play tic tac toe given the following board (given in the form of a numpy matrix): {board}. You are player X and you are trying to win and prevent me from winning. To play your turn, please return 2 numbers in the following format: row, column. DO NOT RETURN ANYTHING ELSE, JUST THOSE TWO NUMBERS IN THAT FORMAT. ALSO, DO NOT OVERRIDE A PLAYER'S MOVE.")     
        arr = stringToIntArr(response)
        condition = checkMove(arr[0], arr[1], board)
    board[arr[0]][arr[1]] = "X"
    if arr[0] == 0:
        if arr[1] == 0:
            drawX(canvas, 160, 160)
        elif arr[1] == 1:
            drawX(canvas, 300, 160)
        else:
            drawX(canvas, 435, 160)
    elif arr[0] == 1:
        if arr[1] == 0:
            drawX(canvas, 160, 300)
        elif arr[1] == 1:
            drawX(canvas, 300, 300)
        else:
            drawX(canvas, 435, 300)
    else:
        if arr[1] == 0:
            drawX(canvas, 160, 435)
        elif arr[1] == 1:
            drawX(canvas, 300, 435)
        else:
            drawX(canvas, 435, 435)
    drawTurn(canvas, yourTurn, turn)


def stringToIntArr(str):                        # turns chatgpt's response into an int array
    strList = str.split(", ")
    intArr = [int(num) for num in strList]
    return intArr

# ========== checking win ==========

def fullCheck(board):                           # checks if the board is full
    for row in board:
        for col in row:
            if col == "":
                return False
    return True

def rowCheck(board, player):
    temp = ""
    for row in board:
        temp = "".join(row)
        if temp == player:
            return True
        temp = ""
    return False

def colCheck(board, player):
    temp = ""
    for col in range(3):
        for row in range(3):
            temp = temp+board[row][col]
        if temp == player:
            return True
        temp = ""
    return False

def diagCheckLeft(board,player):
    temp = ""
    for i in range(3):
        temp = temp+board[i][i]
    if temp == player:
        return True
    return False

def diagCheckRight(board, player):
    temp = ""
    j = 0
    for i in range(2, -1, -1):
        temp = temp+board[i][j]
        j += 1
    if temp == player:
        return True
    return False

def winCheck(board, player):
    condition1 = rowCheck(board, player)
    condition2 = colCheck(board, player)
    condition3 = diagCheckLeft(board, player)
    condition4 = diagCheckRight(board, player)
    return (condition1 or condition2 or condition3 or condition4)


# ========== main function ==========


if __name__ == "__main__":
    main()
