#Крестики-нолики. Играют два человека, можно играть  клавиатурой клавишами qweasdzxc

from tkinter import *
import tkinter.messagebox
import random

#выход из приложения
def exit_(event):
    root.destroy()

#справка
def help1(event):
    tkinter.messagebox.showinfo("Справка по игре.",
                                "F1 - Инфа.\n"+
                                "F12 - Новая игра.\n"+
                                "Ecs - выход из игры.\n"+
                                "Автор Abduvohid\n")

#начать занаво
def begin(event):
    global butn
    global field
    global numButton
    global XO
    for b in butn:
        b.config(bg = "green", text = '')
    field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    numButton = []
    XO = 1
    
       

#логика приложения
def logik():
    global field
    global numButton
    end = False
    if field[0] ==  field[1] ==  field[2] > 0:
        winner = field[0]
        end = True
    elif field[3] ==  field[4] ==  field[5] > 0:
        winner = field[3]
        end = True
    elif field[6] ==  field[7] ==  field[8] > 0:
        winner = field[6]
        end = True
    elif field[0] ==  field[3] ==  field[6] > 0:
        winner = field[0]
        end = True
    elif field[1] ==  field[4] ==  field[7] > 0:
        winner = field[1]
        end = True
    elif field[2] ==  field[5] ==  field[8] > 0:
        winner = field[2]
        end = True
    elif field[0] ==  field[4] ==  field[8] > 0:
        winner = field[0]
        end = True
    elif field[2] ==  field[4] ==  field[6] > 0:
        winner = field[2]
        end = True
    if end:
        if winner ==  1:
            user = "Нолик"
        elif winner ==  2:
            user = "Крестик"
        tkinter.messagebox.showinfo("Конец игры", "Выиграл " + user)
        begin(None)
    elif len(numButton) ==  9:
        tkinter.messagebox.showinfo("Конец игры", "  Ничья!!!  ")
        begin(None)

#Ход бота
def bots_move():
    global XO
    global numButton
    global butn
    if XO == 2:
        s = []
        for i in range(9):
            if i not in numButton:
                s.append(i)
        
        num = random.choice(s)
        button = butn[num]
        button.config(text = 'Крестик')
        button.config(bg = 'grey')
        field[num] = XO
        XO = 1
        numButton.append(num)
        logik()
        
        
#нажатие на кнопки
def click(button, num):
    global numButton
    if num not in numButton:
        global XO
        if XO ==  1:
            button.config(text = 'Нолик')
            button.config(bg = 'gold')
            field[num] = XO
            XO = 2
        numButton.append(num)
        logik()
        bots_move()


field = [0, 0, 0, 0, 0, 0, 0, 0, 0] #список значений 1 или 2
XO = 1#крестик - 2, нолик - 1
numButton = [] #список нажатых кнопок


root = Tk()
root.title("Крестики-нолики")
root.geometry("233x238")
root.resizable(False, False)

ris0 = Button(root, width = 10, height = 5, bg = "green",
              text = "q", command = lambda:click(ris0, 0))
ris0.place(x = 0, y = 0)
ris1 = Button(root, width = 10, height = 5, bg = "green",
              text = "w", command = lambda:click(ris1, 1))
ris1.place(x = 81, y = 0)
ris2 = Button(root, width = 10, height = 5, bg = "green",
              text = "e", command = lambda:click(ris2, 2))
ris2.place(x = 162, y = 0)

ris3 = Button(root, width = 10, height = 5, bg = "green",
              text = "a", command = lambda:click(ris3, 3))
ris3.place(x = 0, y = 81)
ris4 = Button(root, width = 10, height = 5, bg = "green",
              text = "s", command = lambda:click(ris4, 4))
ris4.place(x = 81, y = 81)
ris5 = Button(root, width = 10, height = 5, bg = "green",
              text = "d", command = lambda:click(ris5, 5))
ris5.place(x = 162, y = 81)

ris6 = Button(root, width = 10, height = 5, bg = "green",
              text = "z", command = lambda:click(ris6, 6))
ris6.place(x = 0, y = 162)
ris7 = Button(root, width = 10, height = 5, bg = "green",
              text = "x", command = lambda:click(ris7, 7))
ris7.place(x = 81, y = 162)
ris8 = Button(root, width = 10, height = 5, bg = "green",
              text = "c", command = lambda:click(ris8, 8))
ris8.place(x = 162, y = 162)

butn = [ris0, ris1, ris2, ris3, ris4, ris5, ris6, ris7, ris8]

#функциональные клавиши
root.bind('<Escape>', exit_)
root.bind('<F1>', help1)
root.bind('<F12>', begin)

#игра нажатием букв
root.bind('<q>', lambda *ignore:click(ris0,0))
root.bind('<w>', lambda *ignore:click(ris1,1))
root.bind('<e>', lambda *ignore:click(ris2,2))
root.bind('<a>', lambda *ignore:click(ris3,3))
root.bind('<s>', lambda *ignore:click(ris4,4))
root.bind('<d>', lambda *ignore:click(ris5,5))
root.bind('<z>', lambda *ignore:click(ris6,6))
root.bind('<x>', lambda *ignore:click(ris7,7))
root.bind('<c>', lambda *ignore:click(ris8,8))

root.mainloop()
