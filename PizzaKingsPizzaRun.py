import tkinter as tk
from tkinter import *

# 1. SETUP & WINDOW INITIALIZATION
root = tk.Tk()
root.title("Pizza King's Pizza Run")
canvas = tk.Canvas(root, width=1000, height=600, bg="brown")
canvas.pack()

# Player spawns safely directly on top of the first orange platform
player = canvas.create_rectangle(100, 160, 120, 220, fill="white")

# 2. LEVEL DESIGN (Platforms & Goals)
platform_ids = []

post = canvas.create_rectangle(890, 100, 900, 600, fill="silver")
goal = canvas.create_rectangle(890, 330, 950, 350, fill="gold")

# The tall silver post is still a safe platform you can land on
platform_ids.append(post)

# Staircase layout
platform_ids.append(canvas.create_rectangle(80, 230, 220, 240, fill="orange"))    
platform_ids.append(canvas.create_rectangle(260, 320, 400, 330, fill="orange"))   
platform_ids.append(canvas.create_rectangle(440, 230, 580, 240, fill="orange"))   
platform_ids.append(canvas.create_rectangle(620, 180, 740, 190, fill="orange"))   
platform_ids.append(canvas.create_rectangle(760, 140, 880, 150, fill="orange"))   

# Floor ground platform (Acts as a hazard)
ground = canvas.create_rectangle(0, 550, 1000, 600, fill="darkgray")

# 3. GAME STATE & INPUT DICTIONARY
yv = 0 
game_active = True
loop_id = None 
keys_pressed = {"Left": False, "Right": False, "Up": False, "space": False, "r": False, "R": False}

# 4. KEYBOARD TRACKING MECHANICS
def key_down(event):
    if event.keysym in keys_pressed:
        keys_pressed[event.keysym] = True

def key_up(event):
    if event.keysym in keys_pressed:
        keys_pressed[event.keysym] = False

# 5. INSTANT RESET LOGIC
def reset_game():
    global yv, game_active, loop_id
    
    if loop_id is not None:
        root.after_cancel(loop_id)
        loop_id = None
        
    canvas.coords(player, 100, 160, 120, 220)
    yv = 0
    
    for key in keys_pressed:
        keys_pressed[key] = False
        
    canvas.itemconfig(goal, fill="gold")
    status_label.config(text="Respawned! Avoid the gray floor.", fg="black", font=("Arial", 12))
    
    game_active = True
    loop_id = root.after(16, game_loop)

# 6. PRECISE COLLISION ENGINE
def touching_platforms():
    p_box = canvas.coords(player)
    p_left, p_top, p_right, p_bottom = p_box[0], p_box[1], p_box[2], p_box[3]

    for plat in platform_ids:
        plat_box = canvas.coords(plat)
        o_left, o_top, o_right, o_bottom = plat_box[0], plat_box[1], plat_box[2], plat_box[3]

        if p_right >= o_left and p_left <= o_right:
            if abs(p_bottom - o_top) <= 6 and yv >= 0:
                canvas.move(player, 0, o_top - p_bottom)
                return True
    return False

# 7. ENGINE PHYSICS & ACTION LOOP
def game_loop():
    global yv, game_active, loop_id
    
    if keys_pressed.get("r") or keys_pressed.get("R"):
        reset_game()
        return

    if not game_active:
        loop_id = root.after(16, game_loop)
        return

    # Process Horizontal Movements safely
    if keys_pressed.get("Left"):
        canvas.move(player, -5, 0)
    if keys_pressed.get("Right"):
        canvas.move(player, 5, 0)

    # Super jump calculation checks
    if keys_pressed.get("Up") and keys_pressed.get("space") and touching_platforms():
        yv = -15  
    elif keys_pressed.get("Up") and touching_platforms():
        yv = -10  

    # Apply Environmental Gravity Force
    if not touching_platforms():
        yv += 0.4  
    else:
        if yv > 0:
            yv = 0  

    canvas.move(player, 0, yv)

    # Fetch position variables for immediate bounds evaluation
    p_pos = canvas.coords(player)
    overlapping_items = canvas.find_overlapping(p_pos[0], p_pos[1], p_pos[2], p_pos[3])
    
    # Instant auto-restart triggers if player drops off platforms into gray ground or below 600
    if ground in overlapping_items or p_pos[1] > 600:
        reset_game()
        return

    # FIXED: Removed the post win condition block entirely. 
    # Only the gold goal overlap below can trigger a win now.

    # Win Checking Logic: Goal Box Overlap Collision
    if goal in overlapping_items and game_active:
        status_label.config(text="YOU WIN! You reached the gold goal!", fg="green", font=("Arial", 14, "bold"))
        canvas.itemconfig(goal, fill="yellow")
        game_active = False
        loop_id = root.after(16, game_loop)
        return

    loop_id = root.after(16, game_loop)

# 8. UI INTERFACE & SYSTEM BINDINGS
status_label = tk.Label(root, text="Touch the gold goal to win! Avoid the gray ground floor.", fg="black", font=("Arial", 12))
status_label.pack(pady=5)

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

# Start engine core execution safely
loop_id = root.after(16, game_loop)
root.mainloop()

