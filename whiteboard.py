import tkinter as tk
from tkinter import colorchooser
import json, socket

colour = "black"
current_command_list = [] #needs fields as: colour: ..... xValues:..... yValues:...... type:......
draw_stack = []
#Global variables for drawing at mouse pos
prevX = None
prevY = None
type = "freehand"
prevType = None

#redraw clear  
def clear():
    print("Canvas cleared")
    myCanvas.delete("all")


def choose_color():
    global colour
    # variable to store hexadecimal code of color
    colour = colorchooser.askcolor(title="Choose color")[1]
    print(colour)
    
    
# Clear the canvas and reset stacks
def clear_button_clear():
    global current_command_list, draw_stack
    myCanvas.delete("all")
    current_command_list.clear()
    draw_stack.clear()

# Undo last action
def redraw():
    global colour, type, current_command_list, prevType, draw_stack
    if len(current_command_list) != 0:
        draw_stack.append(current_command_list[:])
        current_command_list.clear()
    
    if draw_stack:
        draw_stack.pop()
        clear()
        for command_list in draw_stack:
            for json_data in command_list:
                command = json.loads(json_data)
                if command["type"] == "freehand":
                 myCanvas.create_line(command["X2"], command["Y2"], command["X1"], command["Y1"], 
                                     fill=command["colour"], width=command["width"])

root = tk.Tk()
root.title("Simple Whiteboard")
root.geometry("1000x600")

myCanvas = tk.Canvas(root, bg="WHITE", width=800, height=500)
myCanvas.pack(fill=tk.BOTH, expand=True)

# Button frame at the bottom
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# Colour picker button
Colour_button = tk.Button(button_frame, text='Choose colour', command=choose_color, width=12, height=2)

# Redraw (undo) button
redraw_button = tk.Button(button_frame, text='Undo', command=redraw, width=12, height=2)

# Clear button with image
bin = "images.png"
button_image = tk.PhotoImage(file=bin)
clear_button = tk.Button(button_frame, image=button_image, command=clear_button_clear, width=50, height=50)

# Width selection radio buttons
currentWidth = tk.IntVar(value=2)
def printResults():
    print(currentWidth.get())

# Place the width selection radio buttons in a separate frame
width_frame = tk.Frame(button_frame)
tk.Radiobutton(width_frame, text="1", variable=currentWidth, value=1, command=printResults).pack(side=tk.LEFT, padx=5)
tk.Radiobutton(width_frame, text="2", variable=currentWidth, value=2, command=printResults).pack(side=tk.LEFT, padx=5)
tk.Radiobutton(width_frame, text="3", variable=currentWidth, value=3, command=printResults).pack(side=tk.LEFT, padx=5)
tk.Radiobutton(width_frame, text="4", variable=currentWidth, value=4, command=printResults).pack(side=tk.LEFT, padx=5)

# Pack buttons into the frame
clear_button.pack(side=tk.LEFT, padx=10)
Colour_button.pack(side=tk.LEFT, padx=10)
redraw_button.pack(side=tk.LEFT, padx=10)
width_frame.pack(side=tk.LEFT, padx=10)

# Drawing functions
def startDraw(event):
    global prevX, prevY
    prevX = event.x
    prevY = event.y

def draw(event):
    global prevX, prevY, colour, type, current_command_list, prevType, currentWidth
    if type == "freehand" and (prevX != event.x or prevY != event.y):
        myCanvas.create_line(prevX, prevY, event.x, event.y, fill=colour, width=currentWidth.get())
        jsonCommand = {
            "type": type,
            "X1": event.x,
            "Y1": event.y,
            "X2": prevX,
            "Y2": prevY,
            "colour": colour,
            "width": currentWidth.get()
        }
        
    
        prevX = event.x
        prevY = event.y
        json_data = json.dumps(jsonCommand)
        current_command_list.append(json_data)
        
        
    if type == "circle" and (prevX != event.x or prevY != event.y):
        print("todo")
        
    check_size()

def check_size():
    global draw_stack, current_command_list
    if len(current_command_list) > 100:
        draw_stack.append(current_command_list[:])
        current_command_list.clear()

def endDraw(event):
    global prevX, prevY
    prevX = None
    prevY = None

myCanvas.bind("<ButtonPress-1>", startDraw)
myCanvas.bind("<B1-Motion>", draw)
myCanvas.bind("<ButtonRelease-1>", endDraw)

root.mainloop()
