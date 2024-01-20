import random
import sys
import time

from pygame.transform import scale
import pygame
from pygame.image import load

pygame.init()
gui_torg = False


class Gui_torg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gui_sell = pygame.image.load("datafiles/sell.png")
        self.rect_sell = self.gui_sell.get_rect()
        self.gui_buy_fire = pygame.image.load("datafiles/fire_buy.png")
        self.gui_buy_el = pygame.image.load("datafiles/el_buy.png")
        self.sound = pygame.mixer.Sound("datafiles/torg.mp3")

    def update(self):
        global max_coins
        screen.blit(self.gui_buy_el, (400, 200))
        screen.blit(self.gui_buy_fire, (100, 200))
        screen.blit(self.gui_sell, (250, 200))
        key = pygame.key.get_pressed()
        if key[pygame.K_s]:
            if inventory["loot"] > 0:
                inventory["loot"] -= 1
                inventory["rupis"] += 1
                max_coins += 1
                self.sound.play(1)
            else:
                print("У вас нету товара")
        if key[pygame.K_f]:
            if inventory["rupis"] >= 3:
                inventory["rupis"] -= 3
                inventory["fire_cristal"] += 1
                self.sound.play(1)
            else:
                print("Нема деняг")
        if key[pygame.K_h]:
            if inventory["rupis"] >= 1:
                inventory["rupis"] -= 1
                inventory["healme5"] += 1
                self.sound.play(1)
            else:
                print("Нема деняг")


class Torg(pygame.sprite.Sprite):
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


class Gui:
    def __init__(self):
        global inventory
        self.font = pygame.font.Font("datafiles/Lightman.ttf", 20)
        self.hearts = self.font.render("99", True, (255, 255, 255))
        self.healim = pygame.image.load("datafiles/health.png")
        self.healim = pygame.transform.scale(self.healim, (50, 50))
        self.summ = str(inventory["rupis"])
        self.rup = self.font.render(self.summ, True, (20, 255, 20))
        self.loot = self.font.render(str(inventory["loot"]), True, (20, 255, 20))
        self.potion_hp = self.font.render(
            str(inventory["healme5"]), True, (20, 255, 20)
        )
        self.fire_mag = self.font.render(
            str(inventory["fire_cristal"]), True, (20, 255, 20)
        )

    def update(self):
        screen.blit(self.healim, (25, 10))
        screen.blit(scale(load("datafiles/coin.png"), (50, 50)), (94, 7))
        screen.blit(scale(load("datafiles/inventory.png"), (50, 50)), (163, 7))
        screen.blit(scale(load("datafiles/potion_hp.png"), (50, 70)), (25, 70))
        screen.blit(scale(load("datafiles/fire_mag.png"), (50, 55)), (35, 140))
        screen.blit(self.hearts, (20, 20))
        screen.blit(self.rup, (100, 20))
        screen.blit(self.loot, (180, 20))
        screen.blit(self.potion_hp, (5, 85))
        screen.blit(self.fire_mag, (5, 160))
        self.loot = self.font.render(str(inventory["loot"]), True, (20, 255, 20))
        self.summ = str(inventory["rupis"])
        self.rup = self.font.render(self.summ, True, (20, 255, 20))
        self.hearts = self.hearts = self.font.render(str(pl.hp), True, (255, 255, 255))
        self.potion_hp = self.font.render(
            str(inventory["healme5"]), True, (20, 255, 20)
        )
        self.fire_mag = self.font.render(
            str(inventory["fire_cristal"]), True, (20, 255, 20)
        )


