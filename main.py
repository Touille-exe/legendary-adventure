import pygame
import pyscroll
import pytmx

pygame.init()

# --- Paramètres de la fenêtre ---
largeur_ecran = 800
hauteur_ecran = 600
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Cats and Cats 😺")

# --- Charge la spritesheet ---
def charger_animations(image, index_perso):
    largeur = 64
    hauteur = 64
    animations = {
        "bas": [],
        "gauche": [],
        "droite": [],
        "haut": [],
    }
    directions = ["bas", "gauche", "droite", "haut"]
    x_debut = index_perso * 3 * largeur

    for i, direction in enumerate(directions):
        for frame in range(3):
            x = x_debut + frame * largeur
            y = i * hauteur
            rect = pygame.Rect(x, y, largeur, hauteur)
            sprite = image.subsurface(rect)
            animations[direction].append(sprite)
    return animations

# --- Classe Joueur ---
class Joueur(pygame.sprite.Sprite):
    def __init__(self, position, animations):
        super().__init__()
        self.animations = animations
        self.direction = "bas"
        self.frame = 0
        self.image = self.animations[self.direction][self.frame]
        self.rect = self.image.get_rect(topleft=position)
        self.pos = list(position)
        self.vitesse = 2
        self.timer_anim = 0
        self.en_mouvement = False

    def deplacer(self, touches):
        dx = dy = 0
        self.en_mouvement = False
        if touches[pygame.K_UP]:
            self.direction = "haut"
            dy = -self.vitesse
        elif touches[pygame.K_DOWN]:
            self.direction = "bas"
            dy = self.vitesse
        elif touches[pygame.K_LEFT]:
            self.direction = "gauche"
            dx = -self.vitesse
        elif touches[pygame.K_RIGHT]:
            self.direction = "droite"
            dx = self.vitesse

        if dx != 0 or dy != 0:
            self.en_mouvement = True
            self.pos[0] += dx
            self.pos[1] += dy
            self.rect.topleft = self.pos

    def update(self):
        if self.en_mouvement:
            self.timer_anim += 1
            if self.timer_anim >= 10:
                self.timer_anim = 0
                self.frame = (self.frame + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.frame]
        else:
            self.frame = 1  # image neutre au repos
            self.image = self.animations[self.direction][self.frame]

# --- Chargement de la carte ---
tmx_data = pytmx.util_pygame.load_pygame("assets/ma_carte.tmx")
carte_data = pyscroll.data.TiledMapData(tmx_data)
carte_renderer = pyscroll.orthographic.BufferedRenderer(carte_data, (largeur_ecran, hauteur_ecran))

# --- Position du joueur ---
spawn = tmx_data.get_object_by_name("spawn")
position_joueur = (spawn.x, spawn.y)

# --- Chargement du joueur ---
image_spritesheet = pygame.image.load("assets/spritesheet.png").convert_alpha()
animations = charger_animations(image_spritesheet, index_perso=1)
joueur = Joueur(position_joueur, animations)

# --- Collisions avec le calque d’objets "arbres" ---
calque_objets = tmx_data.get_layer_by_name("arbres")
collisions = [pygame.Rect(obj.x, obj.y, obj.width, obj.height) for obj in calque_objets]

# --- Groupe Pyscroll ---
groupe_de_dessin = pyscroll.PyscrollGroup(map_layer=carte_renderer, default_layer=1)
groupe_de_dessin.add(joueur)

# --- Boucle principale ---
horloge = pygame.time.Clock()
en_cours = True

while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    touches = pygame.key.get_pressed()
    ancienne_pos = joueur.pos[:]
    joueur.deplacer(touches)

    # Collision
    if any(joueur.rect.colliderect(obj) for obj in collisions):
        joueur.pos = ancienne_pos
        joueur.rect.topleft = joueur.pos

    groupe_de_dessin.center(joueur.rect.center)
    groupe_de_dessin.update()
    groupe_de_dessin.draw(ecran)
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
