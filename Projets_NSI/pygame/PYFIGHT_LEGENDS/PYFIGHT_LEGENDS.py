import pygame
from pygame.locals import *
from assets.module import *
import textwrap
from random import randint
import sys
import os

#  /!\  /!\ VERSION DU CODE POUR LA CONVERSION EN .exe  /!\  /!\               #

def get_resource_path(relative_path):
    """Obtenir le chemin absolu pour une ressource embarquée."""
    # Si l'application est empaquetée avec PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, *relative_path.split('/'))
    # Si le programme est exécuté directement
    return os.path.join(os.path.abspath("."), *relative_path.split('/'))

pygame.init()

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# PROGRAMME PRINCIPAL                                                          #
# /!\ CE PROGRAMME NECESSITE LE PROGRAMMME 'module.py' /!\                     #
# /!\IL NECESSITE AUSSI LES FICHIERS ANNEXES /!\                               #
# Lire 'READ_ME.txt' pour plus d'informations                                  #

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #


# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# /|PLAN DU CODE|/:                                                            #
#( numéro de ligne faux a cause du rajout de la fonction get_resource_path )   #

# I) def de la fenètre                                                 (l-36)  #
# II) chargemement de la map                                           (l-45)  #
# IV) position joueur + rotation                                       (l-51)  #          
# V) chargement des boutons du jeu                                     (l-72)  # 
# VI) chargement des images du jeu                                     (l-96)  # 
# VII) polices d'écritures et textes                                   (l-113) #
# VIII) variables boutons                                              (l-166) #
# IX) chargement des quêtes                                            (l-192) #
# X) chargement des sons                                               (l-199) #
# XI) fonctions d'affichage + fonction reset des quêtes                (l-220) #
# XII) BOUCLE DU JEU                                                   (l-332) #

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

clock = pygame.time.Clock()
pygame.key.set_repeat(400,30)    
# Defini la taille de la fenêtre de jeux #  
screen = pygame.display.set_mode((1000,600))        
pygame.display.set_caption('PYFIGHT LEGENDS')
screen = pygame.display.get_surface()

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# Charge la maps et change ça taille #
background = pygame.image.load(get_resource_path("assets/background.png")).convert()
backgroundRect = background.get_rect()
background = pygame.transform.scale(background, (3700, 2800))

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# Chargement des differents personnages #
def load_perso():
    perso = Personnage("Bob",10,10,[get_resource_path("assets/Perso1.png"),get_resource_path("assets/Perso2.png"),get_resource_path("assets/Perso3.png"),get_resource_path("assets/Perso4.png")],screen,10,1,1,0,100,1,5)
    mobs = Personnage("mechant",10,10,[get_resource_path("assets/Ennemi1.png"),get_resource_path("assets/Ennemi2.png"),get_resource_path("assets/Ennemi3.png"),get_resource_path("assets/Ennemi4.png")],screen,0,0,0,0,100,0,1)
    return perso,mobs
perso,mobs = load_perso()

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# Variable pour le calcule des positions de cartains élements tel que pour le lieu de spawn du perso principal  # 
fond_x = -100 
fond_y = -685 
rotation = 0 # sprite 0 du perso
direction = 1 # Direction initiale du mobs (1 pour droite, -1 pour gauche)

