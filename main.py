import tkinter as tk
from tkinter import messagebox, PhotoImage
import random
import pygame
import os

# === SETUP ===
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
BACKGROUND_IMG = os.path.join(ASSETS_DIR, 'background.png')
MUSIC_FILE = os.path.join(ASSETS_DIR, 'background_music.mp3')

# === MUSIC ===
pygame.mixer.init()
try:
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.play(-1)
except:
    print("Music file not found or failed to load.")

# === MAIN WINDOW ===
root = tk.Tk()
root.title("🎯 Number Guessing Game 🎯")
root.geometry("800x500")
root.resizable(False, False)

bg_image = PhotoImage(file=BACKGROUND_IMG)
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

center_frame = tk.Frame(canvas, bg="#f0f0f0")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# === GAME VARIABLES ===
player_turn = 1
players = {1: {"score": 0}, 2: {"score": 0}}
guess_number = 0
attempts_left = 0
timer_id = None
difficulty_settings = {"Easy": (1, 10, 5), "Medium": (1, 50, 4), "Hard": (1, 100, 3)}

# === FUNCTIONS ===
def on_enter(e): e.widget.config(bg="#cce7ff")
def on_leave(e): e.widget.config(bg="#ddeeff")

def set_difficulty():
    global guess_number, attempts_left
    diff = difficulty_var.get()
    low, high, attempts = difficulty_settings[diff]
    guess_number = random.randint(low, high)
    attempts_left = attempts
    guess_range_label.config(text=f"Guess a number between {low} and {high}")
    attempts_label.config(text=f"Attempts left: {attempts_left}")
    status_label.config(text=f"Player {player_turn}'s turn!")
    start_timer()

def check_guess():
    global attempts_left, guess_number, player_turn
    try:
        user_guess = int(guess_entry.get())
    except:
        messagebox.showwarning("Invalid", "Please enter a valid number")
        return

    attempts_left -= 1
    attempts_label.config(text=f"Attempts left: {attempts_left}")

    if user_guess == guess_number:
        players[player_turn]["score"] += 1
        messagebox.showinfo("Correct!", f"🎉 Player {player_turn} guessed right!")
        update_scores()
        next_round()
    elif user_guess < guess_number:
        status_label.config(text="Too low! Try again.")
    else:
        status_label.config(text="Too high! Try again.")

    if attempts_left == 0:
        messagebox.showinfo("Out of attempts!", f"The number was {guess_number}.")
        next_round()

def start_timer():
    countdown(15)

def countdown(time_left):
    global timer_id
    timer_label.config(text=f"⏳ Time left: {time_left}s")
    if time_left > 0:
        timer_id = root.after(1000, countdown, time_left - 1)
    else:
        messagebox.showinfo("Time's Up", "You ran out of time!")
        next_round()

def next_round():
    global player_turn
    root.after_cancel(timer_id)
    player_turn = 2 if player_turn == 1 else 1
    guess_entry.delete(0, tk.END)
    set_difficulty()

def update_scores():
    p1_score.config(text=f"Player 1 Score: {players[1]['score']}")
    p2_score.config(text=f"Player 2 Score: {players[2]['score']}")

def reset_game():
    global players, player_turn
    players = {1: {"score": 0}, 2: {"score": 0}}
    player_turn = 1
    update_scores()
    set_difficulty()

# === TITLE ===
title_label = tk.Label(center_frame, text="🎯 Number Guessing Game 🎯",
                       font=("Arial", 22, "bold"), fg="#222222", bg="#f0f0f0")
title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

# === DIFFICULTY ===
difficulty_var = tk.StringVar(value="Easy")
difficulty_label = tk.Label(center_frame, text="Difficulty:", font=("Arial", 13), bg="#f0f0f0")
difficulty_label.grid(row=1, column=0, sticky="e")
difficulty_menu = tk.OptionMenu(center_frame, difficulty_var, *difficulty_settings.keys())
difficulty_menu.config(font=("Arial", 12), bg="#ddeeff")
difficulty_menu.grid(row=1, column=1, sticky="w", pady=5)

guess_range_label = tk.Label(center_frame, text="", font=("Arial", 12), bg="#f0f0f0")
guess_range_label.grid(row=2, column=0, columnspan=3)

# === INPUT ===
guess_entry = tk.Entry(center_frame, font=("Arial", 14), width=10)
guess_entry.grid(row=3, column=0, columnspan=2, pady=10)

submit_btn = tk.Button(center_frame, text="Submit Guess", font=("Arial", 12, "bold"), bg="#ddeeff", command=check_guess)
submit_btn.grid(row=3, column=2, padx=10)
submit_btn.bind("<Enter>", on_enter)
submit_btn.bind("<Leave>", on_leave)

# === INFO ===
attempts_label = tk.Label(center_frame, text="", font=("Arial", 12), bg="#f0f0f0")
attempts_label.grid(row=4, column=0, columnspan=3)

status_label = tk.Label(center_frame, text="", font=("Arial", 12), fg="green", bg="#f0f0f0")
status_label.grid(row=5, column=0, columnspan=3, pady=5)

timer_label = tk.Label(center_frame, text="", font=("Arial", 12), fg="red", bg="#f0f0f0")
timer_label.grid(row=6, column=0, columnspan=3)

# === SCOREBOARD ===
p1_score = tk.Label(center_frame, text="Player 1 Score: 0", font=("Arial", 12), bg="#f0f0f0")
p1_score.grid(row=7, column=0)

p2_score = tk.Label(center_frame, text="Player 2 Score: 0", font=("Arial", 12), bg="#f0f0f0")
p2_score.grid(row=7, column=2)

# === CONTROLS ===
start_btn = tk.Button(center_frame, text="▶ Start Game", font=("Arial", 12, "bold"), bg="#ddeeff", command=set_difficulty)
start_btn.grid(row=8, column=0, columnspan=3, pady=(15, 5))
start_btn.bind("<Enter>", on_enter)
start_btn.bind("<Leave>", on_leave)

reset_btn = tk.Button(center_frame, text="🔄 Restart Game", font=("Arial", 12, "bold"), bg="#ffeedd", command=reset_game)
reset_btn.grid(row=9, column=0, columnspan=3, pady=(0, 10))
reset_btn.bind("<Enter>", on_enter)
reset_btn.bind("<Leave>", on_leave)

# === START ===
root.mainloop()
