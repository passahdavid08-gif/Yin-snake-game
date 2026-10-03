import random
import tkinter as tk

WIDTH = 600
HEIGHT = 600
BLOCK = 20
GRID = WIDTH // BLOCK

root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

score_var = tk.StringVar(value="Score: 0")
score_label = tk.Label(root, textvariable=score_var, fg="white", bg="black", font=("Arial", 14, "bold"))
score_label.pack(fill=tk.X)

snake = [(5, 5), (4, 5), (3, 5)]
direction = (1, 0)
next_direction = (1, 0)
food = None
score = 0
game_over = False


def place_food():
    global food
    free_cells = []
    for y in range(GRID):
        for x in range(GRID):
            if (x, y) not in snake:
                free_cells.append((x, y))
    if free_cells:
        food = random.choice(free_cells)
    else:
        food = None


def update_score():
    score_var.set(f"Score: {score}")


def draw():
    canvas.delete("all")

    for x in range(0, WIDTH, BLOCK):
        canvas.create_line(x, 0, x, HEIGHT, fill="#111111")
    for y in range(0, HEIGHT, BLOCK):
        canvas.create_line(0, y, WIDTH, y, fill="#111111")

    for x, y in snake:
        canvas.create_rectangle(
            x * BLOCK,
            y * BLOCK,
            (x + 1) * BLOCK,
            (y + 1) * BLOCK,
            fill="lime",
            outline="darkgreen",
            width=2,
        )

    if food:
        fx, fy = food
        canvas.create_oval(
            fx * BLOCK + 3,
            fy * BLOCK + 3,
            (fx + 1) * BLOCK - 3,
            (fy + 1) * BLOCK - 3,
            fill="red",
            outline="darkred",
            width=2,
        )

    if game_over:
        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="Game Over",
            fill="white",
            font=("Arial", 28, "bold"),
        )
        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 35,
            text="Press Space to restart",
            fill="white",
            font=("Arial", 14),
        )


def change_direction(new_direction):
    global next_direction
    if new_direction[0] == -direction[0] and new_direction[1] == -direction[1]:
        return
    next_direction = new_direction


def step():
    global snake, direction, next_direction, food, score, game_over

    if game_over:
        return

    direction = next_direction
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    if (
        new_head[0] < 0
        or new_head[0] >= GRID
        or new_head[1] < 0
        or new_head[1] >= GRID
        or new_head in snake
    ):
        game_over = True
        draw()
        return

    snake.insert(0, new_head)

    if food and new_head == food:
        score += 1
        update_score()
        place_food()
    else:
        snake.pop()

    draw()
    root.after(120, step)


def reset_game():
    global snake, direction, next_direction, food, score, game_over
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    next_direction = (1, 0)
    score = 0
    update_score()
    game_over = False
    place_food()
    draw()
    root.after(120, step)


def handle_key(event):
    key = event.keysym.lower()

    if game_over and key == "space":
        reset_game()
        return

    if key in {"up", "w"}:
        change_direction((0, -1))
    elif key in {"down", "s"}:
        change_direction((0, 1))
    elif key in {"left", "a"}:
        change_direction((-1, 0))
    elif key in {"right", "d"}:
        change_direction((1, 0))


root.bind("<KeyPress>", handle_key)

place_food()
draw()
root.after(120, step)
root.mainloop()
