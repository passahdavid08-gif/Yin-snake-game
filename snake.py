#====================================
# MINI PROJECT:  YIN SNAKE GAME
#====================================


# Auteur : @yindav


# Description :
# Snake Game est un une recreation du jeu classique Snake, 
# developpé en utilisant le module graphique "turtle" de Python.
# Le joueur dirige a l'aide des touches un serpent qui grandit a chaque fruit mangé. 
# Le but est de manger le plus de fruits possible sans se heurter aux murs ou à soi-même.
# Ce mini-projet inclu la sauvegarde du score, la gestion des collisions et un affichage graphique simple.
# Developpé dans le but d'apprendre les bases de la programmation graphique et de la logique de jeu en Python.


#Etapes de développement :
# 1. Importation des modules nécessaires (turtle, random, time)
# 2. Constantes de configuration du jeu (taille de la fenêtre, taille du serpent, vitesse, etc.)
# 3. Fonction de persistance du score (lecture et écriture dans un fichier)
# 4. Creation de la fenetre et filigrane de personnalisation (titre, couleur de fond, etc.)
# 5. Creation des objets du jeu (serpent, nourriture, score)
# 6. Etat du jeu (initialisation, mise à jour, gestion des collisions, high_score)
# 7. Fonctions de controle du serpent (deplacement, changement de direction)
# 8. Fonction de renitialisation du jeu (reset apres une partie perdue)
# 9. Boucle principale du jeu (mise a jour de l'affichage, gestion des evenements clavier, pause courte entre les frames)
# 10. Gestion de la fin du jeu (affichage du message "Game Over", fermeture propre, option de recommencer)
# 11. Option d'enregistrement du score le plus élevé (high_score) dans un fichier texte pour persistance entre les sessions de jeu.


# Code du jeu Snake avec le module turtle de Python:


import turtle
import time
import random
import json
import tkinter
import colorsys   # NOUVEAU : pour générer un dégradé arc-en-ciel facilement

# ============================================================
# CONSTANTES
# ============================================================
FICHIER_HIGHSCORE = "highscore.txt"
FICHIER_LEADERBOARD = "leaderboard.json"
DELAY = None

MODE_SANS_MURS = False

# Séquence de flèches à reproduire pour débloquer le mode secret.
SEQUENCE_SECRETE = ["Up", "Right", "Down", "Left", "Up", "Left", "Down", "Right"]

LARGEUR_BOUTON = 280
HAUTEUR_BOUTON = 34

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
    classement.sort(key=lambda e: e["score"], reverse=True)
    classement = classement[:5]
    sauvegarder_leaderboard(classement)

# ============================================================
# FENÊTRE DU JEU
# ============================================================
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)
turtle.colormode(255)

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
# ============================================================
obstacle_mobile = turtle.Turtle()
obstacle_mobile.speed(0)
obstacle_mobile.shape("square")
obstacle_mobile.color("purple")
obstacle_mobile.penup()
obstacle_mobile.hideturtle()

direction_obstacle_mobile = 1

def deplacer_obstacle_mobile():
    global direction_obstacle_mobile
    if not obstacle_mobile.isvisible():
        return
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

bouton_pen = turtle.Turtle()
bouton_pen.speed(0)
bouton_pen.hideturtle()
bouton_pen.penup()

# record_pen : .penup() AVANT le .goto() — sans ça, le crayon "posé" par
# défaut trace une ligne visible du centre de l'écran jusqu'ici.
record_pen = turtle.Turtle()
record_pen.speed(0)
record_pen.color("gold")
record_pen.penup()
record_pen.hideturtle()
record_pen.goto(0, 225)

# ============================================================
# ÉTAT DU JEU
# ============================================================
score = 0
high_score = charger_highscore()
game_over = False
en_menu = True
pause = False
grow = 0
direction = "stop"
next_direction = "stop"

temps_debut = 0
pommes_mangees = 0
longueur_max = 1

buffer_touches = []
mode_special = False
pseudo = False
pseudo_actuel = ""

OPPOSES = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