# Position de base du mob # 
valeur_pos_mob_x = 650
pos_x = 200

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# Définie les boutons et charge les images pour les boutons #
button = ImageButton(get_resource_path("assets/bouton1.png"), 15, 15, 60, 60)  
image_choix_touche = ImageButton(get_resource_path("assets/exit.png"), 240, 190, 60, 60)
quit_game = ImageButton(get_resource_path("assets/exit.png"), 240, 290, 60, 60)
affiche_coord = ImageButton(get_resource_path("assets/exit.png"), 240, 390, 60, 60)
button_show_quete1 = ImageButton(get_resource_path("assets/bouton3.png"), 340, 190, 60, 60)
button_show_quete2 = ImageButton(get_resource_path("assets/bouton3.png"), 340, 290, 60, 60)
button_fight = ImageButton(get_resource_path("assets/bouton3.png"), 240, 190,60, 60)
button_exit_quetes = ImageButton(get_resource_path("assets/exit.png"), 15, 15, 60, 60)
button_item_potion = ImageButton(get_resource_path("assets/popo1.png"), 240, 190, 60, 60)
button_item_livre = ImageButton(get_resource_path("assets/book1.png"), 240, 260, 60, 60)
button_item_potion2 = ImageButton(get_resource_path("assets/popo2.png"), 240, 330, 60, 60)
recommencer = ImageButton(get_resource_path("assets/exit.png"), 460, 360, 75,80)
quit_quetes = ImageButton(get_resource_path("assets/exit.png"), 460, 360, 75,80)
bouton_play = ImageButton(get_resource_path("assets/button_play.png"), 400, 490, 200,70)
boutton_egg = ImageButton(get_resource_path("assets/on.png"), 960, 10, 25, 25)
# boutons décoratifs
coin_img = ImageButton(get_resource_path("assets/coin.png"), 860, 533, 45,45)
xp_img = ImageButton(get_resource_path("assets/exp.png"), 860,475, 45,45)
vie_img = ImageButton(get_resource_path("assets/hp.png"), 265,538, 35,35)
speed_img = ImageButton(get_resource_path("assets/speed.png"), 860, 420, 45,45)

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# Définie les images a afficher #
def load_img(nom,size,centre = (0,0)):
    images = pygame.image.load(nom)
    images = pygame.transform.scale(images,size)
    images_rect = images.get_rect(center=centre)
    return images , images_rect

settingpng,settingpng_rect = load_img(get_resource_path("assets/pancarte.png"),(900,550),(500, 240))
menuquetes,menuquetes_rect = load_img(get_resource_path("assets/pancarte.png"),(900,550),(500, 240)) #(1100,700),(700, 300)
menushop,menushop_rect = load_img(get_resource_path("assets/pancarte.png"),(900,550),(500, 240))
game_over_img,game_over_img_rect = load_img(get_resource_path("assets/game_over.jpg"),(1000, 600))
winner_quete_img,winner_quete_img_rect = load_img(get_resource_path("assets/winner_image.png"),(1000, 600))
bienvenue_img,bienvenue_img_rect = load_img(get_resource_path("assets/cadre.png"),(1000, 600))


# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# definition les polices #
font=pygame.font.Font(get_resource_path("assets/font_like_mc.ttf"), 30)
font_titre = pygame.font.Font(get_resource_path("assets/font_titre.ttf"), 40)
font2 = pygame.font.Font(get_resource_path("assets/font_pix_mc.ttf"), 30)
fontdebug = pygame.font.Font(None, 30)
font_deco = pygame.font.Font(get_resource_path("assets/font_videogames.ttf"), 60)
font_bienvenue = pygame.font.Font(get_resource_path("assets/Bake_Soda.otf"), 30)
font_titre_jeux  = pygame.font.Font(get_resource_path("assets/font_titre.ttf"), 28)
font_fleche = pygame.font.Font(get_resource_path("assets/PixArrows.ttf"), 28)
font_zqsd = pygame.font.Font(get_resource_path("assets/Gameplay.ttf"), 20)

# Définie tout les textes #
text_pnj1 = font2.render("Press Space",1,(255,255,255))
texte_setting = font_titre .render("Parametre",1,(255,255,255))
touche_conf1 =  font.render("Controle : config ",1,(255,255,255))
fleche_txt =  font_fleche.render("mNnM",1,(255,255,255))
touche_conf2 =  font.render("Controle : config ",1,(255,255,255))
zqsd_txt = font_zqsd.render("zqsd",1,(255,255,255))
quit_txt = font.render("Quitter le jeu",1,(255,255,255))
coord_txt_setting = font.render("afficher coordonnees",1,(255,255,255))
quetes1_txt = font.render("quetes 1",1,(255,255,255))
quetes2_txt = font.render("quetes 2",1,(255,255,255))
titre_quetes = font_titre.render("Quetes ! ",1,(255,255,255))
titre_shop = font_titre.render("Shop ! ",1,(255,255,255))
potion_txt = font.render("potion soin",1,(255,255,255))
livre_txt = font.render("livre ",1,(255,255,255))
potion2_txt = font.render("potion speed",1,(255,255,255))
nb_max_txt_potion = font.render("nombre max de potion soin atteint ",1,(255,255,255))   
nb_max_txt_livre = font.render("nombre max de livre atteint ",1,(255,255,255))
nb_max_txt_potion2 = font.render("nombre max de potion vitesse atteint ",1,(255,255,255))
level_ok_txt = font2.render("niveau 4 requis",1,(255,255,255))


