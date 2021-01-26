import pygame
import sys
from random import*
import math
import time
from pygame import mixer

"""

Toutes les variables avec "player" concernent le vaisseau du joueur.
Toutes les variables avec "ennemi" concernent les vaisseaux ennemis. 
Toutes les variables avec "laser" concernent le tir de laser du joueur. 
Toutes les variables avec "bullet" concernent le tir de feu des ennemis. 

De même : 
width = longueur (cad x)
height = largeur (cad y)

"""

#Initialisation
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800,600))

#Titre et logo
pygame.display.set_caption("Space Invaders by Elisa")
icon = pygame.image.load("images/logo.png")
pygame.display.set_icon(icon)

#Background
background = pygame.image.load("images/galaxy.png")
mixer.music.load("musique/the-edge-of-dawn.mp3")
mixer.music.play(-1)

#Variables
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
BLEU = (17, 76, 159)
running = True
game = False
end = False
win = False
score = 0
lives = 3
bordure = False

#Fonts/SYS
myFont_window_title = pygame.font.SysFont(None, 70)
myFont_window_taille_1 = pygame.font.SysFont(None, 50)
myFont_window_taille_2 = pygame.font.SysFont(None, 35)
myFont_window_taille_3 = pygame.font.SysFont(None, 25)
myFont_game = pygame.font.SysFont(None, 35)

text_space_invaders = "SPACE INVADERS"
text_mission = "Mission : éliminer les vaisseaux ennemis !"
text_rules = "ESPACE : tire des lasers"
text_rules_2 = "FLECHE GAUCHE : déplace le vaisseau vers la gauche"
text_rules_3 = "FLECHE DROITE : déplace le vaisseau vers la droite"
text_start = "APPUYER SUR ENTREE POUR JOUER"
text_musique = "Chanson : The Edge of Dawn"
text_nb_lives = "NOMBRE DE VIE :"
text_name_score = "SCORE :"
text_win = "BRAVO !"
text_game_over = "PERDU !"

label_space_invaders = myFont_window_title.render(text_space_invaders, 1, BLANC)
label_mission = myFont_window_taille_1.render(text_mission, 1, BLANC)
label_rules = myFont_window_taille_2.render(text_rules,1,BLANC)
label_rules_2 = myFont_window_taille_2.render(text_rules_2,1,BLANC)
label_rules_3 = myFont_window_taille_2.render(text_rules_3,1,BLANC)
label_start = myFont_window_taille_1.render(text_start,1,BLANC)
label_musique = myFont_window_taille_3.render(text_musique, 1, BLANC)
label_nb_lives = myFont_game.render(text_nb_lives,1,BLANC)
label_name_score = myFont_game.render(text_name_score, 1, BLANC)
label_win = myFont_window_title.render(text_win, 1, BLANC)
label_game_over = myFont_window_title.render(text_game_over, 1, BLANC)

# Joueur
player_img = pygame.image.load("images/space-ship.png")
player_width, player_height = 80, 80
player_x, player_y = 370, 480
player_x_change, player_y_change = 0, 0
speed_player = 10

# Laser
laser_img = pygame.image.load("images/laser-4.png")
laser_width, laser_height = 8, 32
laser_x, laser_y = 0, player_y
speed_laser = 10
activation_laser = False

# Ennemi(s)
speed_ennemi = 2
ennemi_width, ennemi_height = 64, 64

ennemiX, ennemiY = 2, 36

nb_ennemis_x, nb_ennemis_y = 8, 3
nb_ennemis = nb_ennemis_x*nb_ennemis_y
ennemi_img = []
ennemi_x = []
ennemi_y = []
ennemis_éliminés = []

#Création des ennemis
for j in range(nb_ennemis_y):
    for i in range (nb_ennemis_x):
        ennemi_img.append(pygame.image.load("images/enemy.png"))
        ennemi_x.append(ennemiX + (i*74))
        ennemi_y.append(ennemiY + (j*69))

# Bullet
bullet_width, bullet_height = 8, 32
speed_bullet = 6
bullet_img = []
bullet_x = []
bullet_y = []
nb_bullet = 5
activation_bullet = [False for x in range(nb_bullet)]

#Création des bullet
for x in range (nb_bullet):
    bullet_img.append(pygame.image.load("images/bullet-2.png"))
    bullet_x.append(0)
    bullet_y.append(0)

# FONCTIONS
"""Fonctions de mouvement"""
def player(x,y):
    screen.blit(player_img, (x, y))

def ennemi(x,y,i):
    screen.blit(ennemi_img[i], (x,y))

def lancement_laser(x,y):
    screen.blit(laser_img,(x+(player_width/2 - laser_width/2),y))

def lancement_bullet(x,y,i):
    screen.blit(bullet_img[i],(x+(ennemi_width/2 - bullet_width/2),y+ennemi_height))

"""Fonctions de détection"""
def extrêmité_player(x,y):
    if x <= 0:
        x = 0
    elif x >= (800-player_width):
        x = 800-player_width
    return (x, y)

def détection_bordure(ennemi_x):
    if ennemi_x <= 0 or ennemi_x >= (800-ennemi_width):
        return True
    else:
        return False