class Evil(pygame.sprite.Sprite):
    def __init__(self, player_sprites, x, y, image, hp, typep):
        super().__init__(evil_sprites)
        self.poison = 0
        self.hp = int(hp)
        self.image = image
        self.type = typep
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player_sprites = player_sprites

    def update(self):
        global flag_is_dying, flag_is_dying_enemy, evils, count, deaths, col_killed_enem, max_col_loots
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
                if pl.hp == 0:
                    flag_is_dying = True
                    deaths += 1

        for i in evils:
            if pygame.sprite.spritecollide(i, eff_sprites, False):
                i.hp -= self.poison
            if evils[i] != 0 and i.hp <= 0:
                if i.type == "normal":
                    i.image = load("datafiles/evil_death.png")
                    i.rect.y += 45
                    loot = random.randint(1, 3)
                else:
                    i.image = scale(load("datafiles/boss_death.png"), (135, 76))
                    loot = random.randint(5, 15)

                inventory["loot"] += loot
                max_col_loots += loot
                evils[i] = 0
                col_killed_enem += 1
        for i in evils:
            if evils[i] == 0 and i.rect.y < 720:
                i.rect.y += 10

        if all(evils[j] == 0 for j in evils) and count == 2:
            flag_is_dying_enemy = True

        else:
            count += 1


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


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, platforms)
        self.image = pygame.Surface((1280, 20))
        self.image.fill("red")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(pos, (1280, 20))


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, player_sprites)
        self.hp = 100
        self.frames_hod = []
        self.frames_at = []
        self.cut_sheet_hod(sheet, columns, rows)
        self.cut_sheet_attack(pygame.image.load("datafiles/anim_at.png"), 3, 1)
        self.cur_frame = 0
        self.image = self.frames_hod[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
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
            self.mask = pygame.mask.from_surface(self.image)

        else:
            self.rect.x -= 30
            images = self.frames_hod[self.cur_frame]
            images = pygame.transform.flip(images, True, False)
            self.image = images
            self.mask = pygame.mask.from_surface(self.image)

        if self.cur_frame == 4:
            self.cur_frame = 1

    def update_attack(self):
        self.cur_frame = self.cur_frame + 1
        if not otr:
            self.image = self.frames_at[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
        else:
            images = self.frames_at[self.cur_frame]
            images = pygame.transform.flip(images, True, False)
            self.image = images
            self.mask = pygame.mask.from_surface(self.image)
        if self.cur_frame == 2:
            self.cur_frame = 0

    def update(self):
        global flag_jumping
        if pygame.sprite.spritecollideany(self, platforms) is None and pl.rect.y <= 500:
            pl.rect.y += 10
            if pl.rect.y == 510:
                flag_jumping = True


def start_or_over_screen():
    global flag_is_dying, inventory
    if flag_is_dying:
        screen.blit(
            scale(load("datafiles/game_over.png"), (1280, 720)),
            (0, 0),
        )
        pl.hp = 100
        inventory = {
            "fire_cristal": 10,
            "el_cristal": 2,
            "healme5": 3,
            "loot": 0,
            "rupis": 20,
        }
    else:
        screen.blit(scale((load("datafiles/start_game.png")), (1280, 720)), (0, 0))
    pl.rect.x = 10
    pl.rect.y = 500
    flag_is_dying = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)


def write_res():
    global deaths, time_max, max_coins, col_killed_enem, max_col_loots
    with open("result_game.txt", "w", encoding="utf-8") as res:
        res.write(f"Время в игре: {time_max} секунд.\n")
        res.write(f"Колличество убитых врагов: {col_killed_enem}.\n")
        res.write(f"Поллучено геля {max_col_loots} с убитых врагов.\n")
        res.write(f"Всего собранно монет: {max_coins}.\n")
        res.write(f"Персоонаж умер {deaths} раз.")


def generate_floor():
    platform = Platform((0, 515))


inventory = {
    "fire_cristal": 10,
    "el_cristal": 2,
    "healme5": 3,
    "loot": 0,
    "rupis": 20,
}
col_killed_enem = 0
max_col_loots = 0
max_coins = 20
time_max = 0
deaths = 0
flag_is_dying = False
flag_is_dying_enemy = False
clock = pygame.time.Clock()
size = height, width = 1280, 720
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
eff_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
see_sprites = pygame.sprite.Group()
evil_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
running = True
attack = [False, 0]
attack_cr = [False, 0]
sound_hod = pygame.mixer.Sound("datafiles/soundh.mp3")
fire_son = pygame.mixer.Sound("datafiles/fire_son.mp3")
gui_t = Gui_torg()
gui = Gui()
torg = Torg()
mous = None
pl = Player(pygame.image.load("datafiles/anim.png"), 5, 1, 10, 500)
otr = False
fand_torg = False
play = True
lvls = 0
flag_jumping = True
enemy_ph = 30
boss_hp = 120
evils = {}
while play:
    time.sleep(1)
    time_max += 1
    if maps == "map0":
        if evils == {} or all(evils[j] == 0 for j in evils):
            torg_in_map = True

    elif maps == "map1" and (evils == {} or all(evils[j] == 0 for j in evils)):
        try:
            fand_torg = False
            torg_in_map = False
            evils = {}
            x = 250
            flag_is_dying_enemy = False
            count = 0
            for i in range(4):
                evils[
                    Evil(
                        player_sprites,
                        x,
                        510,
                        pygame.image.load("datafiles/evil1.png"),
                        enemy_ph,
                        "normal",
                    )
                ] = 1
                x += 150
            lvls += 1
            if lvls % 5 == 1:
                evils[
                    Evil(
                        player_sprites,
                        x,
                        390,
                        scale(pygame.image.load("datafiles/boss.png"), (180, 180)),
                        boss_hp,
                        "boss",
                    )
                ] = 1
            enemy_ph += enemy_ph * 0.05
            boss_hp += boss_hp * 0.05
            print(enemy_ph, boss_hp)
        except TypeError:
            print("reset")
    start_or_over_screen()
    while running:
        try:
            sound_sword = pygame.mixer.Sound("datafiles/sound_fite.mp3")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pl.cur_frame >= 2:
                        pl.cur_frame = 0
                    attack = [True, 0]
                    sound_sword.play()
                    print("attack")
                    pl.update_attack()
                    for i in evil_sprites:
                        if abs(i.rect.x - pl.rect.x) <= 60:
                            i.hp -= 5
                key = pygame.key.get_pressed()

                if key[pygame.K_a] or key[pygame.K_d]:
                    sound_hod.play(-1)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        sound_hod.stop()
            key = pygame.key.get_pressed()

            if key[pygame.K_1]:
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
            if key[pygame.K_d]:
                pl.update_hod("r")
                otr = False
            if key[pygame.K_a]:
                pl.update_hod("l")
                otr = True
            if key[pygame.K_SPACE] and flag_jumping:
                pl.rect.y -= 80
                flag_jumping = False
            if attack[0] and attack[1] <= 2:
                pl.update_attack()
                attack[1] += 1
            else:
                attack = [False, 0]
            if key[pygame.K_e]:
                if inventory["healme5"] > 0:
                    pl.hp += 5
                    inventory["healme5"] -= 1
            screen.blit(pygame.image.load("datafiles/map1.png"), (0, 0))
            all_sprites.update()
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
            if flag_is_dying:
                start_or_over_screen()
            evil_sprites.draw(screen)
            evil_sprites.update()
            gui.update()
            pl.update()
            if torg_in_map:
                torg.update()
            if fand_torg:
                gui_t.update()
            player_sprites.draw(screen)
            if pl.rect.x > 1280:
                if maps == "map1":
                    maps = "map0"
                else:
                    maps = "map1"
                break
            pygame.display.flip()
            clock.tick(10)
        except IndexError:
            pl.cur_frame = 0
            print("Ошибка анимации")
write_res()
