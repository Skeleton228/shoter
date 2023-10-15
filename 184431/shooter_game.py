#Создай собственный Шутер!

from pygame import *
from random import *
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('wall.jpg'),(win_width, win_height))
display.set_caption('Shooter')
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a]and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d]and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bull.png', self.rect.centerx, self.rect.top , 15, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            global lost
            lost += 1
            self.rect.x = randint(0, win_width - 80)
            self.rect.y = 0
            self.speed = randint(1,5)
monsters = sprite.Group()

class Asteroed(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_width - 80)
            self.rect.y = 0
            self.speed = randint(1,5)
Asteroeds = sprite.Group()
for i in range(2):
    asteroed = Asteroed('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    Asteroeds.add(asteroed)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy('pngwing.com.png', randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
global score
score = 0
global lost
lost = 0
font.init()
font1 = font.Font(None, 36)
fire_shooter = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60
life = 3
game = True
Finish = False
ship = Player('sprite.png', 5, win_height - 100, 80, 100, 10)
num_fire = 0
rel_time = False
import time as t
while game:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            run = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            if rel_time == False:
                fire_shooter.play()
                ship.fire()
                num_fire += 1

            if num_fire >= 5 and rel_time == False:
                last_time = t.time()
                rel_time = True

    if not Finish:
        #обновляем фон
        window.blit(background,(0,0))
        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        
        Asteroeds.draw(window)
        Asteroeds.update()

        bullets.update()
        bullets.draw(window)

        text_score = font1.render('Уничтожено: ' + str(score), True, (255,255,255))
        window.blit(text_score, (10, 20))
        
        text_lost = font1.render('Пропущено: ' + str(lost), True, (255,255,255))
        window.blit(text_lost, (10, 50))
        
        text_health = font1.render("Жизни: " + str(life), 1, (255, 255, 255))
        window.blit(text_health, (win_width - 150, 20))
        
        text_fire = font1.render("Патроны: " + str(5 - num_fire), 1, (255, 255, 255))
        window.blit(text_fire, (win_width - 150, 50))
        

        #перезарядка
        if rel_time == True:
            now_time = t.time() #считываем время
            if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезарядке
                reload = font1.render('Перезарядка' + '.' * (1 + int(now_time - last_time)), 1, (255, 255, 255))
                window.blit(reload, (win_width/3, win_height-50))
            else:
                num_fire = 0   #обнуляем счётчик пуль
                rel_time = False #сбрасываем флаг перезарядки

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('pngwing.com.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if score >= 10:
            finish = True
            #finish_sound = mixer.Sound('win.mp3')
            mixer.music.pause()
            #finish_sound.play()
            finish_image = transform.scale(image.load('win.png'), (win_width, win_height))
        if lost >= 3 or life <= 0:
            finish = True
            #finish_sound = mixer.Sound('lose.mp3')
            mixer.music.pause()
            #finish_sound.play()
            finish_image = transform.scale(image.load('lose.jpg'), (win_width, win_height))
        
        sprite.spritecollide(asteroed, bullets, True)

        for ast in Asteroeds:
            if ship.rect.colliderect(ast.rect):
                ast.kill()
                life -= 1
                asteroed = Asteroed('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
                Asteroeds.add(asteroed)
        
    
    else:
        window.blit(finish_image, (0, 0))

    display.update()
    clock.tick(60)