# ============================================================
# IDÉE 1 : COULEUR ÉVOLUTIVE DU SERPENT — VERSION ARC-EN-CIEL
# colorsys.hsv_to_rgb(teinte, saturation, luminosité) convertit une
# simple "teinte" (0 à 1) en couleur RGB. En faisant varier cette teinte
# avec le score, on obtient un dégradé fluide à travers toutes les
# couleurs : rouge → orange → jaune → vert → cyan → bleu → violet.
# Le facteur *0.85 arrête le dégradé avant qu'il ne reboucle sur le rouge.
# ============================================================
def couleur_selon_score(s):
    PALIER_MAX = 250
    t = min(s, PALIER_MAX) / PALIER_MAX
    r, g, b = colorsys.hsv_to_rgb(t * 0.85, 1, 1)
    return (int(r * 255), int(g * 255), int(b * 255))

def colorier_serpent():
    """Applique la couleur actuelle (dorée en mode secret, sinon le
    dégradé arc-en-ciel selon le score) à la TÊTE et à TOUS les
    segments du corps — plus de corps gris figé, tout le serpent
    change de couleur ensemble."""
    couleur = "gold" if mode_special else couleur_selon_score(score)
    head.color(couleur)
    for seg in segments:
        seg.color(couleur)

def afficher_score():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 24, "normal"))

# ============================================================
# IDÉE 2 : CODE SECRET (séquence de flèches)
# ============================================================
def verifier_code_secret(touche):
    global buffer_touches, mode_special
    if buffer_touches and buffer_touches[-1] == touche:
        return   # ignore un appui répété de la même touche (auto-répétition clavier)
    buffer_touches.append(touche)
    buffer_touches = buffer_touches[-len(SEQUENCE_SECRETE):]
    if buffer_touches == SEQUENCE_SECRETE and not mode_special:
        mode_special = True
        colorier_serpent()
        print("✨ Mode secret activé !")

# ============================================================
# DIRECTION DU SERPENT
# ============================================================
def changer_direction(nouvelle):
    global next_direction
    verifier_code_secret(nouvelle)
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
    gerer_murs()

# ==========================
# PAUSE
# ==========================
def toogle_pause():
    global pause
    if game_over or en_menu:
        return
    pause = not pause
    if pause:
        message_pen.goto(0, 0)
        message_pen.write("PAUSE - appuie sur p  pour reprendre", align="center", font=("Arial", 20, "bold"))
    else:
        message_pen.clear()

# ============================================================
# IDÉE 4 : AFFICHAGE UNIFIÉ DU GAME OVER
# ============================================================
def afficher_game_over(raison):
    global game_over
    game_over = True

    if pseudo:
        ajouter_score(pseudo_actuel, score)

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

def dessiner_bouton(y_centre, texte):
    bouton_pen.setheading(0)
    bouton_pen.goto(-LARGEUR_BOUTON / 2, y_centre - HAUTEUR_BOUTON / 2)
    bouton_pen.pendown()
    bouton_pen.fillcolor("#222222")
    bouton_pen.pencolor("white")
    bouton_pen.begin_fill()
    for _ in range(2):
        bouton_pen.forward(LARGEUR_BOUTON)
        bouton_pen.left(90)
        bouton_pen.forward(HAUTEUR_BOUTON)
        bouton_pen.left(90)
    bouton_pen.end_fill()
    bouton_pen.penup()
    bouton_pen.goto(0, y_centre - 7)
    bouton_pen.write(texte, align="center", font=("Arial", 13, "bold"))

# ============================================================
# MENU DE DIFFICULTÉ
# ============================================================
def afficher_menu():
    menu_pen.clear()
    bouton_pen.clear()

    menu_pen.goto(0, 150)
    menu_pen.write(" YIN SNAKE GAME", align="center", font=("Arial", 32, "bold"))
    menu_pen.goto(0, 95)
    menu_pen.write("Clique sur un bouton, ou tape 1 / 2 / 3", align="center", font=("Arial", 15, "normal"))

    dessiner_bouton(40, "1 - Facile (0 obstacle)")
    dessiner_bouton(0, "2 - Moyen (4 obstacles)")
    dessiner_bouton(-40, "3 - Difficile (8 obstacles + mobile)")

    classement = charger_leaderboard()
    if classement:
        menu_pen.goto(0, -100)
        menu_pen.write("Meilleurs scores :", align="center", font=("Arial", 14, "bold"))
        y = -125
        for i, entree in enumerate(classement, start=1):
            menu_pen.goto(0, y)
            menu_pen.write(f"{i}. {entree['nom']} - {entree['score']}", align="center", font=("Arial", 12, "normal"))
            y -= 22

