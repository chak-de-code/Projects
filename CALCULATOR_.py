from tkinter import *

root = Tk()
root.title("Calculator")
root.geometry("570x600")
root.resizable(False,False)
root.configure(bg="#17161b")

label_result = Label(root,width=25,height=2,text="",font=("arial",30))
label_result.pack()

equation = ""

def show(value):
    global equation
    equation += value
    label_result.config(text=equation)

def clear():
    global equation
    equation = ""
    label_result.config(text=equation)

def calculate():
    global equation
    try:
        result = eval(equation)
        equation = str(result)
        label_result.config(text=equation)
    except ZeroDivisionError:
        label_result.config(text="Error!")  # or "division by zero"
        equation = ""
    except:
        label_result.config(text="Error!")
        equation = ""

def create_button(text, x, y, width=5, height=1, bg="#2a2d36", fg="#fff", font=("arial", 30, "bold"), command=None):
    Button(root, text=text, width=width, height=height, font=font, bd=1, fg=fg, bg=bg, command=command).place(x=x, y=y)

create_button("C", 10, 100, bg="#3697f5", command=clear)
create_button("/", 150, 100, command=lambda: show("/"))
create_button("%", 290, 100, command=lambda: show("%"))
create_button("*", 430, 100, command=lambda: show("*"))

create_button("7", 10, 200, command=lambda: show("7"))
create_button("8", 150, 200, command=lambda: show("8"))
create_button("9", 290, 200, command=lambda: show("9"))
create_button("-", 430, 200, command=lambda: show("-"))

create_button("6", 10, 300, command=lambda: show("6"))
create_button("5", 150, 300, command=lambda: show("5"))
create_button("4", 290, 300, command=lambda: show("4"))
create_button("+", 430, 300, command=lambda: show("+"))

create_button("3", 10, 400, command=lambda: show("3"))
create_button("2", 150, 400, command=lambda: show("2"))
create_button("1", 290, 400, command=lambda: show("1"))
create_button("=", 430, 400, height=3, bg="#fe9037", command=calculate)

create_button("0", 10, 500, width=11, command=lambda: show("0"))
create_button(".", 290, 500, command=lambda: show("."))

root.mainloop()