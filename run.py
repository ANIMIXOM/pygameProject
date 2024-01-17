import pygame


class enger_spire(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(eff_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frames = 0
        self.image = self.frames[self.cur_frames]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frames += 1
        self.image = self.frames[self.cur_frames]
        if self.cur_frames >= 2:
            self.cur_frames = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_sprites)
        self.frames_hod = []
        self.frames_at = []
        self.cut_sheet_hod(sheet, columns, rows)
        self.cut_sheet_attack(pygame.image.load("datafiles/anim_at.png"), 3, 1)
        self.cur_frame = 0
        self.image = self.frames_hod[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet_hod(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames_hod.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet_attack(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames_at.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_hod(self, n):
        self.cur_frame = self.cur_frame + 1
        if n == "r":
            self.rect.x += 30
            self.image = self.frames_hod[self.cur_frame]
        else:
            self.rect.x -= 30
            images = self.frames_hod[self.cur_frame]
            images = pygame.transform.flip(images, True, False)
            self.image = images

        if self.cur_frame == 4:
            self.cur_frame = 1

    def update_attack(self):
        self.cur_frame = self.cur_frame + 1
        if not otr:
            self.image = self.frames_at[self.cur_frame]
        else:
            images = self.frames_at[self.cur_frame]
            images = pygame.transform.flip(images, True, False)
            self.image = images
        if self.cur_frame == 2:
            self.cur_frame = 0


inventory = {"fire_cristal": 2, "el_cristal": 0, "frozen_cristal": 0}

otr = False
clock = pygame.time.Clock()
size = height, width = 1280, 720
screen = pygame.display.set_mode(size)
eff_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
see_sprites = pygame.sprite.Group()
evil_sprites = pygame.sprite.Group()
pl = Player(pygame.image.load("datafiles/anim.png"), 5, 1, 10, 400)
running = True
attack = [False, 0]
attack_cr = [False, 0]

while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pl.cur_frame >= 2:
                    pl.cur_frame = 0
                attack = [True, 0]
                print("attack")
                pl.update_attack()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if inventory["fire_cristal"] != 0:
                        inventory["fire_cristal"] -= 1
                        enger_spire(pygame.image.load("datafiles/anim_fire.png"), 3, 1, pl.rect.x - 20, pl.rect.y - 10)
                        attack_cr = [True, 0]

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            pl.update_hod("r")
            otr = False
        if key[pygame.K_LEFT]:
            pl.update_hod("l")
            otr = True
        if attack[0] and attack[1] <= 2:
            pl.update_attack()
            attack[1] += 1
        else:
            attack = [False, 0]
        screen.fill(pygame.Color("black"))
        if attack_cr[0] and attack_cr[1] <= 10:
            eff_sprites.update()
            eff_sprites.draw(screen)
            attack_cr[1] += 1
        else:
            eff_sprites.empty()
            attack_cr[0] = False
            attack_cr[1] = 0
        player_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10)
    except IndexError:
        pl.cur_frame = 0
        print("Ошибка анимации")
