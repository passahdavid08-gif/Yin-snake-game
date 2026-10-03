#====================================
# MINI PROJECT: SNAKE GAME
#====================================
# Auteur : @yindav

import turtle
import time
import random
import json

# ============================================================
# CONSTANTES
# ============================================================
FICHIER_HIGHSCORE = "highscore.txt"
FICHIER_LEADERBOARD = "leaderboard.json"   # IDÉE 3 : classement des 5 meilleurs scores
DELAY = None

# IDÉE 6 : passe à True pour activer le mode "sans murs" (wraparound) —
# le serpent réapparaît du côté opposé au lieu de mourir contre le mur.
# Incompatible en pratique avec l'idée "mourir contre le mur" :
# CHOIX DE DESIGN, pas un ajout en plus — un seul des deux comportements
# est actif à la fois, contrôlé par cet interrupteur.
MODE_SANS_MURS = True

# IDÉE 2 : séquence de touches à reproduire pour débloquer le mode secret
SEQUENCE_SECRETE = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right"]

# ============================================================
# PERSISTANCE DU HIGH SCORE
# ============================================================
def charger_highscore():
    try:
        with open(FICHIER_HIGHSCORE, "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
    except ValueError:
        print("Fichier de score corrompu, réinitialisation à 0.")
        return 0

def sauvegarder_highscore(valeur):
    with open(FICHIER_HIGHSCORE, "w") as f:
        f.write(str(valeur))

# ============================================================
# IDÉE 3 : PERSISTANCE DU CLASSEMENT (leaderboard avec pseudo)
# Même principe que le high score, mais on stocke une LISTE de
# dictionnaires {"nom": ..., "score": ...} au format JSON.
# ============================================================
def charger_leaderboard():
    try:
        with open(FICHIER_LEADERBOARD, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def sauvegarder_leaderboard(classement):
    with open(FICHIER_LEADERBOARD, "w") as f:
        json.dump(classement, f, indent=2)

def ajouter_score(nom, score_final):
    classement = charger_leaderboard()
    classement.append({"nom": nom, "score": score_final})
    classement.sort(key=lambda e: e["score"], reverse=True)   # tri décroissant
    classement = classement[:5]                                  # garde les 5 meilleurs
    sauvegarder_leaderboard(classement)

# ============================================================
# FENÊTRE DU JEU
# ============================================================
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)
turtle.colormode(255)   # autorise les couleurs RGB (0-255) — nécessaire pour l'IDÉE 1

# ---- FILIGRANE DE PERSONNALISATION ----
filigrane = turtle.Turtle()
filigrane.speed(0)
filigrane.color("gray")
filigrane.penup()
filigrane.hideturtle()
for x in range(-240, 241, 160):
    for y in range(-240, 241, 160):
        filigrane.goto(x, y)
        filigrane.write("YIN", align="center", font=("Arial", 16, "bold"))

# ---- TÊTE DU SERPENT ----
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.hideturtle()

# ---- CORPS DU SERPENT ----
segments = []

# ---- NOURRITURE ----
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)
food.hideturtle()

# ============================================================
# OBSTACLES FIXES
# ============================================================
obstacles = []

def position_valide(x, y):
    if abs(x) < 60 and abs(y) < 60:
        return False
    for obs in obstacles:
        if obs.xcor() == x and obs.ycor() == y:
            return False
    return True

def nouvelle_position_libre():
    while True:
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        if position_valide(x, y):
            return x, y

def generer_obstacles(nombre):
    for obs in obstacles:
        obs.hideturtle()
    obstacles.clear()
    while len(obstacles) < nombre:
        x, y = nouvelle_position_libre()
        obs = turtle.Turtle()
        obs.speed(0)
        obs.shape("square")
        obs.color("orange")
        obs.penup()
        obs.goto(x, y)
        obstacles.append(obs)

# ============================================================
# IDÉE 5 : OBSTACLE MOBILE (actif uniquement en mode "difficile")
# Fait un simple va-et-vient horizontal, indépendamment du serpent.
# ============================================================
obstacle_mobile = turtle.Turtle()
obstacle_mobile.speed(0)
obstacle_mobile.shape("square")
obstacle_mobile.color("purple")
obstacle_mobile.penup()
obstacle_mobile.hideturtle()

direction_obstacle_mobile = 1   # 1 = vers la droite, -1 = vers la gauche

def deplacer_obstacle_mobile():
    global direction_obstacle_mobile
    if not obstacle_mobile.isvisible():
        return   # pas en mode difficile : on ne fait rien
    nouvelle_x = obstacle_mobile.xcor() + 4 * direction_obstacle_mobile
    if nouvelle_x > 260 or nouvelle_x < -260:
        direction_obstacle_mobile *= -1
        nouvelle_x = obstacle_mobile.xcor() + 4 * direction_obstacle_mobile
    obstacle_mobile.setx(nouvelle_x)

# ============================================================
# STYLOS D'AFFICHAGE
# ============================================================
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

message_pen = turtle.Turtle()
message_pen.speed(0)
message_pen.color("white")
message_pen.penup()
message_pen.hideturtle()

