import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def main():
    pygame.init()
    size = width, height = 600, 300
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    car_image = load_image("gameover.png")
    car = pygame.sprite.Sprite(all_sprites)
    car.image = car_image
    car.rect = car_image.get_rect()
    car.rect.x = 600
    pygame.mouse.set_visible(False)
    running = True
    dist = 10
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if car.rect.x == 0:
            dist = 0
        screen.fill("blue")
        car.rect.left += dist
        clock.tick(55)
        all_sprites.draw(screen)
        pygame.display.flip()


main()