bienvenue_txt = """Bienvenue sur                           
But du jeu :                            
Faire les quetes disponibles en bas de la maps a droite
puis battre le boss final                                
Pour vous aider des items sont disponible a l'achat dans le shop
potions de soin , livres d'attaque , potions de vitesse pour les deplacements 
_________________________________ 
Moquet Titouan ~ Devallan Flavien 
                       
2024~2025"""

max_width = 750  # Largeur maximale de la zone d'affichage (en pixels)
lines = textwrap.wrap(bienvenue_txt, width=40)  # 40 caractères par ligne

titre_jeux = font_titre_jeux.render("PYFIGHT LEGENDS !",1,(235,159,7))
texte_deco = font_deco.render(".",1,(0,0,0))

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# Définie si les éléments doivent être affichés ou non (variable modifiable via les boutons du jeu) #
bienvenue =True 
show_quetes = False 
affiche_texte = False
show_boss = False    
show_setting = False
show_shop = False
show_quete1 = False 
show_quete2 = False
coord_debug = False
nb_max_potion = False
nb_max_livre = False
nb_max_potion2 = False
game_over_quete = False 
winner_quete = False
game_over = False
level_ok = False
max_livre = False
max_potion = False
max_potion2 = False
perso_skin_egg = False
boss_battu = False
arriver_mob = False
# Definie le mode de base des touches : True -> flèches ; modifiable dans les parametres du jeu #
mode_touche = True

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# Definie les quêtes et le boss #
Quete1 = Quêtes(get_resource_path("assets/fight.png"),1,perso,mobs,get_resource_path("assets/Perso1.png"),get_resource_path("assets/Ennemi3.png"))
Quete2 = Quêtes(get_resource_path("assets/fight.png"),2,perso,mobs,get_resource_path("assets/Perso1.png"),get_resource_path("assets/Ennemi3.png"))
Boss_final = Quêtes(get_resource_path("assets/fight.png"),3,perso,mobs,get_resource_path("assets/Perso1.png"),get_resource_path("assets/boss.png"))

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

# Chargement des sons du jeux #
pygame.mixer.init()
son_ambiance = pygame.mixer.Sound(get_resource_path("assets/sfx_main_atmosphere.ogg"))
son_ambiance.set_volume(0.2)
son_ambiance.play(loops =-1,maxtime =0,fade_ms =0 )

son_click = pygame.mixer.Sound(get_resource_path("assets/sfx-pop.ogg"))
son_click.set_volume(0.2)

son_cash = pygame.mixer.Sound(get_resource_path("assets/sfx_cash.ogg"))
son_cash.set_volume(0.2)

son_game_over = pygame.mixer.Sound(get_resource_path("assets/sfx_game_over.ogg"))
son_game_over.set_volume(0.8)
bruit_jouer = False

son_ambiance_quete = pygame.mixer.Sound(get_resource_path("assets/Musique_test_quete.ogg"))
son_ambiance_quete.set_volume(0)
son_ambiance_quete.play(loops =-1,maxtime =0,fade_ms =0 )

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

##  FONCTIONS ##
# affichage #
def bienvenue_msg():
    screen.blit(bienvenue_img,(0,0))
    y_position = 45
    
    for line in lines:
        text_surface = font_bienvenue.render(line, True, (255, 255, 255)) 
        screen.blit(text_surface, (175, y_position))  
        y_position += 40  
        
    bouton_play.draw(screen)
    screen.blit(texte_deco, (55,510))
    screen.blit(titre_jeux, (420,50))
    
def affichage_base():
    pygame.display.update()
    screen.fill(0)
    screen.blit(background, (fond_x, fond_y))
    mobs.afficheV2(screen,x,y)
    perso.affiche(screen)
    button.draw(screen)
    health_bar.draw(screen)
    coin_img.draw(screen)
    xp_img.draw(screen)
    vie_img.draw(screen)
    speed_img.draw(screen)
    screen.blit(perso_argent_txt,(910,540))
    screen.blit(perso_speed_txt,(910,430))
    screen.blit(vie_perso_txt,(500,543))
    screen.blit(level_perso_txt,(910,483))
    if boss_battu is True :
        boutton_egg.draw(screen)
    