menu_pen = turtle.Turtle()
menu_pen.speed(0)
menu_pen.color("white")
menu_pen.penup()
menu_pen.hideturtle()

# ============================================================
# ÉTAT DU JEU
# ============================================================
score = 0
high_score = charger_highscore()
game_over = False
en_menu = True
grow = 0
direction = "stop"
next_direction = "stop"

# IDÉE 4 : statistiques de la partie en cours
temps_debut = 0
pommes_mangees = 0
longueur_max = 1

# IDÉE 2 : mémoire des dernières touches (pour détecter le code secret)
buffer_touches = []
mode_special = False

OPPOSES = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

# ============================================================
# IDÉE 1 : COULEUR ÉVOLUTIVE DU SERPENT (corrigée)
# Dégradé VERT → JAUNE → ROUGE, complet à PALIER_MAX points.
# ============================================================
def couleur_selon_score(s):
    PALIER_MAX = 150
    t = min(s, PALIER_MAX) / PALIER_MAX

    if t < 0.5:
        progression = t / 0.5
        r = int(progression * 255)
        g = 255
        b = 0
    else:
        progression = (t - 0.5) / 0.5
        r = 255
        g = int(255 - progression * 255)
        b = 0

    return (r, g, b)

def afficher_score():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 24, "normal"))

# ============================================================
# IDÉE 2 : CODE SECRET
# ============================================================
def verifier_code_secret(touche):
    global buffer_touches, mode_special
    buffer_touches.append(touche)
    buffer_touches = buffer_touches[-len(SEQUENCE_SECRETE):]
    if buffer_touches == SEQUENCE_SECRETE and not mode_special:
        mode_special = True
        head.color("gold")
        print("✨ Mode secret activé !")

# ============================================================
# DIRECTION DU SERPENT
# ============================================================
def changer_direction(nouvelle):
    global next_direction
    verifier_code_secret(nouvelle)   # IDÉE 2 : on vérifie à chaque touche de direction
    if OPPOSES.get(nouvelle) == direction:
        return
    next_direction = nouvelle

def go_up():
    changer_direction("Up")

def go_down():
    changer_direction("Down")

def go_left():
    changer_direction("Left")

def go_right():
    changer_direction("Right")

# IDÉE 6 : gestion des murs — ne fait rien si MODE_SANS_MURS est False
def gerer_murs():
    if not MODE_SANS_MURS:
        return
    if head.xcor() > 290:
        head.setx(-290)
    elif head.xcor() < -290:
        head.setx(290)
    if head.ycor() > 290:
        head.sety(-290)
    elif head.ycor() < -290:
        head.sety(290)

def move():
    global direction
    direction = next_direction
    if direction == "Up":
        head.sety(head.ycor() + 20)
    if direction == "Down":
        head.sety(head.ycor() - 20)
    if direction == "Left":
        head.setx(head.xcor() - 20)
    if direction == "Right":
        head.setx(head.xcor() + 20)
    gerer_murs()   # IDÉE 6

# ============================================================
# IDÉE 4 : AFFICHAGE UNIFIÉ DU GAME OVER
# Remplace les 3 blocs qui étaient dupliqués (mur / obstacle / corps)
# par une seule fonction réutilisable — principe DRY (Don't Repeat Yourself).
# ============================================================
def afficher_game_over(raison):
    global game_over
    game_over = True
    duree = int(time.time() - temps_debut)
    message_pen.clear()
    message_pen.goto(0, 40)
    message_pen.write("Game Over!", align="center", font=("Arial", 24, "bold"))
    message_pen.goto(0, 0)
    message_pen.write("Press Space to Restart", align="center", font=("Arial", 18, "normal"))
    message_pen.goto(0, -30)
    message_pen.write(f"Pommes: {pommes_mangees}  Longueur max: {longueur_max}  Durée: {duree}s",
                    align="center", font=("Arial", 14, "normal"))
    print(f"Game over : {raison}")

# ============================================================
# MENU DE DIFFICULTÉ
# ============================================================
def afficher_menu():
    menu_pen.clear()
    menu_pen.goto(0, 130)
    menu_pen.write(" YIN SNAKE GAME", align="center", font=("Arial", 32, "bold"))
    menu_pen.goto(0, 60)
    menu_pen.write("Veuillez choisir la difficulté :", align="center", font=("Arial", 18, "normal"))
    menu_pen.goto(0, 20)
    menu_pen.write("1 = easy level (0 obstacle)", align="center", font=("Arial", 16, "normal"))
    menu_pen.goto(0, -10)
    menu_pen.write("2 = Medium Level (4 obstacles)", align="center", font=("Arial", 16, "normal"))
    menu_pen.goto(0, -40)
    menu_pen.write("3 = HOT Level (8 obstacles + 1 mobile)", align="center", font=("Arial", 16, "normal"))

    # IDÉE 3 : affichage du classement directement sur le menu
    classement = charger_leaderboard()
    if classement:
        menu_pen.goto(0, -90)
        menu_pen.write("Meilleurs scores :", align="center", font=("Arial", 14, "bold"))
        y = -115
        for i, entree in enumerate(classement, start=1):
            menu_pen.goto(0, y)
            menu_pen.write(f"{i}. {entree['nom']} - {entree['score']}", align="center", font=("Arial", 12, "normal"))
            y -= 22

