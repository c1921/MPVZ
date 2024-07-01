import pygame
import time

# 设置颜色
green = (0, 255, 0)
brown = (139, 69, 19)
red = (255, 0, 0)
grey = (128, 128, 128)
blue = (0, 0, 255)

class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y, health, color):
        super().__init__()
        self.image = pygame.Surface((40, 40))  # 设置大小为40x40
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = health

    def update(self):
        if self.health <= 0:
            self.kill()

class Peashooter(Plant):
    def __init__(self, x, y, all_sprites, bullets, zombies):
        super().__init__(x, y, 100, green)
        self.last_shot = time.time()
        self.all_sprites = all_sprites
        self.bullets = bullets
        self.zombies = zombies
    
    def update(self):
        super().update()
        # 检查是否有僵尸在同一行且在其右侧
        for zombie in self.zombies:
            if zombie.rect.y == self.rect.y and zombie.rect.x > self.rect.x:
                if time.time() - self.last_shot >= 1:
                    bullet = Bullet(self.rect.right, self.rect.centery, self.zombies)
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
                    self.last_shot = time.time()
                break

class WallNut(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, 10000, brown)

class CherryBomb(Plant):
    def __init__(self, x, y, all_sprites, zombies, cell_width, cell_height):
        super().__init__(x, y, 10000, red)
        self.plant_time = time.time()
        self.all_sprites = all_sprites
        self.zombies = zombies
        self.cell_width = cell_width
        self.cell_height = cell_height
    
    def update(self):
        super().update()
        if time.time() - self.plant_time >= 0.5:
            self.explode()
    
    def explode(self):
        for zombie in self.zombies:
            if abs(zombie.rect.centerx - self.rect.centerx) <= 1.5 * self.cell_width and abs(zombie.rect.centery - self.rect.centery) <= 1.5 * self.cell_height:
                zombie.take_damage(10000)
        self.kill()

class IceShooter(Plant):
    def __init__(self, x, y, all_sprites, bullets, zombies):
        super().__init__(x, y, 100, blue)
        self.last_shot = time.time()
        self.all_sprites = all_sprites
        self.bullets = bullets
        self.zombies = zombies
    
    def update(self):
        super().update()
        # 检查是否有僵尸在同一行且在其右侧
        for zombie in self.zombies:
            if zombie.rect.y == self.rect.y and zombie.rect.x > self.rect.x:
                if time.time() - self.last_shot >= 1:
                    bullet = IceBullet(self.rect.right, self.rect.centery, self.zombies)
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
                    self.last_shot = time.time()
                break

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, zombies):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(grey)  # 设置子弹颜色为灰色
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.damage = 20
        self.zombies = zombies
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.left > 400:  # 根据具体情况调整
            self.kill()
        hit_zombies = pygame.sprite.spritecollide(self, self.zombies, False)
        if hit_zombies:
            leftmost_zombie = min(hit_zombies, key=lambda z: z.rect.x)
            leftmost_zombie.take_damage(self.damage)
            self.kill()

class IceBullet(Bullet):
    def __init__(self, x, y, zombies):
        super().__init__(x, y, zombies)
        self.image.fill(blue)  # 设置寒冰子弹颜色为蓝色
        self.slow_duration = 3  # 减速持续时间3秒
    
    def update(self):
        super().update()
        hit_zombies = pygame.sprite.spritecollide(self, self.zombies, False)
        if hit_zombies:
            leftmost_zombie = min(hit_zombies, key=lambda z: z.rect.x)
            leftmost_zombie.take_damage(self.damage)
            leftmost_zombie.apply_ice_effect(self.slow_duration)
            self.kill()
