import pygame


class player(pygame.sprite.Sprite):
    images = pygame.image.load("datafiles/player_stof.png")

    def __init__(self):
        super().__init__(player_sprites)
        self.image = images
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update_anim(self, group, events):
        if group == 1:  # хождение
            pass
        if group == 2:  # уворот
            pass
        if group == 3:  # атака
            pass


clock = pygame.time.Clock()
size = height, width = 600, 500
screen = pygame.display.set_mode(size)
player_sprites = pygame.sprite.Group()
see_sprites = pygame.sprite.Group()
evil_sprites = pygame.sprite.Group()
running = True
while running:
    for i in pygame.event.get():
        pass
    key = pygame.key.get_pressed()
    if key[pygame.K_LCTRL]:
        player.attack()
        player.update_anim(3, 23)
