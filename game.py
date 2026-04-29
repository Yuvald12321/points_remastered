import tkinter as tk
from tkinter import messagebox

BG_COLOR = "#191923"
TEXT_COLOR = "#FFFFFF"
BAR_BG = "#3C3C46"
BAR_FILL = "#2ECC71"
TURN_COLOR = "#FFD700"


def setup():
    setup_frame = tk.Frame(root, bg=BG_COLOR)
    setup_frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(setup_frame, text="Winning Score (Default 8000):", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 12)).pack(
        pady=5)
    goal_entry = tk.Entry(setup_frame, font=("Arial", 12))
    goal_entry.pack(pady=5)
    goal_entry.insert(0, "8000")

    tk.Label(setup_frame, text="Player Name:", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 12)).pack(pady=10)
    name_entry = tk.Entry(setup_frame, font=("Arial", 12))
    name_entry.pack(pady=5)
    name_entry.focus_set()

    players = []
    list_label = tk.Label(setup_frame, text="Players: ", fg="#FFD700", bg=BG_COLOR, font=("Arial", 11))
    list_label.pack(pady=5)

    def add_player(event=None):
        name = name_entry.get().strip()
        if name:
            players.append(name)
            name_entry.delete(0, tk.END)
            list_label.config(text=f"Players: {', '.join(players)}")

    root.bind('<Return>', add_player)
    tk.Button(setup_frame, text="Add Player", font=("Arial", 11), command=add_player).pack(pady=5)

    def start():
        try:
            goal_val = int(goal_entry.get())
        except ValueError:
            goal_val = 8000

        if len(players) < 2:
            messagebox.showwarning("Error", "Add at least 2 players!")
            return

        root.unbind('<Return>')
        setup_frame.destroy()
        game(players, goal_val)

    tk.Button(setup_frame, text="Start Game", font=("Arial", 12, "bold"), command=start).pack(side="bottom", pady=20)


def game(players_names, goal):
    players_data = {name: 0 for name in players_names}
    history = []
    ui_elements = {}
    state = {"turn": 0}
    winners = []

    game_frame = tk.Frame(root, bg=BG_COLOR)
    game_frame.pack(fill="both", expand=True, padx=20, pady=10)

    tk.Label(game_frame, text=f"GOAL: {goal}", font=("Arial", 20, "bold"), fg="#FFD700", bg=BG_COLOR).pack(pady=10)

    def update_turn_indicator():
        for i, name in enumerate(players_names):
            if i == state["turn"]:
                ui_elements[name]['label'].config(highlightbackground=TURN_COLOR, highlightthickness=2, fg=TURN_COLOR)
            else:
                ui_elements[name]['label'].config(highlightbackground=BG_COLOR, highlightthickness=2, fg=TEXT_COLOR)

    def update_bars(event=None):
        for name, score in players_data.items():
            progress = min(abs(score) / goal, 1.0) if goal > 0 else 0
            canvas = ui_elements[name]['canvas']
            fill_rect = ui_elements[name]['fill']
            current_width = canvas.winfo_width()

            if name in winners:
                canvas.coords(fill_rect, 0, 0, current_width * progress, 35)
                canvas.itemconfig(fill_rect, fill=TURN_COLOR)
            elif score >= 0:
                canvas.coords(fill_rect, 0, 0, current_width * progress, 35)
                canvas.itemconfig(fill_rect, fill=BAR_FILL)
            else:
                canvas.coords(fill_rect, current_width * (1 - progress), 0, current_width, 35)
                canvas.itemconfig(fill_rect, fill="#E74C3C")

    def update_display():
        for name, score in players_data.items():
            ui_elements[name]['label'].config(text=f"{name}: {score}")
            if name in winners:
                rank = winners.index(name) + 1
                ui_elements[name]['percent'].config(text=f"#{rank}")
            else:
                percent = int((score / goal) * 100) if goal > 0 else 0
                ui_elements[name]['percent'].config(text=f"{percent}%")
        update_bars()
        update_turn_indicator()

    def handle_action(is_e=False, event=None):
        try:
            points = int(points_entry.get())
        except ValueError:
            return

        active_name = players_names[state["turn"]]
        prev_turn = state["turn"]

        if is_e:
            for p in players_data:
                if p != active_name and p not in winners:
                    players_data[p] -= points
                    history.append((p, -points, None))
            history.append((None, 0, prev_turn))
        else:
            players_data[active_name] += points
            history.append((active_name, points, prev_turn))

        if players_data[active_name] >= goal and active_name not in winners:
            winners.append(active_name)

        if len(winners) >= len(players_names) - 1:
            for p in players_names:
                if p not in winners:
                    winners.append(p)
            update_display()

            lb_text = "LEADERBOARD\n\n"
            for i, w in enumerate(winners):
                lb_text += f"{i + 1}. {w} - {players_data[w]}\n"

            messagebox.showinfo("Game Over", lb_text)
            root.destroy()
            return

        state["turn"] = (state["turn"] + 1) % len(players_names)
        while players_names[state["turn"]] in winners:
            state["turn"] = (state["turn"] + 1) % len(players_names)

        points_entry.delete(0, tk.END)
        update_display()

    def undo():
        if not history: return

        last_action = history.pop()
        while last_action:
            name, pts, turn = last_action
            if name:
                players_data[name] -= pts
                if players_data[name] < goal and name in winners:
                    winners.remove(name)
            if turn is not None: state["turn"] = turn

            if not history or history[-1][2] is not None:
                break
            last_action = history.pop()

        update_display()

    for name in players_names:
        p_row = tk.Frame(game_frame, bg=BG_COLOR, pady=5)
        p_row.pack(fill="x")

        lbl = tk.Label(p_row, text=f"{name}: 0", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold"), width=12,
                       anchor="w", padx=5, pady=2, highlightthickness=2, highlightbackground=BG_COLOR)
        lbl.pack(side="left", padx=5)

        per_lbl = tk.Label(p_row, text="0%", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 10), width=4)
        per_lbl.pack(side="right", padx=5)

        canv = tk.Canvas(p_row, height=25, bg=BAR_BG, highlightthickness=0)
        canv.pack(side="left", padx=10, fill="x", expand=True)
        fill_rect = canv.create_rectangle(0, 0, 0, 25, fill=BAR_FILL, width=0)

        ui_elements[name] = {'label': lbl, 'canvas': canv, 'fill': fill_rect, 'percent': per_lbl}
        canv.bind("<Configure>", update_bars)

    controls_frame = tk.Frame(root, bg=BG_COLOR, pady=20)
    controls_frame.pack(side="bottom", fill="x")

    input_frame = tk.Frame(controls_frame, bg=BG_COLOR)
    input_frame.pack()

    points_entry = tk.Entry(input_frame, width=10, font=("Arial", 16), justify="center")
    points_entry.pack(side="left", padx=10)
    points_entry.focus_set()

    root.bind('<Return>', lambda e: handle_action(False))

    tk.Button(input_frame, text="+", bg="#2ECC71", font=("Arial", 14, "bold"), width=5,
              command=lambda: handle_action(False)).pack(side="left", padx=5)
    tk.Button(input_frame, text="E", bg="#E74C3C", fg="white", font=("Arial", 14, "bold"), width=5,
              command=lambda: handle_action(True)).pack(side="left", padx=5)

    tk.Button(controls_frame, text="Undo Last Action", font=("Arial", 10), command=undo, bg="#F1C40F").pack(pady=15)

    update_turn_indicator()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Points Remastered")
    root.configure(bg=BG_COLOR)
    setup()
    root.mainloop()