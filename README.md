# YIN Snake Game

Recréation du jeu Snake en Python avec le module turtle — menu de difficulté interactif, obstacles, high score et classement persistants, pause, et personnalisation complète.

## Description

Snake Game est une recréation du jeu classique Snake, développée en utilisant le module graphique "turtle" de Python. Le joueur dirige, à l'aide des touches ou de la souris, un serpent qui grandit à chaque fruit mangé. Le but est de manger le plus de fruits possible sans se heurter aux murs, aux obstacles ou à soi-même. Ce mini-projet inclut la sauvegarde persistante du score et d'un classement des meilleurs joueurs, la gestion complète des collisions, un menu interactif, et plusieurs éléments de personnalisation. Développé dans le but d'apprendre les bases de la programmation graphique et de la logique de jeu en Python.

## Fonctionnalités

- Menu de difficulté interactif (boutons cliquables ou touches 1/2/3), avec obstacles fixes et un obstacle mobile en mode difficile
- High score et classement des 5 meilleurs joueurs, sauvegardés entre les sessions
- Saisie du pseudo lors d'un nouveau record, affiché directement dans le menu
- Pause (touche P)
- Redémarrage rapide sans fermer la fenêtre (touche Espace)
- Couleur du serpent évolutive (dégradé arc-en-ciel selon le score), appliquée à la tête et à tout le corps
- Mode secret caché, activable par une séquence de touches
- Statistiques de fin de partie (pommes mangées, longueur max, durée)
- Filigrane personnalisé "YIN" en fond d'écran

## Prérequis

- Python 3.x (les modules turtle, tkinter, json et colorsys sont inclus dans la bibliothèque standard, aucune installation supplémentaire n'est nécessaire)

## Installation et lancement

```bash
git clone https://github.com/passahdavid08-gif/Yin-snake-game.git
cd Yin-snake-game
python snake.py
```

## Version exécutable (.exe)

Une version autonome pour Windows est disponible, ne nécessitant pas d'installation de Python — voir la section "Releases" du dépôt.

## Contrôles

| Touche | Action |
|--------|--------|
| Flèches directionnelles | Déplacer le serpent |
| 1 / 2 / 3 ou clic souris | Choisir la difficulté (au menu) |
| Espace | Rejouer après un Game Over |
| P | Mettre en pause / reprendre |

## Auteur

@Yin_dav

## Pistes d'amélioration futures

- Sons
- Mode sans murs (wraparound) activable depuis le menu
- Niveaux avec obstacles personnalisés
- D'autres modifications proposées seront les bienvenues