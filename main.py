print("TIC TAC TOE")

import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Advanced Tic Tac Toe")
root.resizable(False, False)
root.configure(bg="#2b2b2b")

current_player = "X"
buttons = []
game_over = False
game_mode = "two"

x_score = 0
o_score = 0
draw_score = 0

winning_combinations = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def update_score():
    score_label.config(
        text=f"X: {x_score}   O: {o_score}   Draws: {draw_score}"
    )

def restart_game():
    global current_player, game_over
    current_player = "X"
    game_over = False
    turn_label.config(text="Player X's Turn")

    for btn in buttons:
        btn.config(text="", bg="#404040", fg="white")

def play_again():
    if messagebox.askyesno("Play Again", "Do you want to play again?"):
        restart_game()

def check_winner():
    global game_over, x_score, o_score, draw_score

    for combo in winning_combinations:
        a,b,c = combo
        if buttons[a]["text"] == buttons[b]["text"] == buttons[c]["text"] != "":
            winner = buttons[a]["text"]

            for i in combo:
                buttons[i].config(bg="lightgreen")

            if winner == "X":
                x_score += 1
            else:
                o_score += 1

            update_score()
            game_over = True
            save_scores()
            messagebox.showinfo("Winner", f"Player {winner} Wins!")
            play_again()
            return

    if all(btn["text"] != "" for btn in buttons):
        draw_score += 1
        update_score()
        game_over = True
        save_scores()
        messagebox.showinfo("Draw", "It's a Draw!")
        play_again()

def computer_move():
    global current_player

    if game_over:
        return

    empty = [i for i in range(9) if buttons[i]["text"] == ""]

    if empty:
        move = random.choice(empty)
        buttons[move]["text"] = "O"
        buttons[move].config(fg="red")

        check_winner()

        if not game_over:
            current_player = "X"
            turn_label.config(text="Player X's Turn")

def button_click(index):
    global current_player

    if game_over:
        return

    if game_mode == "single" and current_player == "O":
        return

    if buttons[index]["text"] == "":
        buttons[index]["text"] = current_player

        if current_player == "X":
            buttons[index].config(fg="deepskyblue")
        else:
            buttons[index].config(fg="tomato")

        check_winner()

        if not game_over:
            if game_mode == "single":
                current_player = "O"
                turn_label.config(text="Computer's Turn")
                root.after(500, computer_move)
            else:
                current_player = "O" if current_player == "X" else "X"
                turn_label.config(text=f"Player {current_player}'s Turn")

def set_single():
    global game_mode
    game_mode = "single"
    mode_label.config(text="Mode: Single Player")

def set_two():
    global game_mode
    game_mode = "two"
    mode_label.config(text="Mode: Two Player")

dark_mode = True

def toggle_theme():
    global dark_mode

    if dark_mode:
        root.configure(bg="white")
        title_label.config(bg="white", fg="black")
        turn_label.config(bg="white", fg="black")
        score_label.config(bg="white", fg="black")
        mode_label.config(bg="white", fg="black")
        dark_mode = False
    else:
        root.configure(bg="#2b2b2b")
        title_label.config(bg="#2b2b2b", fg="white")
        turn_label.config(bg="#2b2b2b", fg="white")
        score_label.config(bg="#2b2b2b", fg="gold")
        mode_label.config(bg="#2b2b2b", fg="white")
        dark_mode = True

def save_scores():
    with open("tictactoe_scores.txt", "w") as f:
        f.write(f"X Wins: {x_score}\n")
        f.write(f"O Wins: {o_score}\n")
        f.write(f"Draws: {draw_score}\n")

title_label = tk.Label(root, text="TIC TAC TOE",
                       font=("Arial", 22, "bold"),
                       bg="#2b2b2b", fg="white")
title_label.grid(row=0, column=0, columnspan=3, pady=10)

mode_label = tk.Label(root, text="Mode: Two Player",
                      font=("Arial", 12, "bold"),
                      bg="#2b2b2b", fg="white")
mode_label.grid(row=1, column=0, columnspan=3)

turn_label = tk.Label(root, text="Player X's Turn",
                      font=("Arial", 14, "bold"),
                      bg="#2b2b2b", fg="white")
turn_label.grid(row=2, column=0, columnspan=3)

score_label = tk.Label(root, text="X: 0   O: 0   Draws: 0",
                       font=("Arial", 12, "bold"),
                       bg="#2b2b2b", fg="gold")
score_label.grid(row=3, column=0, columnspan=3)

for i in range(9):
    btn = tk.Button(root,
                    text="",
                    width=6,
                    height=3,
                    font=("Arial", 24, "bold"),
                    bg="#404040",
                    fg="white",
                    command=lambda i=i: button_click(i))
    btn.grid(row=(i // 3) + 4, column=i % 3, padx=3, pady=3)
    buttons.append(btn)

tk.Button(root, text="Single Player",
          command=set_single).grid(row=7, column=0, sticky="nsew")

tk.Button(root, text="Two Player",
          command=set_two).grid(row=7, column=1, sticky="nsew")

tk.Button(root, text="Theme",
          command=toggle_theme).grid(row=7, column=2, sticky="nsew")

tk.Button(root, text="Restart Game",
          command=restart_game,
          font=("Arial", 12, "bold")).grid(
          row=8, column=0, columnspan=3, sticky="nsew", pady=8)

root.mainloop()
