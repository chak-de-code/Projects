from tkinter import *

root = Tk()
root.title("Tic Tac Toe")
root.geometry("500x500")

frame1 = Frame(root,relief="solid",borderwidth=3)
frame1.pack()

titlelabel = Label(frame1,text="Tic Tac Toe",font=("arial",30),bg="orange",width=13)
titlelabel.grid(row=0,column=0,columnspan=3)

# initial values of the board we can track the position of player move using this dictionary
# board = {1:" ",2:" ",3:" ",4:" ",5:" ",6:" ",7:" ",8:" ",9:" "}
board = {i : " " for i in range(1,10)}
turn = "x"

def checkforwin(player):
    # all rows
    if (board[1] == board[2] == board[3] == player or
        board[4] == board[5] == board[6] == player or
        board[7] == board[8] == board[9] == player or
        board[1] == board[4] == board[7] == player or
        board[2] == board[5] == board[8] == player or
        board[3] == board[6] == board[9] == player or
        board[1] == board[5] == board[9] == player or
        board[3] == board[5] == board[7] == player):
        return True
    return False

def checkdraw():
    for x in board.keys():
        if board[x] == " ":
            return False

    return True
    
def restartgame():
    for button in buttons:
        button["text"]=" "

    for i in board.keys():
        board[i] = " "

    titlelabel = Label(frame1,text="Tic Tac Toe",font=("arial",30),bg="orange",width=13)
    titlelabel.grid(row=0,column=0,columnspan=3)


def play(event):
    global turn
    button = event.widget

# track which button is pressed
    # button belongs to <class 'tkinter.button'>
    buttontext = str(button)
    clicked = buttontext[-1]            # we access only the button number (let say 5 using it from .!frame2.!button5 )
    
    if clicked == 'n':
        clicked = 1
    else:
        clicked = int(clicked)
    # ensure that we cannot over write x or o
    if button["text"]==" ":
        if turn == "x":
            button["text"]="X"
            board[clicked]=turn
            if checkforwin(turn):
                winlabel= Label(frame1 ,text=f"{turn} wins the game",font=("arial",30),bg="orange",width=13)
                winlabel.grid(row=0,column=0,columnspan=3)
            # fill the clicked value in the dict for tracking the board
            turn = "o"
        else:
            button["text"]="O"
            board[clicked]= turn
            if checkforwin(turn):
                winlabel=Label(frame1,text=f"{turn} wins the game",font=("arial",30),bg="orange",width=13)
                winlabel.grid(row=0,column=0,columnspan=3)
            turn = "x"

    if checkdraw():
        drawlabel = Label(frame1,text=f"Game Draw",font=("arial",25),bg="pink",width=13)
        drawlabel.grid(row=0,column=0,columnspan=3)
    


# Buttons
frame2 = Frame(root)
frame2.pack()

buttons = []
for i in range(3):                      # for rows
    for j in range(3):                  # for columns
        button = Button(frame2,text=" ",width=4,height=2,font=("arial",30),bg="light blue",relief="raised",borderwidth=5)
        button.grid(row=i,column=j)
        button.bind("<Button-1>",play)
        buttons.append(button)


# restart button
restart = Button(frame2,text=f"Restart",width=19,height=1,font=("arial",20),bg="light green",relief="sunken",borderwidth=5,command=restartgame)
restart.grid(row=4,column=0,columnspan=3)

root.mainloop()