def demarrer(vitesse, nb_obstacles):
    global DELAY, en_menu, temps_debut, pommes_mangees, longueur_max
    DELAY = vitesse
    generer_obstacles(nb_obstacles)

    # IDÉE 5 : l'obstacle mobile n'apparaît qu'en mode difficile
    if nb_obstacles >= 8:
        obstacle_mobile.goto(0, 150)
        obstacle_mobile.showturtle()
    else:
        obstacle_mobile.hideturtle()

    menu_pen.clear()
    food.showturtle()
    head.showturtle()

    # IDÉE 4 : on réinitialise les statistiques au lancement
    temps_debut = time.time()
    pommes_mangees = 0
    longueur_max = 1

    afficher_score()
    en_menu = False

def facile():
    demarrer(0.15, 0)

def moyen():
    demarrer(0.10, 4)

def difficile():
    demarrer(0.06, 8)

# ============================================================
# REJOUER
# ============================================================
def reset_game():
    global score, direction, next_direction, game_over, grow
    global temps_debut, pommes_mangees, longueur_max
    if not game_over:
        return

    for seg in segments:
        seg.hideturtle()
    segments.clear()

    head.goto(0, 0)
    direction = "stop"
    next_direction = "stop"
    score = 0
    grow = 0
    game_over = False

    temps_debut = time.time()   # IDÉE 4
    pommes_mangees = 0
    longueur_max = 1

    fx, fy = nouvelle_position_libre()
    food.goto(fx, fy)

    if not mode_special:   # IDÉE 2 : si le mode secret est actif, on garde le doré
        head.color(couleur_selon_score(score))   # IDÉE 1 : retour à la couleur de départ

    message_pen.clear()
    afficher_score()

# ============================================================
# CLAVIER
# ============================================================
wn.listen()
wn.onkeypress(facile, "1")
wn.onkeypress(moyen, "2")
wn.onkeypress(difficile, "3")
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(reset_game, "space")

# ============================================================
# ÉCRAN DE MENU (avant le jeu)
# ============================================================
afficher_menu()
while en_menu:
    wn.update()
    time.sleep(0.05)

# ============================================================
# BOUCLE PRINCIPALE DU JEU
# ============================================================
try:
    while True:
        wn.update()

        if game_over:
            time.sleep(DELAY)
            continue

        # 1. Faire suivre le corps AVANT de déplacer la tête
        if segments:
            for i in range(len(segments) - 1, 0, -1):
                x = segments[i - 1].xcor()
                y = segments[i - 1].ycor()
                segments[i].goto(x, y)
            segments[0].goto(head.xcor(), head.ycor())

        # 2. Déplacer la tête (gère aussi le wraparound si activé — IDÉE 6)
        move()

        # 3. Collision avec les murs (désactivée si MODE_SANS_MURS est True)
        if not MODE_SANS_MURS:
            if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
                afficher_game_over("mur")
                time.sleep(DELAY)
                continue

        # 4. Collision avec un obstacle fixe
        collision_obstacle = False
        for obs in obstacles:
            if head.distance(obs) < 20:
                collision_obstacle = True
                break
        if collision_obstacle:
            afficher_game_over("obstacle")
            time.sleep(DELAY)
            continue

        # 4bis. IDÉE 5 : obstacle mobile (déplacement + collision)
        deplacer_obstacle_mobile()
        if obstacle_mobile.isvisible() and head.distance(obstacle_mobile) < 20:
            afficher_game_over("obstacle mobile")
            time.sleep(DELAY)
            continue

        # 5. Manger la nourriture
        if head.distance(food) < 20:
            fx, fy = nouvelle_position_libre()
            food.goto(fx, fy)
            score += 10
            pommes_mangees += 1   # IDÉE 4

            if not mode_special:   # IDÉE 2 : le mode secret garde sa couleur dorée fixe
                head.color(couleur_selon_score(score))   # IDÉE 1

            if score > high_score:
                high_score = score
                sauvegarder_highscore(high_score)
                nom = wn.textinput("Nouveau record !", "Entre ton pseudo :")   # IDÉE 3
                if nom:
                    ajouter_score(nom, score)

            afficher_score()
            grow += 1

        # 6. Faire grandir le serpent si besoin
        if grow > 0:
            seg = turtle.Turtle()
            seg.speed(0)
            seg.shape("square")
            seg.color("grey")
            seg.penup()
            seg.goto(1000, 1000)
            segments.append(seg)
            grow -= 1
            longueur_max = max(longueur_max, len(segments) + 1)   # IDÉE 4

        # 7. Collision avec son propre corps
        for seg in segments:
            if seg.distance(head) < 20:
                afficher_game_over("corps")
                break

        time.sleep(DELAY)

except turtle.Terminator:
    pass

wn.mainloop()