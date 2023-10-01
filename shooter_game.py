#Создай собственный Шутер!

from pygame import *
from random import *
 
lost = 0
win = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 7, 20, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global win
        if self.rect.y >= win_height:
            self.rect.x = randint(0, 600)
            self.rect.y = 0
            lost += 1
        if sprite.groupcollide(enemys, bullets, True, True):
            enemy = Enemy('ufo.png', randint(0, 650), 0, 2, 65, 65)
            enemys.add(enemy)
            enemy.rect.x = randint(0, 650)
            enemy.rect.y = 0
            win += 1
        if sprite.spritecollide(hero, asteroids, False):
            asteroid = Enemy('asteroid.png', randint(0, 650), 0, 2, 65, 65)
            asteroids.add(asteroid)
            asteroid.rect.x = randint(0, 650)
            asteroid.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

hero = Player('rocket.png', 320, 400, 7, 65, 65)

enemys = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(0, 620), 0, randint(1, 3), 65, 65)
    enemys.add(enemy)
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0, 620), 0, randint(1, 3), 65, 65)
    asteroids.add(asteroid)

bullets = sprite.Group()

font.init()
font_1 = font.SysFont('Arial', 30)
font_2 = font.SysFont('Arial', 65)
text_lose = font_1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
text_win = font_1.render('Счёт:' + str(win), 1, (255,255,255))

run = True
finish = False 
clock = time.Clock()
FPS = 60
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
    if finish != True:
        window.blit(background, (0,0))
        hero.reset()
        hero.update()

        text_lose = font_1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_win = font_1.render('Счёт:' + str(win), 1, (255,255,255))
        enemys.draw(window)
        enemys.update()

        bullets.draw(window)
        bullets.update()

        asteroids.draw(window)
        asteroids.update()

        window.blit(text_lose, (0, 25))
        window.blit(text_win, (0, 0))

        if win >= 10:
            winer = font_2.render('Победа!', True, (0, 255, 0))
            window.blit(winer, (270, 250))
            finish = True
        if sprite.spritecollide(hero, enemys, False) or lost >= 3:
            loser = font_2.render('Проигрышь!', True, (255, 0, 0))
            window.blit(loser, (240, 250))
            finish = True
        if sprite.spritecollide(hero, asteroids, False):
            loser = font_2.render('Проигрышь!', True, (255, 0, 0))
            window.blit(loser, (240, 250))
            finish = True
    else:
        time.delay(5000)
        for bullet in bullets:
            bullet.kill()
        for enemy in enemys:
            enemy.kill()
        for asteroid in asteroids:
            asteroid.kill()
        lost = 0
        win = 0
        finish = False
        for i in range(5):
            enemy = Enemy('ufo.png', randint(0, 620), 0, randint(1, 3), 65, 65)
            enemys.add(enemy)
        for i in range(3):
            asteroid = Enemy('asteroid.png', randint(0, 620), 0, randint(1, 3), 65, 65)
            asteroids.add(asteroid)
    
    display.update()
    clock.tick(FPS)