import pygame



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
size = height, width = 1280, 720
screen = pygame.display.set_mode(size)
player_sprites = pygame.sprite.Group()
see_sprites = pygame.sprite.Group()
evil_sprites = pygame.sprite.Group()
pl = Player(pygame.image.load("datafiles/anim.png"), 5, 1, 10, 400)
running = True
while running:
    for i in pygame.event.get():
        pass
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT]:
        pl.update("r")
    if key[pygame.K_LEFT]:
        pl.update("l")
    screen.fill(pygame.Color("black"))
    # Update the animations
    player_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(8)
