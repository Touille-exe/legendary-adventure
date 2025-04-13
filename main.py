import pygame
import pyscroll

pygame.init()

largeur_ecran = 800
hauteur_ecran = 600
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Cats ands Cats 😺") # Donne un nom à ta fenêtre

image_personnage = pygame.image.load("mon_personnage.png").convert_alpha() # .convert_alpha() pour la transparence

carte_data = pyscroll.data.TiledMapData("assets/ma_carte.tmx") # Si tu utilises un logiciel comme Tiled pour créer ta carte
carte_renderer = pyscroll.orthographic.BufferedRenderer(carte_data, ecran.get_size(), clamp_camera=False)
groupe_de_dessin = pyscroll.PyscrollGroup(renderer=carte_renderer, map_layer=carte_renderer.get_layer_by_name("calque_des_collisions")) # "calque_des_collisions" est un exemple, adapte-le à ta carte

position_personnage = image_personnage.get_rect()
position_personnage.center = (largeur_ecran // 2, hauteur_ecran // 2) # Au centre de l'écran au début

en_cours = True
while en_cours:
    # 1. Gérer les événements (clavier, souris, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        # Ici, tu vas ajouter les contrôles de ton personnage (par exemple, si on appuie sur une touche, il bouge)

    # 2. Mettre à jour l'état du jeu (positions, scores, etc.)
    # Par exemple, si une touche est pressée, modifier la position du personnage

    # 3. Dessiner tout à l'écran
    ecran.fill((255, 255, 255)) # Efface l'écran à chaque image (noir ici)
    groupe_de_dessin.draw(ecran) # Dessine la carte avec Pyscroll
    ecran.blit(image_personnage, position_personnage) # Dessine le personnage
    pygame.display.flip() # Montre ce qui a été dessiné

    # 4. Contrôler la vitesse du jeu (facultatif mais recommandé)
    pygame.time.Clock().tick(60) # Limite le jeu à 60 images par seconde

pygame.quit()