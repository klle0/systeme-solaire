import pygame
import math
import random
import sys
from datetime import datetime, timedelta
import time

# Initialisation de Pygame
pygame.init()

# Fenêtre du jeu
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

vitesse_factor = 1.0 

# Récupére les dimensions de la fenêtre pour mettre la page en plein écran
width_window, height_window = pygame.display.get_surface().get_size()

global FPS
FPS = 120  # Valeur par défaut
clock = pygame.time.Clock()

pause = False
# couleur
YELLOW = (255, 255, 0)
BLUE = (0, 25, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
BROWN = (165, 42, 42)
RED = (255, 0, 0)
GREY = (200, 200, 200)
DARKGREY = (50, 50, 50)
ORANGE = (255, 128, 0)
WHITE = (255,255,255)

#image des signes
signeastro = {
    'Capricorne': 'capricorne.png',
    'Verseau': 'verseau.png',
    'Poissons': 'poisson.png',
    'Bélier': 'belier.png',
    'Taureau': 'taureau.png',
    'Gémeaux': 'gemeaux.png',
    'Cancer': 'cancer.png',
    'Lion': 'lion.png',
    'Vierge': 'vierge.png',
    'Balance': 'balance.png',
    'Scorpion': 'scorpion.png',
    'Sagittaire': 'sagittaire.png'
}


# Charger une image pour une planète
texture_planete_soleil = pygame.image.load("sun.jpg")
texture_planete_mercure = pygame.image.load("mercury.jpg")
texture_planete_venus = pygame.image.load("venus.jpg")
texture_planete_terre = pygame.image.load("terre.jpg")
texture_planete_mars = pygame.image.load("mars.jpg")
texture_planete_jupiter = pygame.image.load("jupiter.jpg")
texture_planete_saturne = pygame.image.load("saturn.jpg")
texture_planete_uranus = pygame.image.load("uranus.jpg")
texture_planete_neptune = pygame.image.load("neptune.jpg")



global axe_visible
axe_visible=True

#image des phases de la lune

tailleimg = (280,280)

image_lune = [
    pygame.transform.scale(pygame.image.load("nouvelleLune.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("premierCroissant.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("premierQuartier.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("gibbeuseCroissante.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("pleineLune.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("gibbeuseDecroissante.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("dernierQuartier.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("dernierCroissant.png"), tailleimg)
]

#liste des musiques 
liste_musiques = [
    "DayOne.mp3",
    "CornfieldChase.mp3",
    "WhereWereGoing.mp3",
    "NoTimeForCaution.mp3"
]

index_musique = 0

vitesse_tps = 86400

date_reference = datetime(1900, 1, 1)

# images pour les boutons
tailleimage = (70,70)
image_lire = pygame.transform.scale(pygame.image.load("lire.png"), tailleimage)  # triangle de lecture
image_pause = pygame.transform.scale(pygame.image.load("pause.png"), tailleimage)  # deux barres pour arrêter
image_prec = pygame.transform.scale(pygame.image.load("prec.png"), tailleimage)
image_suiv = pygame.transform.scale(pygame.image.load("suiv.png"), tailleimage)



# Détermine les coordonnées du centre de la page par rapport a l'ecran
centre_x = width_window // 2
centre_y = height_window // 2


background_image = pygame.image.load("stars.jpg")
background_image = pygame.transform.scale(background_image, (width_window, height_window))


def scale_value(value, screen_width):
    return int(value * (screen_width / 1920))  # largeur de référence



class Bouton:
    # dessiner un bouton
    def __init__(self, x, y, largeur, hauteur, texte, action=None):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.action = action
        self.font = pygame.font.SysFont(None, 36)

    def dessiner_bouton(surface, txt, rect, couleur):
        pygame.draw.rect(surface, couleur, rect)
        font = pygame.font.SysFont("Times New Roman", 25)
        surface_texte = font.render(txt, True, BLACK)
        rectangle_txt = surface_texte.get_rect(center=rect.center)
        #coodonées et dimensions du rectangle du txt + centrer txt 
        surface.blit(surface_texte, rectangle_txt)
        #dessine une surface

    def dessiner(self, surface):
        couleur=ORANGE
        pygame.draw.rect(surface, couleur, self.rect)
        surface_texte = self.font.render(self.texte, True, BLACK)
        rect_texte = surface_texte.get_rect(center=self.rect.center)
        surface.blit(surface_texte, rect_texte)

    def click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            print(f"Bouton cliqué : {self.texte}")
            self.action()
        
class Bouton_eruption:
    #classe bouton pour les eruptions
    def __init__(self, x, y, w, h, couleur, texte):
        self.rect = pygame.Rect(x, y, w, h)
        self.couleur = couleur
        self.texte = texte
        self.font = pygame.font.SysFont("Times New Roman", 25)
        
    def dessiner(self, surface):
        pygame.draw.rect(surface, self.couleur, self.rect)
        surface_texte = self.font.render(self.texte, True, BLACK)
        rect_texte = surface_texte.get_rect(center=self.rect.center)
        surface.blit(surface_texte, rect_texte)
        
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)
        
        
# classe bouton pr la musique
class BoutonMusique:
    def __init__(self, x, y, image_lire, image_pause):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image_lire = image_lire
        self.image_pause = image_pause
        self.en_pause = True  # Démarre en état de pause

    def dessiner(self, surface):
        if self.en_pause:
            surface.blit(self.image_lire, self.rect.topleft)
        else:
            surface.blit(self.image_pause, self.rect.topleft)

    def est_clique(self, pos):
        return self.rect.collidepoint(pos)

class Asteroide:
    # Attribut pour stocker les informations des astéroïdes
    asteroides = []
    angle_rotation = 0  # Angle global de rotation de la ceinture
    
    def __init__(self, nombre_asteroides, distances_ceintures):
        Asteroide.asteroides = [
            {'angle_initial': random.uniform(0, 2 * math.pi), 'distance': random.choice(distances_ceintures)}
            for _ in range(nombre_asteroides)
        ]
    
    def dessiner_ceinture_asteroides(self, surface, centre_soleil, vitesse_rotation_ceinture, pause, zoom):

        if not pause:
            Asteroide.angle_rotation += vitesse_rotation_ceinture
        
        # Récupérer la position de la souris
        souris_x, souris_y = pygame.mouse.get_pos()
    
        # Dessiner chaque astéroïde
        for asteroide in Asteroide.asteroides:
            angle_total = asteroide['angle_initial'] + Asteroide.angle_rotation
            distance = asteroide['distance']
            
            # Calculer la position X et Y de chaque astéroïde
            x = centre_soleil[0] + distance * math.cos(angle_total) * zoom
            y = centre_soleil[1] + distance * math.sin(angle_total) * zoom
            
            # Dessiner l'astéroïde
            pygame.draw.circle(surface, (169, 169, 169), (int(x), int(y)), 2)
            
            # Vérifier si la souris est proche de cet astéroïde
            distance_souris_asteroide = math.hypot(souris_x - x, souris_y - y)
            if distance_souris_asteroide < 10:  # Seuil de survol
                # Afficher un pop-up près de la souris
                font = pygame.font.SysFont(None, 24)
                text = font.render("Astéroïde", True, (255, 255, 255))
                surface.blit(text, (souris_x + 10, souris_y + 10))


class Meteorite:
    def __init__(self):
        self.x = random.randint(0, width_window)
        self.y = 0
        self.vitesse_y = random.uniform(5, 10)  # vitesse verticale
        self.vitesse_x = random.uniform(-5, 5)   # vitesse horizontale
        self.taille = random.randint(4, 7)

    def mouvement(self):
        # faaire descendre la meteorite
        self.y += self.vitesse_y
        self.x += self.vitesse_x

    def dessiner(self, surface):
        # Dessine la météorite
        pygame.draw.circle(surface, GREY, (self.x, int(self.y)), self.taille)

# date de reference pr calculer l'angle initial
def calculerAngle(periode_orbitale, date_reference):
    # nb d'annees depuis la date de reference
    date = datetime.now()
    annees_ecoulees = (date - date_reference).days / 365.26 
    #radians
    return (2 * math.pi * annees_ecoulees / periode_orbitale) % (2 * math.pi)

import pygame
import math

class Planet:
    global vitesse_factor
    def __init__(self, nom, color, rayon_x, rayon_y, speed, size, angle_rotation, diametre, population, info="", periode_orbitale=1, texture_path=None,):
        self.nom = nom
        self.color = color
        self.rayon_x = rayon_x
        self.rayon_y = rayon_y
        self.speed = speed
        self.size = size
        self.angle_rotation = angle_rotation
        self.diametre = diametre  
        self.population = population
        self.info = info.split("|")  # Retours à la ligne
        self.periode_orbitale = periode_orbitale
        self.angle = calculerAngle(periode_orbitale, date_reference)
        
        if texture_path:  # Si un chemin de texture est donné, charge l'image
            self.texture = pygame.image.load(texture_path)
            self.resize_texture()
        else:
            self.texture = None  # Pas de texture si non définie

    def resize_texture(self):
        # Redimensionner la texture selon la taille de la planète
        texture_size = int(self.size * 2)  # On suppose que la taille de la planète est deux fois le rayon
        self.texture_resized = pygame.transform.scale(self.texture, (texture_size, texture_size))

    def mouvP(self, en_pause, vitesse_factor):
        # Déplacement des planètes si pas en pause
        if not en_pause:
            self.x = centre_x + self.rayon_x * math.cos(self.angle)
            self.y = centre_y + self.rayon_y * math.sin(self.angle)
            self.angle += self.speed * vitesse_factor

    def drawP(self, surface):

        #Afficher les axes de rotation
        longueure_axe = self.size*2 + 10
        start_x = self.x - (longueure_axe / 2) * math.cos(self.angle_rotation)
        start_y = self.y - (longueure_axe / 2) * math.sin(self.angle_rotation)
        end_x = self.x + (longueure_axe / 2) * math.cos(self.angle_rotation)
        end_y = self.y + (longueure_axe / 2) * math.sin(self.angle_rotation)
        if axe_visible==True:
            pygame.draw.line(surface, GREY, (start_x, start_y), (end_x, end_y), 2)
        """Dessine la planète avec une texture ronde et un masque circulaire."""
        if hasattr(self, 'texture_resized'):
            # Taille de la texture
            taille_texture = self.size * 2

            # Surface temporaire pour créer la texture masquée
            texture_circulaire = pygame.Surface((taille_texture, taille_texture), pygame.SRCALPHA)
            texture_circulaire.blit(self.texture_resized, (0, 0))  # Dessine la texture redimensionnée

            # Création d'un masque circulaire
            masque = pygame.Surface((taille_texture, taille_texture), pygame.SRCALPHA)
            pygame.draw.circle(masque, (255, 255, 255), (taille_texture // 2, taille_texture // 2), self.size)

            # Application du masque circulaire
            texture_circulaire.blit(masque, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # Affichage de la texture ronde sur la surface principale
            rect = texture_circulaire.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(texture_circulaire, rect)



    def survole(self, pos_souris):
        distance = math.hypot(pos_souris[0] - self.x, pos_souris[1] - self.y)
        return distance <= self.size

    def afficher_info(self, surface, pos_souris):
        font = pygame.font.SysFont("Times New Roman", 20)
        padding = 10  # Espacement entre le texte et les bords du pop-up
        
        # Contenu des informations avec le diamètre et la population
        info_lines = [
            f"Nom: {self.nom}",
            f"Diamètre: {self.diametre} km",
            f"Population: {self.population}",
        ] + self.info  # On ajoute les autres infos
        
        # Calcul de la largeur et hauteur du rectangle en fonction du contenu
        max_line_width = max(font.size(line)[0] for line in info_lines) + 2 * padding + 20
        line_height = font.get_height()
        rect_height = line_height * len(info_lines) + 2 * padding
        rect_x, rect_y = pos_souris[0] + 10, pos_souris[1] + 10

        # Dessiner le fond du pop-up
        pygame.draw.rect(surface, WHITE, (rect_x, rect_y, max_line_width, rect_height))
        pygame.draw.rect(surface, BLACK, (rect_x, rect_y, max_line_width, rect_height), 2)  # Bordure noire

        # Afficher chaque ligne de texte avec un point en début
        for i, line in enumerate(info_lines):
            texte = font.render(f"• {line}", True, BLACK)
            surface.blit(texte, (rect_x + padding, rect_y + padding + i * line_height))

# Classe Satellite 
class Satellite:
    global vitesse_factor
    def __init__(self, nom, color, rayon_x, rayon_y, speed, size, planet_parent, diametre, population, info="", periode_orbitale=1):
        self.nom = nom
        self.color = color
        self.rayon_x = rayon_x
        self.rayon_y = rayon_y
        self.speed = speed
        self.size = size
        self.planet_parent = planet_parent
        self.diametre = diametre  # Ajout du diamètre
        self.population = population  # Ajout de la population
        self.info = info.split("|")
        
        self.periode_orbitale = periode_orbitale
        self.angle = calculerAngle(periode_orbitale, date_reference)

    def mouvS(self,en_pause, vitesse_factor):
        
        #mouvement des sattelites si pas en pause
        if not en_pause:
            self.x = self.planet_parent.x + self.rayon_x * math.cos(self.angle)
            self.y = self.planet_parent.y + self.rayon_y * math.sin(self.angle)
            self.angle += self.speed * vitesse_factor

    def drawS(self, surface):
        #affiche les satellittes
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

    def survole(self, pos_souris):
        distance = math.hypot(pos_souris[0] - self.x, pos_souris[1] - self.y)
        return distance <= self.size
    
    def afficher_info(self, surface, pos_souris):
        font = pygame.font.SysFont("Times New Roman", 20)
        padding = 30  # Espacement entre le texte et les bords du pop-up
        
        # Contenu des informations avec le diamètre et la population
        info_lines = [
            f"Nom: {self.nom}",
            f"Diamètre: {self.diametre} km",
            f"Population: {self.population}",
        ] + self.info
        
        # Contenu des informations avec le diamètre et la population
        info_lines = [
            f"Nom: {self.nom}",
            f"Diamètre: {self.diametre} km",
            f"Population: {self.population}",
        ] + self.info  # On ajoute les autres infos

        # Calcul de la largeur et hauteur du rectangle en fonction du contenu
        max_line_width = max(font.size(line)[0] for line in info_lines) + 2 * padding
        line_height = font.get_height()
        rect_height = line_height * len(info_lines) + 2 * padding
        rect_x, rect_y = pos_souris[0] + 10, pos_souris[1] + 10

        # Dessiner le fond du pop-up
        pygame.draw.rect(surface, WHITE, (rect_x, rect_y, max_line_width, rect_height))
        pygame.draw.rect(surface, BLACK, (rect_x, rect_y, max_line_width, rect_height), 2)  # Bordure noire

        # Afficher chaque ligne de texte avec un point en début
        for i, line in enumerate(info_lines):
            texte = font.render(f"• {line}", True, BLACK)
            surface.blit(texte, (rect_x + padding, rect_y + padding + i * line_height))

#calsse eruptiobn solaire
class eruptionSolaire:
    def __init__(self):
        # postiton aléatoire autour du soleil
        self.angle = random.uniform(0, 2 * math.pi) #en randiant
        self.distance = 90  # distance p/r au centre du soleil
        self.vitesse = random.uniform(1, 4)  # vitesse d'extension de l'éruption
        self.taille = random.randint(2, 4)  # taille de l'eruption
        self.opacite = 255  # niveau de transparence au depart
    
    def mouvement(self):
        # eruption qui s'éloigne du soleil
        self.distance += self.vitesse - 3*(self.vitesse/4)
        # reduction de l'opacite
        self.opacite = max(0, self.opacite - 5)
        
    def draw(self, surface):
        # coordonnées euption
        x = centre_x + self.distance * math.cos(self.angle)
        y = centre_y + self.distance * math.sin(self.angle)
        # dessine cercle
        surface_eruption = pygame.Surface((self.taille * 2, self.taille * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface_eruption, (255, 69, 0, self.opacite), (self.taille, self.taille), self.taille)
        surface.blit(surface_eruption, (x - self.taille, y - self.taille))




# Classe Système Solaire
class SystemeSolaire:
    def __init__(self,background):
        self.planets = []
        self.satellites = []
        self.eruptions = []  # lsite eruptions solaires
        self.meteorites = []
        self.date = datetime(1900, 1, 1)  # date simulation initiale
        self.avancer_date = True
        self.score = 0
        # Charger l'image de fond
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background, (width_window, height_window))

    def add_planet(self, planet):
        self.planets.append(planet)

    def add_satellite(self, satellite):
        self.satellites.append(satellite)
        
    def ajoutermeteorite(self):
        self.meteorites.append(Meteorite())
        
    def add_eruption(self):
        self.eruptions.append(eruptionSolaire())
        
    def maj_date(self, nouvelle_date):
        self.date = nouvelle_date
        self.avancer_date = False
        
    def mouvement(self, en_pause):
        #mouvement si ce n'est pas en pause
        
                
        #avancer date simulation
        if not en_pause and self.avancer_date:
            self.date += timedelta(1)
            
        for planet in self.planets:
            planet.mouvP(en_pause, vitesse_factor)
        for satellite in self.satellites:
            satellite.mouvS(en_pause, vitesse_factor)
            
        for eruption in self.eruptions:
            eruption.mouvement()
            
        for meteorite in self.meteorites:
            meteorite.mouvement()
            
        for planet in self.planets:
            planet.angle = calculerAngle(planet.periode_orbitale, self.date)

    def draw(self, surface,eruption_visible):
        surface.blit(self.background, (0, 0))
        for meteorite in self.meteorites:
            meteorite.dessiner(surface)
            
        # dessine eruptions solaires si visible
        if eruption_visible:
            for eruption in self.eruptions:
                eruption.draw(surface)
        
        # Dessiner le Soleil
        pygame.draw.circle(surface, YELLOW, (centre_x, centre_y), 90)
        # Dessiner les planètes et les satellites
        for planet in self.planets:
            planet.drawP(surface)
        for satellite in self.satellites:
            satellite.drawS(surface)
            
        
        # enelver eruptions terminees
        eruptions_a_garder = []
        for eruption in self.eruptions:
            if eruption.opacite > 0:
                eruptions_a_garder.append(eruption)
                
    def enlevermeteorite(self, clique_position):
        # enelve meteorites qui sortent de l'ecran
        self.meteorites = [m for m in self.meteorites if m.y < height_window and m.x < width_window and not self.clique_sur_meteorite(m, clique_position)]
    
    def clique_sur_meteorite(self, meteorite, clic_position):
        if clic_position is None:
            return False 
        clic_x, clic_y = clic_position
        distance = ((meteorite.x - clic_x) ** 2 + (meteorite.y - clic_y) ** 2) ** 0.5 # distance meteorite et clic(**O.5=racine carré)
         #si la distance est inferieure au rayon de la métééorite, alors vrai
        if distance <= meteorite.taille:
            self.score+=1
            return True
        else:
            return False

#classe lune
class Lune:
    def det_phase_lune(angle_lune):
        #determine la phase de lune a afficher
        nb_de_phase = len(image_lune) #nb de phase
        phase = int((angle_lune % (2 * math.pi)) / (2 * math.pi / nb_de_phase))
        #reparti les angles sur les differentes phases
        
        return phase

    def dessiner_lune(visible, phase):
        # Affichage des phases de la lune
        if visible:
            # Définir une taille maximum pour la fenêtre de la lune
            max_width = width_window - 100  # Laisser une marge de 50 pixels de chaque côté
            max_height = height_window - 100  # Laisser une marge de 50 pixels en haut et en bas

            # Fixer la taille de la fenêtre de la lune
            rect_width = min(300, max_width)
            rect_height = min(300, max_height)

            # Positionner la fenêtre
            pos_x = width_window - rect_width - 20  # Décalage de 20 pixels du bord droit
            pos_y = 50  # Garder la position Y

            pygame.draw.rect(window, WHITE, pygame.Rect(pos_x, pos_y, rect_width, rect_height))
            # Affiche l'image de la phase, centrée dans la fenêtre
            window.blit(image_lune[phase], (pos_x + 10, pos_y + 10))  # Ajuster la position de l'image


# Fonction principale
def main():
    global vitesse_factor
    global axe_visible
    global FPS
    # Récupérer la largeur de la fenêtre
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Créer le système solaire
    systeme_solaire = SystemeSolaire("stars.jpg")
    asteroide_instance = Asteroide(200,[300,315])

    #taille du soleil
      #taille du soleil
    size_sun = scale_value(100, screen_width)  # Taille du soleil à l'échelle
    soleil = Planet("Soleil", YELLOW, scale_value(0, screen_width), scale_value(0, screen_width), 0, size_sun,0, 1392000, "0", "État: Gazeux | Temp: 5778 K | Pression au centre: 2,5 × 10^16 Pa | Diamètre: 1 391 000 km | Masse: 1,989 × 10^30 kg | Luminosité: 3,846 × 10^26 W", 
    1,"sun.jpg")
    systeme_solaire.add_planet(soleil)
    
    

    #ajouter des palente
    mercure = Planet("Mercure", GREY, scale_value(size_sun +140, screen_width), scale_value(130, screen_width), 0.047, scale_value(4, screen_width), 0, 4879, "0", "Eau: 0% | Pression: ~0 atm | Temp: -173 à 427°C | Diamètre: 4 879 km | Masse: 3,301 × 10^23 kg", 
    0.241,"mercury.jpg")
    terre = Planet("Terre", BLUE, scale_value(size_sun + 220, screen_width), scale_value(180, screen_width), 0.029, scale_value(10, screen_width),  math.radians(23.5), 12742, "8,1 milliards", "Eau: 71% | Pression: 1 atm | Temp: -88 à 58°C | Diamètre: 12 742 km | Masse: 5,972 × 10^24 kg", 
    1,"terre.jpg")
    venus = Planet("Vénus", ORANGE, scale_value(size_sun + 195, screen_width), scale_value(180, screen_width), 0.035, scale_value(9, screen_width), math.radians(177.4), 12104, "0", "Eau: 0% | Pression: 92 atm | Temp: 462°C | Diamètre: 12 104 km | Masse: 4,867 × 10^24 kg", 
    0.615,"venus.jpg")
    mars = Planet("Mars", RED, scale_value(size_sun + 300, screen_width), scale_value(240, screen_width), 0.024, scale_value(5, screen_width),  math.radians(25.2), 6779, "0", "Eau: Traces | Pression: 0.006 atm | Temp: -125 à 20°C | Diamètre: 6 779 km | Masse: 6,417 × 10^23 kg", 
    1.881,"mars.jpg")
    systeme_solaire.add_planet(terre)
    systeme_solaire.add_planet(mercure)
    systeme_solaire.add_planet(venus)
    systeme_solaire.add_planet(mars)

    jupiter = Planet("Jupiter", (255, 165, 0), scale_value(450, screen_width), scale_value(300, screen_width), 0.013, scale_value(15, screen_width),  math.radians(3.13), 139820, "0",  "État: Gazeux | Eau: Traces | Temp: -108°C | Diamètre: 139 820 km | Masse: 1,898 × 10^27 kg", 
    11.86,"jupiter.jpg")
    satellite_jupiter1 = Satellite("Io", BROWN, scale_value(50, screen_width), scale_value(30, screen_width), 0.04, scale_value(4, screen_width), jupiter, 3642, "0",  "État: Solide | Eau: Traces | Temp: -143°C | Diamètre: 3 642 km | Masse: 8,93 × 10^22 kg", 
    1.8)
    satellite_jupiter2 = Satellite("Europa", CYAN, scale_value(60, screen_width), scale_value(40, screen_width), 0.03, scale_value(5, screen_width), jupiter, 3121, "0", "État: Solide | Eau: Traces | Océans sous la surface | Temp: -160°C | Diamètre: 3 121 km | Masse: 4,80 × 10^22 kg", 
    3.5)
    satellite_jupiter3 = Satellite("Ganymède", GREY, scale_value(70, screen_width), scale_value(50, screen_width), 0.025, scale_value(6, screen_width), jupiter, 5262, "0", "État: Solide | Eau: Traces | Temp: -163°C | Diamètre: 5 262 km | Masse: 1,48 × 10^23 kg", 
    7.15)
    satellite_jupiter4 = Satellite("Callisto", (200, 200, 200), scale_value(80, screen_width), scale_value(60, screen_width), 0.02, scale_value(6, screen_width), jupiter, 4820, "0", "État: Solide | Eau: Traces | Temp: -139°C | Diamètre: 4 820 km | Masse: 1,08 × 10^23 kg", 
    16.7)
    systeme_solaire.add_planet(jupiter)
    systeme_solaire.add_satellite(satellite_jupiter1)
    systeme_solaire.add_satellite(satellite_jupiter2)
    systeme_solaire.add_satellite(satellite_jupiter3)
    systeme_solaire.add_satellite(satellite_jupiter4)

        #dessiner les anneaux de Saturne
    def dessiner_anneaux_saturne(surface, saturne):
        anneaux_largeur = [scale_value(20 * zoom_factor, width_window), scale_value(40 * zoom_factor, width_window), scale_value(60 * zoom_factor, width_window)]
        anneaux_couleurs = [(210, 180, 140), (192, 192, 192), (169, 169, 169)]  # Couleurs des anneaux

        for largeur, couleur in zip(anneaux_largeur, anneaux_couleurs):
            pygame.draw.ellipse(
                surface, couleur,
                pygame.Rect(
                    saturne.x* zoom_factor - largeur // 2,  # Décalage en fonction de la taille des anneaux
                    saturne.y* zoom_factor - largeur // 4,  # Ajustement en hauteur pour l'effet ellipse
                    largeur,
                    largeur // 2),1)# Épaisseur de l'anneau
            
    saturne = Planet("Saturne", (255, 215, 0), scale_value(600, screen_width), scale_value(350, screen_width), 0.011, scale_value(12, screen_width), math.radians(26.7), 116460, "0", "État: Gazeux | Eau: Traces | Temp: -178°C | Diamètre: 116 460 km | Masse: 5,683 × 10^26 kg", 
    29.46,"saturn.jpg")
    satellite_saturne1 = Satellite("Titan", (255, 165, 0), scale_value(70, screen_width), scale_value(40, screen_width), 0.035, scale_value(6, screen_width), saturne, 5150, "0", "État: Solide | Eau: Lacs de méthane | Temp: -179°C | Diamètre: 5 150 km | Masse: 1,345 × 10^23 kg", 
    15.9)
    satellite_saturne2 = Satellite("Rhea", (169, 169, 169), scale_value(80, screen_width), scale_value(50, screen_width), 0.02, scale_value(5, screen_width), saturne, 1528, "0", "État: Solide | Eau: Traces | Temp: -174°C | Diamètre: 1 528 km | Masse: 2,3 × 10^21 kg", 
    4.5)
    systeme_solaire.add_planet(saturne)
    systeme_solaire.add_satellite(satellite_saturne1)
    systeme_solaire.add_satellite(satellite_saturne2)

    uranus = Planet("Uranus", (173, 216, 230), scale_value(800, screen_width), scale_value(400, screen_width), 0.008, scale_value(10, screen_width), math.radians(97.8), 50724, "0",  "État: Gazeux | Eau: Traces | Temp: -224°C | Diamètre: 50 724 km | Masse: 8,681 × 10^25 kg", 
    84.01,"uranus.jpg")
    satellite_uranus1 = Satellite("Titania", (210, 180, 140), scale_value(50, screen_width), scale_value(30, screen_width), 0.03, scale_value(4, screen_width), uranus, 1577, "0", "État: Solide | Eau: Traces | Temp: -224°C | Diamètre: 1 577 km | Masse: 3,53 × 10^21 kg", 
    8.7)
    satellite_uranus2 = Satellite("Oberon", (200, 200, 200), scale_value(60, screen_width), scale_value(40, screen_width), 0.02, scale_value(4, screen_width), uranus, 1523, "0", "État: Solide | Eau: Traces | Temp: -224°C | Diamètre: 1 523 km | Masse: 3,00 × 10^21 kg", 
    13.5)
    systeme_solaire.add_planet(uranus)
    systeme_solaire.add_satellite(satellite_uranus1)
    systeme_solaire.add_satellite(satellite_uranus2)

    neptune = Planet("Neptune", (30, 144, 255), scale_value(900, screen_width), scale_value(500, screen_width), 0.007, scale_value(9, screen_width), math.radians(28.3), 49244, "0", "État: Gazeux | Eau: Traces | Temp: -214°C | Diamètre: 49 244 km | Masse: 1,024 × 10^26 kg", 
    164.8,"neptune.jpg")
    satellite_neptune1 = Satellite("Triton", (200, 200, 200), scale_value(50, screen_width), scale_value(30, screen_width), 0.03, scale_value(5, screen_width), neptune, 2706, "0", "État: Solide | Eau: Traces | Temp: -235°C | Diamètre: 2 706 km | Masse: 2,14 × 10^22 kg", 
    5.8)
    systeme_solaire.add_planet(neptune)
    systeme_solaire.add_satellite(satellite_neptune1)
    

    # ajout des satellites
    lune = Satellite("Lune", GREY, scale_value(30, screen_width), scale_value(22, screen_width), 0.1, scale_value(3, screen_width), terre, 3474, "0", "Eau: Traces | Pression: ~0 atm | Temp: -183 à 106°C | Diamètre: 3 474 km | Masse: 7,347 × 10^22 kg", 
    27.3)
    systeme_solaire.add_satellite(lune)

    systeme_solaire.add_planet(soleil)
    


    
    #controle visibilité de la fenetre de la lune
    fenetre_lune_visible = False
    
    
    
    #pause
    en_pause = False
    date_changee  = False
    premierTour = True
    image_signe = None
    
    # variable pr activer/désactiver les meteorites et les eruptions
    eruption_visible = True
    meteorites_actives = True
    
    
    font = pygame.font.SysFont("Times New Roman", 30)
    case = pygame.Rect(0.04 * screen_width, 0.1 * screen_height, 0.1 * screen_width, 0.04 * screen_height) 
    couleur_inactive = pygame.Color('lightskyblue3')
    couleur_active = pygame.Color('dodgerblue2')
    couleur = couleur_inactive
    active = False
    texte = ''
    
    
    
    # creation des boutons
    # Création des boutons avec des positions proportionnelles
    bouton_ouvrir_fermer = pygame.Rect(screen_width - 0.03 * screen_width, 0.03 * screen_height, 0.02 * screen_width, 0.022 * screen_height)
    bouton_stop = pygame.Rect(0.04 * screen_width, 0.05 * screen_height, 0.1 * screen_width, 0.04 * screen_height)
    boutonEruption = Bouton_eruption(0.04 * screen_width, 0.15 * screen_height, 0.2 * screen_width, 0.05 * screen_height,ORANGE,"eruptions: on")
    boutonMeteorite = Bouton_eruption(0.04 * screen_width, 0.21 * screen_height, 0.2 * screen_width, 0.05 * screen_height,ORANGE,"meteorite: on")
    bouton_zoom = pygame.Rect(0.04 * screen_width, 0.39 * screen_height, 0.125 * screen_width, 0.03 * screen_height)
    bouton_dezoom = pygame.Rect(0.04 * screen_width, 0.35 * screen_height, 0.125 * screen_width, 0.03 * screen_height)
    bouton_recentrer = pygame.Rect(0.04 * screen_width, 0.31 * screen_height, 0.125 * screen_width, 0.03 * screen_height)
    bouton_axe_visible = pygame.Rect(0.04 * screen_width, 0.27 * screen_height, 0.125 * screen_width, 0.03 * screen_height)

    bouton_augmenter_vitesse = pygame.Rect(0.04 * screen_width, 0.02 * screen_height, 0.1 * screen_width, 0.025 * screen_height)
    bouton_diminuer_vitesse = pygame.Rect(0.141 * screen_width, 0.02 * screen_height, 0.1 * screen_width, 0.025 * screen_height)
        #gestion_vitesse.changer_vitesse_planetes(0.05)
    # boutons de contrele musique

        # Position et dimensions du cadre basés sur la taille de l'écran
    CADRE_LARGEUR, CADRE_HAUTEUR = 300, 100  # Taille du cadre
    CADRE_X = width_window - CADRE_LARGEUR - 20  # Position X du cadre, 20 pixels depuis le bord droit
    CADRE_Y = height_window - CADRE_HAUTEUR - 20  # Position Y du cadre, 20 pixels depuis le bas

    TAILLE_BOUTON = 50
    
        # Initialisation des boutons de contrôle musique avec la classe BoutonMusique
    bouton_lire_pause = BoutonMusique(CADRE_X + (CADRE_LARGEUR // 2) - (TAILLE_BOUTON // 2), CADRE_Y + 25, image_lire, image_pause)
    bouton_prec = BoutonMusique(CADRE_X + 30, CADRE_Y + 25, image_prec, image_prec)
    bouton_suiv = BoutonMusique(CADRE_X + CADRE_LARGEUR - 80, CADRE_Y + 25, image_suiv, image_suiv)

    
    global index_musique
    musique_joue = False
    pygame.mixer.music.load(liste_musiques[index_musique])  # chargement premiere musique
    
    
    def saisir_date_input(screen, systeme_solaire):
        input_box = pygame.Rect(0.01 * screen_width, 0.05 * screen_height, 0.1 * screen_width, 0.04 * screen_height)  # Position et taille de la boîte de saisie
        color_inactive = pygame.Color(BLUE)
        color_active = pygame.Color(WHITE)
        color = color_inactive
        active = False
        texte = ''
        font = pygame.font.SysFont("Times New Roman", 30)
        image_signe=None
        
    #definr le signe astro
    def defsigne(date):

        mois = date.month
        jour = date.day

        # Vérifie chaque période de signe astrologique
        if (mois == 3 and jour >= 21) or (mois == 4 and jour <= 19):
            return "Bélier"
        elif (mois == 4 and jour >= 20) or (mois == 5 and jour <= 20):
            return "Taureau"
        elif (mois == 5 and jour >= 21) or (mois == 6 and jour <= 20):
            return "Gémeaux"
        elif (mois == 6 and jour >= 21) or (mois == 7 and jour <= 22):
            return "Cancer"
        elif (mois == 7 and jour >= 23) or (mois == 8 and jour <= 22):
            return "Lion"
        elif (mois == 8 and jour >= 23) or (mois == 9 and jour <= 22):
            return "Vierge"
        elif (mois == 9 and jour >= 23) or (mois == 10 and jour <= 22):
            return "Balance"
        elif (mois == 10 and jour >= 23) or (mois == 11 and jour <= 21):
            return "Scorpion"
        elif (mois == 11 and jour >= 22) or (mois == 12 and jour <= 21):
            return "Sagittaire"
        elif (mois == 12 and jour >= 22) or (mois == 1 and jour <= 19):
            return "Capricorne"
        elif (mois == 1 and jour >= 20) or (mois == 2 and jour <= 18):
            return "Verseau"
        elif (mois == 2 and jour >= 19) or (mois == 3 and jour <= 20):
            return "Poissons"
    # Boucle du jeu
    en_cours = True
    zoom_factor = 1
    decalage_x, decalage_y = 0, 0
    zoom_active = False
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                clic_position = pygame.mouse.get_pos()
                systeme_solaire.enlevermeteorite(clic_position)
                if bouton_ouvrir_fermer.collidepoint(event.pos):  # si bouton cliqué
                    fenetre_lune_visible = not fenetre_lune_visible #afficher ou pas

                if bouton_stop.collidepoint(event.pos):  # pause
                    en_pause = not en_pause
                    
                if boutonMeteorite.est_clique(event.pos):
                    meteorites_actives = not meteorites_actives
                    if meteorites_actives:
                        boutonMeteorite.texte = "météorites: on"
                    else:
                        boutonMeteorite.texte = "météorites: off"
                        
                if boutonEruption.est_clique(event.pos):
                    eruption_visible = not eruption_visible
                    if eruption_visible:
                        boutonEruption.texte = "eruptions: on"
                    else:
                        boutonEruption.texte = "eruptions: off"

                if bouton_lire_pause.est_clique(event.pos):
                    if musique_joue:
                        pygame.mixer.music.pause()
                        bouton_lire_pause.en_pause = True
                    else:
                        pygame.mixer.music.unpause()
                        bouton_lire_pause.en_pause = False
                    musique_joue = not musique_joue
                    
                    if premierTour:
                        if musique_joue: 
                            pygame.mixer.music.play(0)
                            premierTour = False

                    
                if bouton_prec.est_clique(event.pos):
                    index_musique = (index_musique - 1) % len(liste_musiques)
                    pygame.mixer.music.load(liste_musiques[index_musique])
                    if musique_joue:
                        pygame.mixer.music.play(0)

                if bouton_suiv.est_clique(event.pos):
                    index_musique = (index_musique + 1) % len(liste_musiques)
                    pygame.mixer.music.load(liste_musiques[index_musique])
                    if musique_joue:
                        pygame.mixer.music.play(0)

                if case.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if active:
                    couleur = couleur_active
                else:
                    couleur = couleur_inactive

                if bouton_augmenter_vitesse.collidepoint(event.pos):
                    vitesse_factor=min(vitesse_factor * 2, 64)
                    FPS+=10

                if bouton_diminuer_vitesse.collidepoint(event.pos):
                    vitesse_factor=max(vitesse_factor / 2, 0.125)
                    FPS=max(1, FPS - 10)


                if bouton_zoom.collidepoint(event.pos):
                    zoom_factor += 0.4
                    zoom_active = True
                    
                if bouton_dezoom.collidepoint(event.pos) and zoom_factor>0.1:
                    zoom_factor = max(1, zoom_factor - 0.3)
                    if zoom_factor == 1:
                        zoom_active = False

                if bouton_recentrer.collidepoint(event.pos):
                    zoom_factor = 1
                    decalage_x, decalage_y = 0, 0
                    zoom_active = False

                if bouton_axe_visible.collidepoint(event.pos):
                    if axe_visible==True:
                        axe_visible=False
                    else:
                        axe_visible=True
                
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    decalage_x += 20
                if event.key == pygame.K_RIGHT:
                    decalage_x -= 20
                if event.key == pygame.K_UP:
                    decalage_y += 20
                if event.key == pygame.K_DOWN:
                    decalage_y -= 20

                if active:##
                    if event.key == pygame.K_RETURN:
                        parties = texte.split('/')
                        if len(parties) == 3:
                            jour, mois, annee = map(int, parties)

                            # Vérification de la date
                            date_valide = (1 <= mois <= 12 and 1 <= jour <= 31 and annee > 0)
                            if mois in {4, 6, 9, 11} and jour > 30:
                                date_valide = False
                            elif mois == 2:
                                est_bissextile = (annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0))
                                if (est_bissextile and jour > 29) or (not est_bissextile and jour > 28):
                                    date_valide = False
                            if date_valide:
                                # Mise à jour de la date dans le système solaire
                                systeme_solaire.maj_date(datetime(annee, mois, jour, 0, 0, 0))
                                
                                date_changee = True
                                
                                # Calcul du signe astrologique
                                signe = defsigne(datetime(annee, mois, jour))

                                # Charge l'image du signe astrologique
                                image_signe = pygame.image.load(f"{signe}.png")
                                image_signe = pygame.transform.scale(image_signe, (110, 110))  # Redimensionner l'image

                                # Réinitialiser la saisie de texte
                                texte = ''  # Vide le champ de texte
                                active = False  # Désactive l'entrée de texte
                                ##
                            else:
                                print("date invalide. entrer une date au format jour/mois/année.")
                        else:
                            print("format invalide : entrer une date au format jour/mois/année.")
                        
                        texte = ''
                    elif event.key == pygame.K_BACKSPACE:
                        texte = texte[:-1]
                    else:
                        texte += event.unicode
        

        window.blit(background_image, (0,0))

        
        # ajout de meteorites si actives
        if meteorites_actives and random.random() < 0.1:
            systeme_solaire.ajoutermeteorite()
        
        # proba apparition d'une nouvelle eruption
        if random.random() < 0.2:
            systeme_solaire.add_eruption()
            
        # Mise à jour des positions
        surface_solaire = pygame.Surface((width_window, height_window))
        systeme_solaire.mouvement(en_pause)
        systeme_solaire.draw(surface_solaire, eruption_visible)
        systeme_solaire.enlevermeteorite(pygame.mouse.get_pos())
        
        # affice le système solaire
        systeme_solaire.draw(window,eruption_visible)

        # affichage date
        font_date = pygame.font.SysFont("Times New Roman", 30)
        date_texte = font_date.render(systeme_solaire.date.strftime("%d/%m/%Y"), True, WHITE)
        window.blit(date_texte, (100,height_window - 100))

        # Dessiner les anneaux de Saturne après Saturne
        dessiner_anneaux_saturne(window, saturne)

        pos_souris = pygame.mouse.get_pos()
        
        #fenetre de la lune
        phase_actuelle_lune = Lune.det_phase_lune(lune.angle)

        #afficher la surface zoomée
        if zoom_active:
            zoomed_surface = pygame.transform.scale(
                surface_solaire, (int(width_window * zoom_factor), int(height_window * zoom_factor))
            )
            dessiner_anneaux_saturne(zoomed_surface, saturne) 
            window.blit(zoomed_surface, ((width_window - zoomed_surface.get_width()) // 2+ decalage_x,
                                         (height_window - zoomed_surface.get_height()) // 2+ decalage_y))
            
        else:
        # Affiche la vue normale

            window.blit(surface_solaire, (0, 0))
            dessiner_anneaux_saturne(window, saturne)
        
        if en_pause:
            for planet in systeme_solaire.planets:
                if planet.survole(pos_souris):
                    planet.afficher_info(window, pos_souris)  # Afficher les infos de la planète
            for satellite in systeme_solaire.satellites:
                if satellite.survole(pos_souris):
                    satellite.afficher_info(window, pos_souris)  # Afficher les infos du satellite
        
        if date_changee: # si la date a ete changee pendant stop
            
            en_pause = False 
            systeme_solaire.mouvement(en_pause)  # maj une fois les positions
            systeme_solaire.avancer_date = True
            date_changee = False  # reninit la variable
            en_pause = True
        
        # afficher la fenêtre des phases de la Lune si elle est visible
        Lune.dessiner_lune(fenetre_lune_visible, phase_actuelle_lune)
        
        #dessiner boutons
        
        if fenetre_lune_visible:
            Bouton.dessiner_bouton(window, "x", bouton_ouvrir_fermer, RED) #fermer
        else:
            Bouton.dessiner_bouton(window, "o", bouton_ouvrir_fermer, CYAN) #ouvrir
            
        Bouton.dessiner_bouton(window, "stop", bouton_stop, ORANGE)
        Bouton.dessiner_bouton(window, "zoom", bouton_zoom, ORANGE)
        Bouton.dessiner_bouton(window, "dezoom", bouton_dezoom, ORANGE)
        Bouton.dessiner_bouton(window, "recentrer", bouton_recentrer, ORANGE)
        Bouton.dessiner_bouton(window, "axe visible", bouton_axe_visible, ORANGE)
        Bouton.dessiner_bouton(window, "vitesse +", bouton_augmenter_vitesse, ORANGE)
        Bouton.dessiner_bouton(window, "vitesse -", bouton_diminuer_vitesse, ORANGE)


        #  cadre autour des commandes de musique
        pygame.draw.rect(window, DARKGREY, (width_window - 320, height_window - 110, 300, 100), 0, 5)
        
        txt_surface = font.render(texte, True, couleur)
        width = max(200, txt_surface.get_width() + 10)
        case.w = width
        window.blit(txt_surface, (case.x + 5, case.y + 5))
        pygame.draw.rect(window, couleur, case, 2)
        
        # dessiner boutons contrôle de musique
        bouton_lire_pause.dessiner(window)
        bouton_prec.dessiner(window)
        bouton_suiv.dessiner(window)
        
        
        # afficher titre musique en cours
        font = pygame.font.SysFont("Times New Roman", 20)
        #titre_musique = font.render(liste_musiques[index_musique].split("")[-1].replace("", ""), True, WHITE)
        #window.blit(titre_musique, (width_window - 320 , height_window - 140))

        
        boutonEruption.dessiner(window)
        boutonMeteorite.dessiner(window)

        # affichage date
        font_date = pygame.font.SysFont("Times New Roman", 30)
        date_texte = font_date.render(systeme_solaire.date.strftime("%d/%m/%Y"), True, WHITE)
        window.blit(date_texte, (100,height_window - 50))

        asteroide_instance.dessiner_ceinture_asteroides(window, (centre_x + zoom_factor, centre_y + zoom_factor), 0.002, pause, zoom_factor)

        #Afficher le score
        font = pygame.font.SysFont("Times New Roman", 30)
        score_txt = font.render(f"Score: {systeme_solaire.score}", True, WHITE)
        window.blit(score_txt,  (1100,400))
        print(systeme_solaire.score)

        #image signe astro

        if image_signe:
            pygame.draw.rect(window, (255, 255, 255), (95, height_window - 160, 118, 118))  # fond blanc
            window.blit(image_signe, (100, height_window - 150))
       
         # Mettre à jour l'affichage
        pygame.display.update()
    
    
        pygame.display.update()

        clock.tick(FPS)


    pygame.quit()

# Lancer le programme
main()