def détection_ennemi(ennemi_x, ennemi_y, laser_x, laser_y):
    distance = math.sqrt(pow(ennemi_x - laser_x, 2) + pow(ennemi_y - laser_y, 2)) # formule de la distance
    if distance < 35:
        return True
    else:
        return False

def détection_player(player_x, player_y, bullet_x, bullet_y):
    distance = math.sqrt(pow(player_x - bullet_x, 2) + pow(player_y - bullet_y, 2))
    if distance < 35:
        return True
    else:
        return False

while running: 

    # quitter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game = True

    screen.blit(background, (0, 0))
    screen.blit(label_space_invaders, (220, 50))
    screen.blit(label_mission, (50, 150))
    screen.blit(label_rules, (50, 250))
    screen.blit(label_rules_2, (50, 300))
    screen.blit(label_rules_3, (50, 350))
    screen.blit(label_start, (75, 450))
    screen.blit(label_musique, (550, 550))
    pygame.display.update()

    while game:
        screen.blit(background, (0, 0))

        # Quitter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Déplacement du vaisseau / Activation du laser
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= speed_player
            if event.key == pygame.K_RIGHT:
                player_x += speed_player

            if event.key == pygame.K_SPACE and activation_laser == False:
                activation_laser = True
                laser_x = player_x

        # vérifie et bloque les extrêmités
        coordonnées_player = extrêmité_player(player_x,player_y)
        player_x, player_y = coordonnées_player[0], coordonnées_player[1]

        #affiche le nombre de vie
        text_lives = str(lives)
        label_lives = myFont_game.render(text_lives, 1, BLANC)
        screen.blit(label_nb_lives, (500, 3)) # "NOMBRE DE VIE :"
        screen.blit(label_lives, (750, 3))    # [3, 2, 1]

        #affiche le score
        text_score = str(score)
        label_score = myFont_game.render(text_score, 1, BLANC)
        screen.blit(label_name_score, (15,3)) # "SCORE :"
        screen.blit(label_score, (150, 3))    # [score]

        #Fait accélérer la vitesse - bullet
        if score > 10:
            speed_bullet = 7
        if score > 15:
            speed_bullet = 8

        if end == False:

            # Mouvement de l'ennemi + Collision ennemi-laser
            for i in range(nb_ennemis):
                if i not in ennemis_éliminés: # vérifie si un ennemi doit apparaître
                    ennemi_x[i] += speed_ennemi
                    ennemi(ennemi_x[i], ennemi_y[i],i)

                    # vérifie la collision
                    collision = détection_ennemi(ennemi_x[i], ennemi_y[i], laser_x, laser_y)

                    # vérifie l'activation de bullet
                    test_bullet = randint(1,100)
                    if test_bullet < 10 and (False in activation_bullet):
                            stop = 0
                            for x in range(nb_bullet):
                                if activation_bullet[x] == False and stop == 0:
                                    activation_bullet[x] = True
                                    bullet_x[x] = ennemi_x[i]
                                    bullet_y[x] = ennemi_y[i]
                                    stop = 1

                else:
                    collision = False

                if détection_bordure(ennemi_x[i]):
                    bordure = True

                if collision:
                    explosion_player = mixer.Sound("musique/explosion-player.wav")
                    explosion_player.play()
                    laser_y = 480
                    activation_laser = False
                    score += 1
                    ennemis_éliminés.append(i)

                if nb_ennemis == len(ennemis_éliminés):
                    win = True
                    end = True

            # Direction des ennemis
            if bordure:
                speed_ennemi = -speed_ennemi
                bordure = False

            #Mouvement - laser
            if activation_laser:
                lancement_laser(laser_x,laser_y)
                laser_y -= speed_laser

            #Mouvement - bullet
            for j in range (nb_bullet):
                if activation_bullet[j]:
                    lancement_bullet(bullet_x[j], bullet_y[j], j)
                    bullet_y[j] += speed_bullet

                crash = détection_player(player_x, player_y, bullet_x[j], bullet_y[j])

                if crash: #Collision - bullet/player
                    lives -= 1
                    bullet_x[j], bullet_y[j] = 0, 0
                    explosion_ennemi = mixer.Sound("musique/explosion-ennemi.wav")
                    explosion_ennemi.play()
                    activation_bullet[j] = False

            #Bloquer l'extrêmité haute - laser
            if laser_y <= 0:
                laser_y = 480
                activation_laser = False

            #Bloquer l'extrêmité basse - bullet
            for x in range(nb_bullet):
                if activation_bullet[x]:
                    if bullet_y[x] >= 600:
                        bullet_y[x] = 0
                        activation_bullet[x] = False

            if lives == 0:
                end = True

        player(player_x, player_y)
        pygame.display.update()

        if end:
            game = False

    if win: #affiche "BRAVO !"
        screen.blit(background, (0, 0))
        screen.blit(label_win,(320,50))
        pygame.display.update()
        time.sleep(3)
        running = False

    elif end: # affiche "PERDU !"
        screen.blit(background, (0, 0))
        screen.blit(label_game_over, (320,50))
        pygame.display.update()
        time.sleep(3)
        running = False
        
#sys.exit()
pygame.quit()
