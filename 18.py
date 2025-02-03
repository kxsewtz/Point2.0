from tkinter import *
from tkinter.colorchooser import askcolor

root = Tk()
root.geometry("600x400")
root.title("Point2.0")
root["bg"] = "gray75"

canvas = Canvas(root, width= 540, height= 400, bg = "white")
canvas.grid(row= 0, column = 0, rowspan = 7)

state = "circle"
brush = 10
color = "red"

def choose(input):
   global state, brush
   if input == "plus" and brush < 98:
       brush += 2
       size.configure(text=brush)
       return
   elif input == "minus" and brush > 0:
       brush -= 2
       size.configure(text=brush)
       return
   state = input

def clear_canvas(event):
    canvas.delete("all")

def ask_color(event):
    global color
    color_code = askcolor(title="Выбери цвет")
    color = color_code[1]
    size.configure(fg=color)

square_btn = Button(root, text="🟥", font=(None, 20), command=lambda: choose("square"))
square_btn.grid(row=0, column=1)
circle_btn = Button(root, text="🔴", font=(None, 20), command=lambda: choose("circle"))
circle_btn.grid(row=1, column=1)
line1_btn = Button(root, text="↘️", font=(None, 16), command=lambda: choose("line1"))
line1_btn.grid(row=2, column=1)
line2_btn = Button(root, text="↙️", font=(None, 16), command=lambda: choose("line2"))
line2_btn.grid(row=3, column=1)

plus_btn = Button(root, text="➕", font=(None, 20), command=lambda: choose("plus"))
plus_btn.grid(row=4, column=1)
minus_btn = Button(root, text="➖", font=(None, 20), command=lambda: choose("minus"))
minus_btn.grid(row=5, column=1)

size = Label(root, text=brush, fg=color, font=(None, 32))
size.grid(row=6, column=1)

def paint(event):
   print(event.__dict__)
   if event.widget.__class__ is not Canvas:
       return
   if state == "circle":
       canvas.create_oval(event.x - brush, event.y - brush,
                          event.x + brush, event.y + brush,
                          fill=color, outline=color)
   elif state == "square":
       canvas.create_rectangle(event.x - brush, event.y - brush,
                               event.x + brush, event.y + brush,
                               fill=color, outline=color)
   elif state == "line1":
       canvas.create_line(event.x - brush, event.y - brush,
                          event.x + brush, event.y + brush, fill=color)
   elif state == "line2":
       canvas.create_line(event.x + brush, event.y - brush,
                          event.x - brush, event.y + brush, fill=color)
def erase(event):
   canvas.create_oval(event.x - brush * 2, event.y - brush * 2,
                      event.x + brush * 2, event.y + brush * 2,
                      fill="white", outline="white")


root.bind_all("<3>", erase)
root.bind_all("<B3-Motion>", erase)
canvas.bind_all("c", ask_color)
root.bind_all("<1>", paint)
root.bind_all("<B1-Motion>", paint)
root.bind_all("<BackSpace>", clear_canvas)
root.mainloop()
