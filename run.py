import pygame

pygame.init()
gui_torg = False


class gui_torg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gui_sell = pygame.image.load("datafiles/sell.png")
        self.rect_sell = self.gui_sell.get_rect()

    def update(self):
        screen.blit(self.gui_sell, (200, 200))
        key = pygame.key.get_pressed()
        if key[pygame.K_g]:
            if inventory["wearpon"] > 0:
                inventory["wearpon"] -= 1
                inventory["rupis"] += 1
            else:
                print("У вас нету товара")
        if key[pygame.K_h]:
            if inventory["rupis"] >= 3:
                inventory["rupis"] -= 3
                inventory["fire_cristal"] += 1
            else:
                print("Нема деняг")


class torg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(see_sprites)
        self.image = pygame.image.load("datafiles/torg.png")
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 300

    def update(self):
        if pygame.sprite.spritecollide(self, player_sprites, dokill=False):
            global fand_torg
            fand_torg = True
            pl.rect.x += 200
        screen.blit(self.image, (700, 280))


maps = "map0"


class gui:
    def __init__(self):
        self.font = pygame.font.Font("datafiles/Lightman.ttf", 20)
        self.text_surface = self.font.render("99", True, (255, 255, 255))
        self.healim = pygame.image.load("datafiles/health.png")
        self.healim = pygame.transform.scale(self.healim, (50, 50))
        self.summ = str(inventory["rupis"])
        self.rup = self.font.render(self.summ, True, (20, 255, 20))

    def update(self):
        screen.blit(self.healim, (10, 10))
        screen.blit(self.text_surface, (20, 20))
        screen.blit(self.rup, (100, 20))
        self.summ = str(inventory["rupis"])
        self.rup = self.font.render(self.summ, True, (20, 255, 20))
        self.text_surface = self.text_surface = self.font.render(
            str(pl.hp), True, (255, 255, 255)
        )


class Evil(pygame.sprite.Sprite):
    def __init__(self, player_sprites, x, y, image, hp):
        super().__init__(evil_sprites)
        self.poison = 0
        self.hp = int(hp)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player_sprites = player_sprites

    def update(self):
        if self.hp > 0:
            player = self.player_sprites.sprites()[0]
            distance = abs(pl.rect.x - self.rect.x)
            if self.hp >= 0:
                # Проверяем дистанцию между игроком и врагом
                if distance < 200:
                    # Идем на игрока
                    if pl.rect.x - self.rect.x > 0:
                        self.rect.x += 8
                    else:
                        self.rect.x -= 8

                # Проверяем столкновение с игроком
                if pygame.sprite.spritecollide(self, self.player_sprites, False):
                    pl.hp -= 1
                self.hp -= self.poison


class enger_spire(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(eff_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frames = 0
        self.image = self.frames[self.cur_frames]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(
            0, 0, sheet.get_width() // columns, sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(
                    sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                )

    def update(self):
        self.cur_frames += 1
        self.image = self.frames[self.cur_frames]
        if self.cur_frames >= 2:
            self.cur_frames = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_sprites)
        self.hp = 100
        self.frames_hod = []
        self.frames_at = []
        self.cut_sheet_hod(sheet, columns, rows)
        self.cut_sheet_attack(pygame.image.load("datafiles/anim_at.png"), 3, 1)
        self.cur_frame = 0
        self.image = self.frames_hod[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet_hod(self, sheet, columns, rows):
        self.rect = pygame.Rect(
            0, 0, sheet.get_width() // columns, sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames_hod.append(
                    sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                )

    def cut_sheet_attack(self, sheet, columns, rows):
        self.rect = pygame.Rect(
            0, 0, sheet.get_width() // columns, sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames_at.append(
                    sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                )

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


inventory = {
    "fire_cristal": 10,
    "el_cristal": 2,
    "healme5": 3,
    "healme20": 10,
    "healme100": 1,
    "wearpon": 20,
    "rupis": 20,
}
fand_torg = False
otr = False
clock = pygame.time.Clock()
size = height, width = 1280, 720
screen = pygame.display.set_mode(size)
eff_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
see_sprites = pygame.sprite.Group()
evil_sprites = pygame.sprite.Group()
pl = Player(pygame.image.load("datafiles/anim.png"), 5, 1, 10, 500)
running = True
attack = [False, 0]
attack_cr = [False, 0]
gui = gui()
Torg = torg()
torg_in_map = True
gui_t = gui_torg()
sound_hod = pygame.mixer.Sound("datafiles/soundh.mp3")
fire_son = pygame.mixer.Sound("datafiles/fire_son.mp3")
mous = None
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
                for i in evil_sprites:
                    if abs(i.rect.x - pl.rect.x) <= 60:
                        i.hp -= 5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if inventory["fire_cristal"] != 0:
                        inventory["fire_cristal"] -= 1
                        enger_spire(
                            pygame.image.load("datafiles/anim_fire.png"),
                            3,
                            1,
                            pl.rect.x - 20,
                            pl.rect.y - 10,
                        )
                        attack_cr = [True, 0]
                        fire_son.play()
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    sound_hod.play(-1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    sound_hod.stop()
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
        screen.blit(pygame.image.load("datafiles/map1.png"), (0, 0))
        if attack_cr[0] and attack_cr[1] <= 10:
            eff_sprites.update()
            eff_sprites.draw(screen)
            attack_cr[1] += 1
        else:
            eff_sprites.empty()
            fire_son.stop()
            attack_cr[0] = False
            attack_cr[1] = 0
        if eff_sprites:
            for i in eff_sprites:
                if evil_sprites:
                    for j in evil_sprites:
                        if abs(i.rect.x - j.rect.x) <= 50:
                            j.poison += 1
        evil_sprites.draw(screen)
        evil_sprites.update()
        player_sprites.draw(screen)
        gui.update()
        if torg_in_map:
            Torg.update()
        if fand_torg:
            gui_t.update()
        pygame.display.flip()
        clock.tick(10)
    except IndexError:
        pl.cur_frame = 0
        print("Ошибка анимации")