def demarrer(vitesse, nb_obstacles):
    global DELAY, en_menu, temps_debut, pommes_mangees, longueur_max
    global pseudo, pseudo_actuel, pause

    DELAY = vitesse
    pseudo = False
    pseudo_actuel = ""
    pause = False
    record_pen.clear()

    menu_pen.clear()
    bouton_pen.clear()
    generer_obstacles(nb_obstacles)

    if nb_obstacles >= 8:
        obstacle_mobile.goto(0, 150)
        obstacle_mobile.showturtle()
    else:
        obstacle_mobile.hideturtle()

    food.showturtle()
    head.showturtle()

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

def gerer_clic_menu(x, y):
    if not en_menu:
        return

    if abs(x) > LARGEUR_BOUTON / 2:
        return

    if 40 - HAUTEUR_BOUTON / 2 <= y <= 40 + HAUTEUR_BOUTON / 2:
        facile()
    elif 0 - HAUTEUR_BOUTON / 2 <= y <= 0 + HAUTEUR_BOUTON / 2:
        moyen()
    elif -40 - HAUTEUR_BOUTON / 2 <= y <= -40 + HAUTEUR_BOUTON / 2:
        difficile()

# ============================================================
# REJOUER LA PARTIE
# ============================================================
def reset_game():
    global score, direction, next_direction, game_over, grow
    global temps_debut, pommes_mangees, longueur_max
    global pseudo, pseudo_actuel, pause
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

    temps_debut = time.time()
    pommes_mangees = 0
    longueur_max = 1
    pseudo = False
    pseudo_actuel = ""
    pause = False
    record_pen.clear()

    fx, fy = nouvelle_position_libre()
    food.goto(fx, fy)

    colorier_serpent()   # remet la couleur de départ (le corps est déjà vide ici)

    message_pen.clear()
    afficher_score()

# ============================================================
# CLAVIER
# ============================================================
wn.listen()
wn.onkeypress(facile, "1")
wn.onkeypress(moyen, "2")
wn.onkeypress(difficile, "3")
wn.onclick(gerer_clic_menu)
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(reset_game, "space")
wn.onkeypress(toogle_pause, "p")
wn.onkeypress(toogle_pause, "P")

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

        if pause:
            time.sleep(DELAY)
            continue

        # 1. Faire suivre le corps AVANT de déplacer la tête
        if segments:
            for i in range(len(segments) - 1, 0, -1):
                x = segments[i - 1].xcor()
                y = segments[i - 1].ycor()
                segments[i].goto(x, y)
            segments[0].goto(head.xcor(), head.ycor())

        # 2. Déplacer la tête
        move()

        # 3. Collision avec les murs
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

        # 4bis. Obstacle mobile
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
            pommes_mangees += 1

            colorier_serpent()   # tête + corps recolorés ensemble selon le nouveau score

            if score > high_score:
                high_score = score
                sauvegarder_highscore(high_score)

                if not pseudo:
                    nom = wn.textinput("Nouveau record !", "Entre ton pseudo :")
                    wn.listen()
                    pseudo_actuel = nom if nom else "Anonyme"
                    pseudo = True

                record_pen.clear()
                record_pen.write(f"Nouveau record : {pseudo_actuel} !", align="center", font=("Arial", 14, "bold"))

            afficher_score()
            grow += 1

        # 6. Faire grandir le serpent si besoin
        if grow > 0:
            seg = turtle.Turtle()
            seg.speed(0)
            seg.shape("square")
            seg.color("grey")   # couleur de départ temporaire, écrasée juste après
            seg.penup()
            seg.goto(1000, 1000)
            segments.append(seg)
            grow -= 1
            longueur_max = max(longueur_max, len(segments) + 1)
            colorier_serpent()   # recolore immédiatement ce nouveau segment avec les autres

        # 7. Collision avec son propre corps
        for seg in segments:
            if seg.distance(head) < 20:
                afficher_game_over("corps")
                break

        time.sleep(DELAY)

except (turtle.Terminator, tkinter.TclError):
    pass

wn.mainloop()