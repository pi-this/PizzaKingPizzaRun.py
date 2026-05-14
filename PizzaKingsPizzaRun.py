import tkinter as tk
from tkinter import *
from time import sleep
yv=0

# 1. SETUP & VARIABLES
root = tk.Tk()
root.title("Final Game Starter Kit")
canvas = tk.Canvas(root, width=1000, height=600, bg="brown")
canvas.pack()

# Create a player (Blue) and a Goal (Gold)
player = canvas.create_rectangle(100, 230, 80, 170, fill="white")# 3. MOVEMENT LOGIC (For Platformers/Action)

def move_player(event):
    key = event.keysym
    if key == "Up":
        canvas.move(player, 0, -10)
    elif key == "Left":
        canvas.move(player, -10, 0)
    elif key == "Right":
        canvas.move(player, 10, 0)
    def touching_platforms():
        crds = canvas.coords(player)
        y = (crds[1] + crds[3]) / 2
# Function to check if the player is touching a platform
def touching_platforms():
    crds = canvas.coords(player)
    y = (crds[1] + crds[3]) / 2
    # Check if the player is above a platform (you need to define platform coordinates)
    return y >= 480 # Example: ground level at y=480
post = canvas.create_rectangle(900, 300, 890, 1000, fill="silver")
goal = canvas.create_rectangle(950, 350, 890, 330, fill="gold")
platforms = canvas.create_rectangle(550, 340, 440, 330, fill="orange")
platforms = canvas.create_rectangle(150, 230, 80, 240, fill="orange")
platforms = canvas.create_rectangle(250, 430, 330, 420, fill="orange")
platforms = canvas.create_rectangle(450, 230, 330, 220, fill="orange")
platforms = canvas.create_rectangle(850, 240, 790, 230, fill="orange")
platforms = canvas.create_rectangle(630, 280, 700, 290, fill="orange")



    # Function to apply gravity
def gravity():
    global yv
    if not touching_platforms():
        yv += 0.2 # Increase downward speed
    else:
        yv = 0 # Reset speed if touching a platform


    # Main game loop
while True:
        gravity()
        root.update()
        sleep(0.01) # Control the frame rate
            
    # Get the current position of the player
        p_pos = canvas.coords(player) 
    
    # Look for items overlapping the player's area
        overlapping = canvas.find_overlapping(p_pos[0], p_pos[1], p_pos[2], p_pos[3])
    
    # If the 'goal' ID is in that list, something happened!
        if goal in overlapping:
             status_label.config(text="YOU WIN! You touched the goal!", fg="orange")
             canvas.itemconfig(goal, fill="yellow") # Change color when touched


status_label = tk.Label(root, text="Use Arrows to move. Use Buttons to trade.", fg="gray")
status_label.pack()

# 5. BUTTONS & BINDINGS
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10) 
 
# Connects keyboard to the movement function
root.bind("<Key>", move_player)

root.mainloop()