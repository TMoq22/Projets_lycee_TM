import pygame
from pygame.locals import *
from random import randint
# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| # 

# /!\ ATTENTION CECI N'EST PAS LE PROGRAMME PRINCIPAL /!\                      #
# /!\ OUVRIR PYFIGHT_LEGENDS.py POUR JOUER /!\                                 #
# Lire 'READ_ME.txt' pour plus d'informations                                  #

# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

class Personnage : 
    """ une classe pour pour le personnage  """
    def __init__(self, nom, force, rapidite, sprites,screen,argent,potion,livre,potion2,pv,level,vitesse) :
        self.nom = nom
        self.force = force
        self.rapidite = rapidite
        self.sprites = []
        self.argent = argent
        for sprite in sprites :
            self.sprites.append(pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), (155, 215)))
            
        self.rect = self.sprites[0].get_rect()
        self.rect.center = screen.get_rect().center
        self.rotation = 0
        self.potion = potion
        self.potion2 = potion2
        self.livre = livre
        self.pv = pv
        self.level = level
        self.vitesse = vitesse

    def update_sprites(self,sprites): # actualisation des images du personnage 
        self.sprites = []
        for sprite in sprites :
            self.sprites.append(pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), (155, 215))) 

    # affichage du personnage 
    def affiche(self, screen) : 
        screen.blit(self.sprites[self.rotation], (450,200))
        
    def afficheV2(self,screen,x,y): 
        self.rect.topleft = (x, y) 
        screen.blit(self.sprites[self.rotation], (x,y))
    #  - -- - - - -     
        
    def collision(self, other) : # collision entre un objet et le joueur 
        return self.rect.colliderect(other)
               
    def update_rect(self, x, y):# Mise à jour la position du rect
        self.rect.topleft = (x, y)
        
    # mouvement du "personnage" ( c'est la map qui est déplacée)    
    def mouvement(self,fond_x,fond_y,touche_left,touche_right,touche_up,touche_down):
        dicKeys = pygame.key.get_pressed()
        if dicKeys[touche_left] :
            if fond_x < 0:
                fond_x += self.vitesse
                self.rotation = 1 
        if dicKeys[touche_right] :
            if fond_x > -2500:   
                fond_x -= self.vitesse
                self.rotation = 0
        if dicKeys[touche_up] :
            if fond_y < -490:  
                fond_y += self.vitesse           
                self.rotation = 3
        if dicKeys[touche_down] :
            if fond_y > -2010:  
                fond_y -= self.vitesse
                self.rotation = 2  
        return fond_x,fond_y
   
# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #   
   
class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = 100

    def draw(self, surface): #affichage 
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))
   
   
class ImageButton: 
    def __init__(self, image_path, x, y, width=None, height=None):
        self.original_image = pygame.image.load(image_path) 
        if width and height:
            self.image = pygame.transform.scale(self.original_image, (width, height))
        else:
            self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen): #affichage
        screen.blit(self.image, self.rect)

    def is_clicked(self, event): # detection d'un click sur le rectangle du bouton 
        if self.rect.collidepoint(event.pos):  
            return True
        return False
    
    def update_img_button(self,img,width,height): # actualistation de l'image du bouton 
        for image in img :
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (width,height))
            
        
    
# |/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\||/\| #

