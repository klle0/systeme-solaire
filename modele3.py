import pygame
import math
import random

# Initialisation de Pygame
pygame.init()

# Fenêtre du jeu
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

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

# images pour les boutons
tailleimage = (70,70)
image_lire = pygame.transform.scale(pygame.image.load("lire.png"), tailleimage)  # triangle de lecture
image_pause = pygame.transform.scale(pygame.image.load("pause.png"), tailleimage)  # deux barres pour arrêter
image_prec = pygame.transform.scale(pygame.image.load("prec.png"), tailleimage)
image_suiv = pygame.transform.scale(pygame.image.load("suiv.png"), tailleimage)

# Récupére les dimensions de la fenêtre pour mettre la page en plein écran
width_window, height_window = pygame.display.get_surface().get_size()

# Détermine les coordonnées du centre de la page par rapport a l'ecran
centre_x = width_window // 2
centre_y = height_window // 2

def scale_value(value, screen_width):
    # Exemple d'échelle, ajustez le facteur comme nécessaire
    return int(value * (screen_width / 1920))  # 1920 peut être la largeur de référence

class Bouton:
    # dessiner un bouton
    def dessiner_bouton(surface, txt, rect, couleur):
        pygame.draw.rect(surface, couleur, rect)
        font = pygame.font.SysFont("comicsansms", 25)
        surface_texte = font.render(txt, True, BLACK)
        rectangle_txt = surface_texte.get_rect(center=rect.center)
        #coodonées et dimensions du rectangle du txt + centrer txt 
        surface.blit(surface_texte, rectangle_txt)
        #dessine une surface
        
class Bouton_eruption:
    #classe bouton pour les eruptions
    def __init__(self, x, y, w, h, couleur, texte):
        self.rect = pygame.Rect(x, y, w, h)
        self.couleur = couleur
        self.texte = texte
        self.font = pygame.font.SysFont("comicsansms", 25)
        
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
        self.en_pause = True  # demarre en etat de pause

    def dessiner(self, surface):
        if self.en_pause:
            surface.blit(self.image_lire, self.rect.topleft)  # image de lecture
        else:
            surface.blit(self.image_pause, self.rect.topleft)  # image de pause
        
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)
    
# creer boutons de contrôle de la musique
bouton_lire_pause = BoutonMusique(1400, 800, image_lire, image_pause)
bouton_prec = BoutonMusique(1320, 800, image_prec, image_prec) 
bouton_suiv = BoutonMusique(1480, 800, image_suiv, image_suiv) 

class Meteorite:
    def __init__(self):
        self.x = random.randint(0, width_window)
        self.y = 0
        self.vitesse_y = random.uniform(5, 10)  # vitesse verticale
        self.vitesse_x = random.uniform(-5, 5)   # vitesse horizontale
        self.taille = random.randint(1, 2)

    def mouvement(self):
        # faaire descendre la meteorite
        self.y += self.vitesse_y
        self.x += self.vitesse_x

    def dessiner(self, surface):
        # Dessine la météorite
        pygame.draw.circle(surface, GREY, (self.x, int(self.y)), self.taille)

