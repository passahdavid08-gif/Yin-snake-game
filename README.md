# 🐍 YIN Snake Game

Recréation du jeu Snake en Python avec le module turtle — menu de difficulté, obstacles, high score et classement persistants, pause, et personnalisation.

## Description

Snake Game est une recréation du jeu classique Snake, développé en utilisant le module graphique "turtle" de Python. Le joueur dirige, à l'aide des touches, un serpent qui grandit à chaque fruit mangé. Le but est de manger le plus de fruits possible sans se heurter aux murs ou à soi-même. Ce mini-projet inclut la sauvegarde du score, la gestion des collisions et un affichage graphique simple. Développé dans le but d'apprendre les bases de la programmation graphique et de la logique de jeu en Python.

## Fonctionnalités

-  Menu de difficulté (Facile / Moyen / Difficile) avec obstacles fixes et un obstacle mobile en mode difficile
-  High score et classement des 5 meilleurs scores, sauvegardés entre les sessions
-  Pause (touche `P`)
- Redémarrage rapide sans fermer la fenêtre (touche `Espace`)
-  Couleur du serpent qui évolue avec le score (vert → jaune → rouge)
-  Mode secret caché
-  Filigrane personnalisé "YIN" en fond d'écran

## Prérequis

- Python 3.x (le module "turtle" est inclus dans la bibliothèque standard, aucune installation supplémentaire n'est nécessaire)

## Installation et lancement

```bash
git clone 
cd yin-snake-game
python snake.py
```

## Contrôles

| Touche | Action |
|---|---|
| Flèches directionnelles | Déplacer le serpent |
| `1` / `2` / `3` | Choisir la difficulté (au menu) |
| `Espace` | Rejouer après un Game Over |
| `P` | Mettre en pause / reprendre |

## Auteur

@yindav

## Pistes d'amélioration futures

- Ajouter des sons lorsque le serpent mange un fruit ou perd
- Ajouter un écran de démarrage avec des boutons cliquables
- Ajouter plusieurs types de nourriture avec des valeurs de points différentes
- Permettre au joueur de choisir la couleur du serpent
- Ajouter une musique de fond
- Ajouter un système de vies
- Ajouter un mode deux joueurs
- Créer un fichier `requirements.txt`
- Ajouter des captures d’écran ou un GIF du jeu dans ce README
- Transformer le jeu en application exécutable avec PyInstaller