def affiche_shop(nb_potion_txt,nb_livre_txt,nb_potion2_txt):
    screen.blit(menushop,menushop_rect)   
    button_item_potion.draw(screen) 
    button_item_livre.draw(screen)
    button_item_potion2.draw(screen)
    screen.blit(titre_shop,(400,70))
    screen.blit(potion_txt,(320,205))
    screen.blit(livre_txt,(320,275))
    screen.blit(potion2_txt,(320,345))
    screen.blit(nb_potion_txt,(550,205))
    screen.blit(nb_livre_txt,(550,275))
    screen.blit(nb_potion2_txt,(550,345))
    
    if max_potion is True :
        screen.blit(nb_max_txt_potion,(240,400)) 
    if max_livre is True  :
        screen.blit(nb_max_txt_livre,(240,400))
    if max_potion2 is True :
        screen.blit(nb_max_txt_potion2,(200,400))
        
def affiche_menu_quetes():
    screen.blit(menuquetes, menuquetes_rect)
    screen.blit(titre_quetes, (380,70))
    button_show_quete1.draw(screen)
    screen.blit( quetes1_txt,(420,205))
    button_show_quete2.draw(screen)
    screen.blit( quetes2_txt,(420,305))

def affiche_parametres():
    screen.blit(settingpng, settingpng_rect)
    image_choix_touche.draw(screen)
    screen.blit(texte_setting, (340,70))
    if mode_touche == True :
        screen.blit(touche_conf1,(320,205)) 
        screen.blit(fleche_txt,(600,205))
    else:
        screen.blit(touche_conf2,(320,205))
        screen.blit(zqsd_txt,(600,205))
    quit_game.draw(screen)
    screen.blit(quit_txt,(320,310))
    affiche_coord.draw(screen)
    screen.blit(coord_txt_setting,(320,405))

       
def affiche_espace():
    # Affiche "Press Space" dans la zone definie 
    if -2400<fond_x<-1700 and -850<fond_y<-400 :
        screen.blit(text_pnj1,(30,540))   #(400,490)
    
    if -200<fond_x<170 and -2020<fond_y<-1700:
        if perso.level <= 3 :
            screen.blit(level_ok_txt , (15,540))
        else :
            screen.blit(text_pnj1, (30,540))
 
    if -2520<fond_x<-2100 and -2030<fond_y<-1500 :
        screen.blit(text_pnj1, (30,540))
        
# collision avec le mob sur la map principal # 
def collision_mobs():
    perso.update_rect(460,220)
    mobs.update_rect(x, y)
    if perso.collision(mobs.rect) and show_quete1 is False and show_quete2 is False and show_quetes is False and show_setting is False and show_boss is False:
        perso.pv -=0.1  

# reset des quêtes # 
def reset(la_quete,personne):
    la_quete.health_bar.hp = 100
    la_quete.mob.health_bar.hp = 100
    la_quete.valeur_debug = 0
    personne.livre = la_quete.nb_livre 
    personne.potion =la_quete.nb_potion 
    la_quete.quitter = False
    la_quete.perso_actif = True
    la_quete.livre_use = 0

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

## BOUCLE PRINCIPALE DU JEU ##

