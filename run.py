import pygame
import pytmx


class Map:
    def __init__(self, pl):
        self.map = pytmx.load_pygame('map.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.pl = pl

    def render(self, screen):
        for i in [0, 1, 2]:
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, i)
                    if image:
                        screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)]
    def get_free(self, pos):
        return self.get_tile_id(pos) in self.pl



class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)


    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, n):
        self.cur_frame = self.cur_frame + 1
        if n == "r":
            self.image = self.frames[self.cur_frame]
        else:
            images = self.frames[self.cur_frame]
            images = pygame.transform.flip(images, True, False)
            self.image = images

        if self.cur_frame == 4:
            self.cur_frame = 1


clock = pygame.time.Clock()
size = height, width = 1920, 800
screen = pygame.display.set_mode(size)
player_sprites = pygame.sprite.Group()
see_sprites = pygame.sprite.Group()
evil_sprites = pygame.sprite.Group()
pl = Player(pygame.image.load("datafiles/anim.png"), 5, 1, 10, 400)
running = True
mapp = Map(97)
while running:
    for i in pygame.event.get():
        pass
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT]:
        pl.update("r")
    if key[pygame.K_LEFT]:
        pl.update("l")
    screen.fill(pygame.Color("black"))

    # Update the map
    mapp.render(screen)
    # Update the animations
    player_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(8)