# Classe Planete
class Planet:
    def __init__(self, nom, color, rayon_x, rayon_y, speed, size, diametre, population, info=""):
        self.nom = nom
        self.color = color
        self.rayon_x = rayon_x
        self.rayon_y = rayon_y
        self.speed = speed
        self.size = size
        self.diametre = diametre  # Ajout du diamètre
        self.population = population  # Ajout de la population
        self.angle = 0
        self.info = info.split("|")  # On garde les retours à la ligne

    def mouvP(self, en_pause):
        #deplacement des planetes si pas en pause
        if not en_pause:
            self.x = centre_x + self.rayon_x * math.cos(self.angle)
            self.y = centre_y + self.rayon_y * math.sin(self.angle)
            self.angle += self.speed

    def drawP(self, surface):
        #affiche les planetes
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        
    def survole(self, pos_souris):
        distance = math.hypot(pos_souris[0] - self.x, pos_souris[1] - self.y)
        return distance <= self.size

    def afficher_info(self, surface, pos_souris):
        font = pygame.font.SysFont("comicsansms", 20)
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
    def __init__(self, nom, color, rayon_x, rayon_y, speed, size, planet_parent, diametre, population, info=""):
        self.nom = nom
        self.color = color
        self.rayon_x = rayon_x
        self.rayon_y = rayon_y
        self.speed = speed
        self.size = size
        self.angle = 0
        self.planet_parent = planet_parent
        self.diametre = diametre  # Ajout du diamètre
        self.population = population  # Ajout de la population
        self.info = info.split("|")

    def mouvS(self,en_pause):
        #mouvement des sattelites si pas en pause
        if not en_pause:
            self.x = self.planet_parent.x + self.rayon_x * math.cos(self.angle)
            self.y = self.planet_parent.y + self.rayon_y * math.sin(self.angle)
            self.angle += self.speed

    def drawS(self, surface):
        #affiche les satellittes
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

    def survole(self, pos_souris):
        distance = math.hypot(pos_souris[0] - self.x, pos_souris[1] - self.y)
        return distance <= self.size
    
    def afficher_info(self, surface, pos_souris):
        font = pygame.font.SysFont("comicsansms", 20)
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
        self.vitesse = random.uniform(1, 2)  # vitesse d'extension de l'éruption
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
    def __init__(self):
        self.planets = []
        self.satellites = []
        self.eruptions = []  # lsite eruptions solaires
        self.meteorites = []

    def add_planet(self, planet):
        self.planets.append(planet)

    def add_satellite(self, satellite):
        self.satellites.append(satellite)
        
    def ajoutermeteorite(self):
        self.meteorites.append(Meteorite())
        
    def add_eruption(self):
        self.eruptions.append(eruptionSolaire())

    def mouvement(self, en_pause):
        #mouvement si ce n'est pas en pause
        for planet in self.planets:
            planet.mouvP(en_pause)
        for satellite in self.satellites:
            satellite.mouvS(en_pause)
            
        for eruption in self.eruptions:
            eruption.mouvement()
            
        for meteorite in self.meteorites:
            meteorite.mouvement()

    def draw(self, surface,eruption_visible):
        
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
                
    def enlevermeteorite(self):
        # enelve meteorites qui sortent de l'ecran
        self.meteorites = [m for m in self.meteorites if m.y < height_window and m.x < width_window]

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

class Asteroide:
    
        # Variables de configuration pour la ceinture d'astéroïdes
    nombre_asteroides = 200  # Nombre d'astéroïdes dans la ceinture
    distance_ceinture = scale_value(300, width_window)  # Distance de la ceinture par rapport au soleil
    vitesse_rotation_ceinture = 0.001  # Vitesse de rotation de la ceinture


    # Initialisation des astéroïdes avec des angles aléatoires et des distances fixes
    asteroides = [{'angle': random.uniform(0, 2 * math.pi)} for _ in range(nombre_asteroides)]

    def dessiner_ceinture_asteroides(surface, centre,asteroides,distance_ceinture,vitesse_rotation_ceinture):
        for asteroide in asteroides:
            # Mise à jour de l'angle pour créer une rotation
            asteroide['angle'] += vitesse_rotation_ceinture
            angle = asteroide['angle']
            
            # Calcul des positions X et Y en fonction de l'angle et de la distance
            x = centre[0] + distance_ceinture * math.cos(angle)
            y = centre[1] + distance_ceinture * math.sin(angle)
            
            # Dessiner chaque astéroïde comme un petit cercle
            pygame.draw.circle(surface, (169, 169, 169), (int(x), int(y)), 2)  # Taille et couleur de l'astéroïde

    