class Quêtes:
    def __init__(self, image,difficulte,personnage,mob,image_perso ,image_mob):
        # definition des variables local 
        self.original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original_image, (1000, 650))
        self.rect = self.image.get_rect(center=(500, 320))
        self.difficulte = difficulte
        self.button_fight = ImageButton(r"assets\force.png", 60, 20, 60, 60)
        self.button_potion = ImageButton(r"assets\popo1.png", 190, 20, 50, 50)
        self.button_livre = ImageButton(r"assets\book1.png", 300, 25, 50, 50)
        self.game_over_img = pygame.image.load(r"assets\game_over.jpg")
        self.game_over_img = pygame.transform.scale(self.game_over_img, (1000, 600))
        
        self.valeur_debug = 0
        #perso / mob
        self.personnage = personnage
        self.perso_actif = True
        self.mob = mob
        # barre de vie 
        self.health_bar = HealthBar(40,550, 400, 30, 100)
        self.mob.health_bar = HealthBar(560,550, 400, 30, 100)
        
        # image perso
        self.perso = pygame.image.load(image_perso).convert_alpha()
        self.perso = pygame.transform.scale(self.perso,(155,235))
        self.perso_rect = self.perso.get_rect(center=(0,0))
        
        # image mob
        self.mobs = pygame.image.load(image_mob).convert_alpha()
        self.mobs = pygame.transform.scale(self.mobs,(155,235))
        self.mobs_rect = self.mobs.get_rect(center=(0,0))
        
        #n ombre livre /potion
        self.nb_livre = self.personnage.livre
        self.nb_potion = self.personnage.potion
        # musique + bruitages 
        pygame.mixer.init()
        self.son_popo = pygame.mixer.Sound(r"assets\sfx_popo.ogg")
        self.son_popo.set_volume(0.8)
        self.son_book = pygame.mixer.Sound(r"assets\sfx_book.ogg")
        self.son_book.set_volume(0.9)
        self.son_swoosh = pygame.mixer.Sound(r"assets\sfx_swoosh.ogg")
        self.son_swoosh.set_volume(0.9)
        
        self.livre_use = 0

        self.valeur_attaque = 0
        self.quitter = False
    
    def update_image_perso(self,img): #actualisation de l'image du joueur (si le skin du joueur est changé)
        for image in img :
            self.perso = pygame.image.load(image).convert_alpha()
            self.perso = pygame.transform.scale(self.perso,(155,235))
    
    def game(self,screen,event):  # jeu 
        if self.difficulte == 1 :
            self.valeur_attaque = randint(2, 8)
        if self.difficulte == 2 :
            self.valeur_attaque = randint(4, 10)
        if self.difficulte == 3 :
            self.valeur_attaque = randint(6, 12)
        
        self.nb_livre = self.personnage.livre
        self.nb_potion = self.personnage.potion
        
        #systeme de tour par tour le joueur commence et ne peut pas attaquer tant que le mob n'a pas attaqué
        if self.perso_actif :
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_fight.is_clicked(event): # bouton d'attaque 
                    self.valeur_debug += 1
                    self.mob.health_bar.hp -=randint(1, 8) +(2*self.livre_use) 
                    self.perso_actif = False
                    self.son_swoosh.play()
 
                if self.health_bar.hp <= 90 :# bouton des potions 
                    if self.button_potion.is_clicked(event) :
                        if self.nb_potion > 0:
                            self.son_popo.play()
                            self.nb_potion -= 1
                            self.health_bar.hp += 12
                           
                            self.perso_actif = False
     
                if self.button_livre.is_clicked(event) :# bouton des livres 
                    if self.nb_livre > 0:
                        self.son_book.play()
                        self.nb_livre -= 1
                        self.livre_use +=1 
                        self.perso_actif = False
                        
        else : # attaque du mob
            self.health_bar.hp -=  self.valeur_attaque
            pygame.time.wait(200) 
            self.perso_actif = True
   
   
   
        #|/\||/\| AFFICHAGE |/\||/\|#
        
        font = pygame.font.Font(None, 48)
        self.nb_livre_txt = font.render(f"{self.nb_livre}",1,(255,255,255))
        self.nb_potion_txt = font.render(f"{self.nb_potion}",1,(255,255,255))
        self.perso_actif_txt = font.render("A Vous !",1,(255,255,255))
        self.mob_actif_txt = font.render("le mob attaque ",1,(255,255,255))
        self.vie_mob_txt = font.render(f"{self.mob.health_bar.hp}",1,(255,255,255))
        self.vie_perso_txt = font.render(f"{self.health_bar.hp}",1,(255,255,255))
        
        
        screen.blit(self.image, self.rect)
        self.button_fight.draw(screen)
        
        self.health_bar.draw(screen)
        screen.blit(self.perso,(100,310))
        screen.blit(self.mobs,(700,295))
        self.button_potion.draw(screen)
        self.mob.health_bar.draw(screen)
        self.button_livre.draw(screen)
        screen.blit(self.nb_potion_txt,(228,65))
        screen.blit(self.nb_livre_txt,(335,65))
        # affichage pour savoir à qui est le tour
        if self.perso_actif is True :
            screen.blit(self.perso_actif_txt,( 660,50))
        if self.perso_actif is False  :
            screen.blit(self.mob_actif_txt,( 660,50))
        
        #affichage des pv 
        screen.blit(self.vie_mob_txt,(750,550)) 
        screen.blit(self.vie_perso_txt,(210,550))

            
             
            
        
             
        
             
            
       
       
           
    
    


    
    
    
    
  
  
  
  
  
  
        
        


    