loop = True
while loop:
    health_bar = HealthBar(260,540, 550, 35, perso.pv)
    
    if perso.pv <= 0:
        game_over = True
        
    # |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #
        
    ## Definie le mode de touche pour le deplacement du joueur par défaut : les flèches ##
    if mode_touche == True:
        touche_left = K_LEFT
        touche_right =K_RIGHT
        touche_up = K_UP
        touche_down =K_DOWN
    else :
        touche_left = K_q
        touche_right = K_d
        touche_up = K_z
        touche_down = K_s
         
   # |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #
         
    ## Event ##
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        
        if event.type == KEYUP and event.key ==  K_ESCAPE :
            show_setting = False
            bienvenue = False
           
        #affichage des élements suivant si le joueur est dans la zone definie et si la touche espace est pressé
        if -2400<fond_x<-1700 and -850<fond_y<-400 :      
            if event.type == KEYUP and event.key ==  K_ESCAPE  and show_setting is False and show_shop is True and game_over is False:
                show_shop = False 
            
            if show_setting == False : 
                if event.type == KEYUP and event.key ==  K_SPACE :
                    show_shop = not show_shop
                                       
        if -200<fond_x<170 and -2020<fond_y<-1700:
            if show_setting == False and perso.level >= 4 : 
                if event.type == KEYUP and event.key ==  K_SPACE :
                    show_boss = True
                    
        if -2520<fond_x<-2100 and -2030<fond_y<-1500 :
            if event.type == KEYUP and event.key ==  K_ESCAPE  and show_setting is False and show_quetes is True and game_over is False:
                show_quetes = False 
            if show_setting == False : 
                if event.type == KEYUP and event.key ==  K_SPACE :
                    show_quetes = not show_quetes        
        
        ## Vérifier si le bouton est cliqué ##
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if bouton_play.is_clicked(event) and bienvenue is True : # bouton demarage du jeu
                bienvenue = False 
            
            # bouton d'acces au paramèmetre 
            if button.is_clicked(event) and show_quete1 is False and show_quete2 is False and game_over is False and show_boss is False and game_over is False and game_over_quete is False and winner_quete is False and bienvenue is False :
                son_click.play()
                show_setting = not show_setting
                
            if show_setting is True: # boutons des paramètres
                if quit_game.is_clicked(event):
                    son_click.play()
                    loop = False
                if image_choix_touche.is_clicked(event):
                    son_click.play()
                    mode_touche = not mode_touche
                if affiche_coord.is_clicked(event) :
                    son_click.play()
                    coord_debug = not coord_debug
                
                
                
            if boutton_egg.is_clicked(event) and boss_battu is True: # Changement du skin du joueur (uniquemet disponible après avoir vaincu le boss ) 
                if perso_skin_egg is False :
                    perso.update_sprites([get_resource_path("assets/Perso5.png"),get_resource_path("assets/Perso6.png"),get_resource_path("assets/Perso7.png"),get_resource_path("assets/Perso8.png")])
                    Quete1.update_image_perso([get_resource_path("assets/Perso5.png")])
                    Quete2.update_image_perso([get_resource_path("assets/Perso5.png")])
                    Boss_final.update_image_perso([get_resource_path("assets/Perso5.png")])
                    boutton_egg.update_img_button([get_resource_path("assets/off.png")],25,25)
                    perso_skin_egg = True
                    
                elif perso_skin_egg is True :
                    perso.update_sprites([get_resource_path("assets/Perso1.png"),get_resource_path("assets/Perso2.png"),get_resource_path("assets/Perso3.png"),get_resource_path("assets/Perso4.png")])
                    Quete1.update_image_perso([get_resource_path("assets/Perso1.png")]) 
                    Quete2.update_image_perso([get_resource_path("assets/Perso1.png")])
                    Boss_final.update_image_perso([get_resource_path("assets/Perso1.png")])
                    boutton_egg.update_img_button([get_resource_path("assets/on.png")],25,25)
                    perso_skin_egg = False
                    
                    
            if show_quetes == True and show_quete1 == False and show_quete2 == False and game_over is False and winner_quete is False and bienvenue is False: # affichage des quêtes 1 et 2 
                if button_show_quete1.is_clicked(event):
                    son_click.play()
                    show_quete1 = True 
                    
                if button_show_quete2.is_clicked(event):
                    son_click.play()
                    show_quete2 = True 
        
            if show_shop == True : # achat des items 
                if button_item_potion.is_clicked(event) and perso.argent > 0 and perso.potion < 10: 
                    son_cash.play()
                    perso.potion+=1
                    perso.argent-=5
                    Quete1.nb_potion +=1
                    Quete2.nb_potion +=1
                    Boss_final.nb_potion += 1
                    max_livre = False
                    max_potion = False
                    max_potion2 = False
                    
                if button_item_livre.is_clicked(event) and perso.argent > 0 and perso.livre < 10 :
                    son_cash.play()
                    perso.livre+=1
                    perso.argent-=5
                    Quete1.nb_livre +=1
                    Quete2.nb_livre +=1
                    Boss_final.nb_livre += 1
                    max_livre = False
                    max_potion = False
                    max_potion2 = False
                    
                if button_item_potion2.is_clicked(event) and perso.argent > 0 and perso.potion2 < 5:
                    son_cash.play()
                    perso.potion2 += 1
                    perso.vitesse += 1
                    perso.argent-=5
                    max_livre = False
                    max_potion = False
                    max_potion2 = False
                # affichage si le nombre maxi d'item a été acheté
                if perso.potion > 9 and button_item_potion.is_clicked(event):
                    max_potion = True
                    max_livre = False
                    max_potion2 = False
                    
                if perso.livre > 9 and button_item_livre.is_clicked(event):
                    max_potion = False
                    max_livre = True
                    max_potion2 = False
                    
                if perso.potion2 > 4 and button_item_potion2.is_clicked(event):
                    max_potion = False
                    max_livre = False
                    max_potion2 = True
                    
            if show_shop == False:
                max_livre = False
                max_potion = False
                max_potion2 = False
                    
            # Game_over #     
            if game_over is True :       
                if recommencer.is_clicked(event) : # "recommence" le jeu depuis le debut si le joueur est mort et décide de recommencer
                    perso.pv = 100
                    perso.livre = 1
                    perso.potion = 1
                    perso.argent = 10
                    perso.level = 1 #réinitialise les variables du joueur 
                    fond_x = -100 
                    fond_y = -685  # fait apparaitre le personnage au point de depart 
                    game_over = False
                    max_livre = False
                    max_potion = False
                    max_potion2 = False
                    
                    show_setting, show_shop, show_quetes, show_boss, show_quete1, show_quete2 = False, False, False, False, False, False
                    bruit_jouer = False
                         
            if game_over_quete is True or winner_quete is True : # quitte la quête sans modifier les variables du joueur (+ argent +level en cas de victoire )
                if quit_quetes.is_clicked(event):
                    game_over_quete = False
                    winner_quete = False 
                    show_setting, show_shop, show_quetes, show_boss, show_quete1, show_quete2 = False, False, False, False, False, False
                    bruit_jouer = False
                    son_ambiance_quete.set_volume(0)
                    son_ambiance.set_volume(0.2)
                    
            
    
    # |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #
    
    # Permet de déplacer le personnages           
    # Si un menu est affiché le joueur ne peut plus bouger
    if show_setting is False and show_quetes is False and show_shop is False and show_boss is False and game_over is False and winner_quete is False and bienvenue is False :
        fond_x,fond_y = perso.mouvement(fond_x,fond_y,touche_left,touche_right,touche_up,touche_down) # code pour le deplacement dans la class
    
    # |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #
    
    ## CHEAT ## ctrl + ...
    dicKeys = pygame.key.get_pressed()   
    if dicKeys[K_LCTRL] :
        if perso.argent<= 5000 :
            if dicKeys[K_w]:           
                perso.argent+=20
                      
        if dicKeys[K_v] and show_quetes is True:
            Quete1.mob.health_bar.hp -= 20
        
        if dicKeys[K_b] and show_quetes is True:
            Quete2.mob.health_bar.hp -= 20
            
        if dicKeys[K_n] and show_boss is True :
            Boss_final.mob.health_bar.hp -= 20
            
        if dicKeys[K_p] and show_boss is False and show_quetes is False and show_setting is False and show_shop is False :
            perso.pv -=5
        
        if dicKeys[K_l] :
            perso.level = 4
            
        if dicKeys[K_i] :
            bienvenue = True
    
    # |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #
    
    ## Mouvement Mob ##
    if pos_x >= 200  and arriver_mob is False : 
        valeur_pos_mob_x += mobs.vitesse
        pos_x += 1
        mobs.rotation = 1
    
    if pos_x == 200  and arriver_mob is True :
        arriver_mob = False
    
    if pos_x == 2000 and arriver_mob is False:
        arriver_mob = True
        
    if pos_x <= 2000 and arriver_mob is True:
        valeur_pos_mob_x -= mobs.vitesse
        pos_x-=1
        mobs.rotation = 2
        
    
    x = fond_x +valeur_pos_mob_x 
    y = fond_y +1500
    
    # |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #
    
    ## Definie les textes qui sont actualisés à chaque tour de bouble ##
    position = fontdebug.render(f"pos x:{fond_x} y:{fond_y}",1,(255,255,255)) 
    nb_potion_txt = font2.render(f"{perso.potion}",1,(255,255,255))
    nb_livre_txt = font2.render(f"{perso.livre}",1,(255,255,255))
    nb_potion2_txt = font2.render(f"{perso.potion2}",1,(255,255,255))
    perso_argent_txt = font2.render(f"{perso.argent}",1,(255,255,255))
    perso_speed_txt = font2.render(f"{perso.vitesse}",1,(255,255,255))
    vie_perso_txt = font2.render(f"{round(perso.pv)}",1,(255,255,255))  #round
    level_perso_txt = font2.render(f"{perso.level}",1,(255,255,255))
    
    # |//||//||//||//||//||//||//||//||//||//||//||//||//||//||//||//||//||//||//| # 
    
    ## Affichage des images de base + perso + mob + bouton + ... ##
    affichage_base()
    ## Collision avec le mob ##
    collision_mobs()
    ## Affiche les "press space " au bon endroit ## 
    affiche_espace()
    
    ## Affichage des élements masquables ##
    if bienvenue is True :
        bienvenue_msg()
        
    if show_shop == True :                               
        affiche_shop(nb_potion_txt,nb_livre_txt,nb_potion2_txt)
        
    if show_quetes == True:                                  
        affiche_menu_quetes()
        
    # quêtes # 
    if show_quete1 == True :
        # lancement + changement de musique 
        Quete1.quitter = False
        Quete1.game(screen,event)
        perso.livre = Quete1.nb_livre
        perso.potion = Quete1.nb_potion
        son_ambiance.set_volume(0)
        son_ambiance_quete.set_volume(0.3)
        # condition de fin 
        if Quete1.mob.health_bar.hp <= 0:
            winner_quete = True
            perso.argent += 10
            perso.level += 1
            Quete1.quitter = True
                
        elif Quete1.health_bar.hp <= 0 : 
            Quete1.quitter = True
            game_over_quete = True
            
        if Quete1.quitter is True: # fin de la quête
            show_quete1 = False
            reset(Quete1,perso)
                
    elif show_quete2 == True :
        Quete2.game(screen,event)
        perso.livre = Quete2.nb_livre
        perso.potion = Quete2.nb_potion
        son_ambiance.set_volume(0)
        son_ambiance_quete.set_volume(0.3)
        
        if Quete2.mob.health_bar.hp <= 0:
            winner_quete = True
            perso.argent += 30
            perso.level +=1
            Quete2.quitter = True
                
        elif Quete2.health_bar.hp <= 0 :
            game_over_quete = True
            Quete2.quitter = True
            
        if Quete2.quitter is True:
            show_boss = False
            reset(Quete2,perso)
            
    elif show_boss == True :
        Boss_final.game(screen,event)
        perso.livre = Boss_final.nb_livre
        perso.potion = Boss_final.nb_potion
        son_ambiance.set_volume(0)
        son_ambiance_quete.set_volume(0.3)
        
        if Boss_final.mob.health_bar.hp <= 0:
            winner_quete = True
            boss_battu = True 
            perso.argent += 100
            perso.level +=2
            Boss_final.quitter = True
                
        elif Boss_final.health_bar.hp <= 0 :
            Boss_final.quitter = True
            game_over_quete = True
            
        if Boss_final.quitter is True:
            show_boss = False
            reset(Boss_final,perso)
           
    # reste des éléments #
    if show_setting == True:                               
        affiche_parametres()
        
    if coord_debug == True and show_boss is False and show_quete2 is False and show_quete1 is False : # affichage des coordonnées "du joueur" ( c'est la map qui se deplace ) 
        screen.blit(position, (100,10))

    if game_over is True : # reset de tous le jeu (voir plus haut) 
        screen.blit (game_over_img,(0,0))
        recommencer.draw(screen)
        show_setting = False
        show_shop = False
        show_quetes = False
        show_boss = False
        show_quete1 = False
        show_quete2 = False
        if bruit_jouer is False :
            son_game_over.play()
            bruit_jouer = True
    
    if game_over_quete is True : # fin de la quête en cour (voir plus haut) 
        screen.blit (game_over_img,(0,0))
        quit_quetes.draw(screen)
        show_setting = False
        show_shop = False
        show_quetes = False
        show_boss = False
        show_quete1 = False
        show_quete2 = False
        if bruit_jouer is False :
            son_game_over.play()
            bruit_jouer = True

    if winner_quete is True : # fin de la quête en cour (voir plus haut) 
        screen.blit (winner_quete_img,(0,0))
        quit_quetes.draw(screen)
        show_setting = False
        show_shop = False
        show_quetes = False
        show_boss = False
        show_quete1 = False
        show_quete2 = False

    clock.tick(144) #fps/clock
    
    # Mettre à jour l'affichage
    pygame.display.update()

pygame.quit()


# Moquet Titouan ~ Devallan Flavien 
# TD NSI                  
# 2024~2025