# Fonction principale
def main():
        # Récupérer la largeur de la fenêtre
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Créer le système solaire
    systeme_solaire = SystemeSolaire()
    
    #taille du soleil
    size_sun = scale_value(100, screen_width)  # Taille du soleil à l'échelle
    soleil = Planet("Soleil", YELLOW, scale_value(0, screen_width), scale_value(0, screen_width), 0, size_sun, 1392000, "0", "État: Gazeux | Temp: 5778 K")
    systeme_solaire.add_planet(soleil)
    
    

    #ajouter des palente
    mercure = Planet("Mercure", GREY, scale_value(size_sun +140, screen_width), scale_value(130, screen_width), 0.047, scale_value(4, screen_width), 4879, "0", "Eau: 0% | Pression: ~0 atm | Temp: -173 à 427°C")
    terre = Planet("Terre", BLUE, scale_value(size_sun + 220, screen_width), scale_value(180, screen_width), 0.029, scale_value(10, screen_width), 12742, "7,9 milliards", "Eau: 71% | Pression: 1 atm | Temp: -88 à 58°C")
    venus = Planet("Vénus", ORANGE, scale_value(size_sun + 195, screen_width), scale_value(180, screen_width), 0.035, scale_value(9, screen_width), 12104, "0", "Eau: 0% | Pression: 92 atm | Temp: 462°C")
    mars = Planet("Mars", RED, scale_value(size_sun + 300, screen_width), scale_value(240, screen_width), 0.024, scale_value(5, screen_width), 6779, "0", "Eau: Traces | Pression: 0.006 atm | Temp: -125 à 20°C")
    systeme_solaire.add_planet(terre)
    systeme_solaire.add_planet(mercure)
    systeme_solaire.add_planet(venus)
    systeme_solaire.add_planet(mars)

    # ajoute des planètes gazeuses
    jupiter = Planet("Jupiter", (255, 165, 0), scale_value(450, screen_width), scale_value(300, screen_width), 0.013, scale_value(15, screen_width), 139820, "0", "État: Gazeux | Eau: Traces | Temp: -108°C")
    satellite_jupiter1 = Satellite("Io", BROWN, scale_value(50, screen_width), scale_value(30, screen_width), 0.04, scale_value(4, screen_width), jupiter, 3642, "0", "État: Solide | Eau: Traces")
    satellite_jupiter2 = Satellite("Europa", CYAN, scale_value(60, screen_width), scale_value(40, screen_width), 0.03, scale_value(5, screen_width), jupiter, 3121, "0", "État: Solide | Eau: Traces | Océans sous la surface")
    satellite_jupiter3 = Satellite("Ganymède", GREY, scale_value(70, screen_width), scale_value(50, screen_width), 0.025, scale_value(6, screen_width), jupiter, 5262, "0", "État: Solide | Eau: Traces")
    satellite_jupiter4 = Satellite("Callisto", (200, 200, 200), scale_value(80, screen_width), scale_value(60, screen_width), 0.02, scale_value(6, screen_width), jupiter, 4820, "0", "État: Solide | Eau: Traces")
    systeme_solaire.add_planet(jupiter)
    systeme_solaire.add_satellite(satellite_jupiter1)
    systeme_solaire.add_satellite(satellite_jupiter2)
    systeme_solaire.add_satellite(satellite_jupiter3)
    systeme_solaire.add_satellite(satellite_jupiter4)

        #dessiner les anneaux de Saturne
    def dessiner_anneaux_saturne(surface, saturne):
        anneaux_largeur = [scale_value(20, width_window), scale_value(40, width_window), scale_value(60, width_window)]
        anneaux_couleurs = [(210, 180, 140), (192, 192, 192), (169, 169, 169)]  # Couleurs des anneaux

        for largeur, couleur in zip(anneaux_largeur, anneaux_couleurs):
            pygame.draw.ellipse(
                surface, couleur,
                pygame.Rect(
                    saturne.x - largeur // 2,  # Décalage en fonction de la taille des anneaux
                    saturne.y - largeur // 4,  # Ajustement en hauteur pour l'effet ellipse
                    largeur,
                    largeur // 2),1)# Épaisseur de l'anneau
            
    saturne = Planet("Saturne", (255, 215, 0), scale_value(600, screen_width), scale_value(350, screen_width), 0.011, scale_value(12, screen_width), 116460, "0", "État: Gazeux | Eau: Traces | Temp: -178°C")
    satellite_saturne1 = Satellite("Titan", (255, 165, 0), scale_value(70, screen_width), scale_value(40, screen_width), 0.035, scale_value(6, screen_width), saturne, 5150, "0", "État: Solide | Eau: Lacs de méthane")
    satellite_saturne2 = Satellite("Rhea", (169, 169, 169), scale_value(80, screen_width), scale_value(50, screen_width), 0.02, scale_value(5, screen_width), saturne, 1528, "0", "État: Solide | Eau: Traces")
    systeme_solaire.add_planet(saturne)
    systeme_solaire.add_satellite(satellite_saturne1)
    systeme_solaire.add_satellite(satellite_saturne2)

    uranus = Planet("Uranus", (173, 216, 230), scale_value(800, screen_width), scale_value(400, screen_width), 0.008, scale_value(10, screen_width), 50724, "0", "État: Gazeux | Eau: Traces | Temp: -224°C")
    satellite_uranus1 = Satellite("Titania", (210, 180, 140), scale_value(50, screen_width), scale_value(30, screen_width), 0.03, scale_value(4, screen_width), uranus, 1577, "0", "État: Solide | Eau: Traces")
    satellite_uranus2 = Satellite("Oberon", (200, 200, 200), scale_value(60, screen_width), scale_value(40, screen_width), 0.02, scale_value(4, screen_width), uranus, 1523, "0", "État: Solide | Eau: Traces")
    systeme_solaire.add_planet(uranus)
    systeme_solaire.add_satellite(satellite_uranus1)
    systeme_solaire.add_satellite(satellite_uranus2)

    neptune = Planet("Neptune", (30, 144, 255), scale_value(900, screen_width), scale_value(500, screen_width), 0.007, scale_value(9, screen_width), 49244, "0", "État: Gazeux | Eau: Traces | Temp: -214°C")
    satellite_neptune1 = Satellite("Triton", (200, 200, 200), scale_value(50, screen_width), scale_value(30, screen_width), 0.03, scale_value(5, screen_width), neptune, 2706, "0", "État: Solide | Eau: Traces")
    systeme_solaire.add_planet(neptune)
    systeme_solaire.add_satellite(satellite_neptune1)
    


    # ajout des satellites
    lune = Satellite("Lune", GREY, scale_value(30, screen_width), scale_value(22, screen_width), 0.1, scale_value(3, screen_width), terre, 3474, "0", "Eau: Traces | Pression: ~0 atm | Temp: -183 à 106°C")
    systeme_solaire.add_satellite(lune)

    systeme_solaire.add_planet(soleil)
    
    #controle visibilité de la fenetre de la lune
    fenetre_lune_visible = False
    
    #pause
    en_pause = False
    
    premierTour = True
    
    # variable pr activer/désactiver les meteorites et les eruptions
    eruption_visible = True
    meteorites_actives = True
    
    
    # creation des boutons
    bouton_ouvrir_fermer = pygame.Rect(1520, 50, 30, 30)
    bouton_stop = pygame.Rect(100, 50, 100, 50)
    boutonEruption = Bouton_eruption(100, 150, 200, 50, ORANGE, "eruptions: on")
    boutonMeteorite = Bouton_eruption(100, 250, 200, 50, ORANGE, "météorites: on")
    
    global index_musique
    musique_joue = False
    pygame.mixer.music.load(liste_musiques[index_musique])  # chargement premiere musique
    
    
    # Boucle du jeu
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
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

        window.fill(BLACK)
        
        # ajout de meteorites si actives
        if meteorites_actives and random.random() < 0.1:
            systeme_solaire.ajoutermeteorite()

        
        #  cadre autour des commandes de musique
        
        cadreW = width_window - 320
        pygame.draw.rect(window, DARKGREY, (cadreW, height_window - 110, 300, 100), 0, 5)

        # dessiner boutons contrôle de musique
        bouton_lire_pause.dessiner(window)
        bouton_prec.dessiner(window)
        bouton_suiv.dessiner(window)

        # afficher titre musique en cours
        font = pygame.font.SysFont("comicsansms", 20)
        titre_musique = font.render(liste_musiques[index_musique], True, WHITE)
        window.blit(titre_musique, (cadreW , height_window - 140))
        
        # proba apparition d'une nouvelle eruption
        if random.random() < 0.03:
            systeme_solaire.add_eruption()

        # Mise à jour des positions
        systeme_solaire.mouvement(en_pause)
        
        systeme_solaire.enlevermeteorite()

        # affice le système solaire
        systeme_solaire.draw(window,eruption_visible)
        
        # Dessiner les anneaux de Saturne après Saturne
        dessiner_anneaux_saturne(window, saturne)

        pos_souris = pygame.mouse.get_pos()
        
        #fenetre de la lune
        phase_actuelle_lune = Lune.det_phase_lune(lune.angle)
        
        if en_pause:
            for planet in systeme_solaire.planets:
                if planet.survole(pos_souris):
                    planet.afficher_info(window, pos_souris)  # Afficher les infos de la planète

            for satellite in systeme_solaire.satellites:
                if satellite.survole(pos_souris):
                    satellite.afficher_info(window, pos_souris)  # Afficher les infos du satellite
        
        # afficher la fenêtre des phases de la Lune si elle est visible
        Lune.dessiner_lune(fenetre_lune_visible, phase_actuelle_lune)
        
        #dessiner boutons
        
        if fenetre_lune_visible:
            Bouton.dessiner_bouton(window, "x", bouton_ouvrir_fermer, RED) #fermer
        else:
            Bouton.dessiner_bouton(window, "o", bouton_ouvrir_fermer, CYAN) #ouvrir
            
        Bouton.dessiner_bouton(window, "stop", bouton_stop, ORANGE)
        
        boutonEruption.dessiner(window)
        boutonMeteorite.dessiner(window)

        # Mettre à jour l'affichage
        pygame.display.update()

    
        pygame.time.Clock().tick(60)

    pygame.quit()

# Lancer le programme
main()

