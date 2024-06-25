import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((800, 600))

# 定义颜色
WHITE = (40, 40, 40)
GREEN = (0, 27, 0)
RED = (40, 0, 0)
BLACK = (0, 0, 0)

# 定义字体
font = pygame.font.SysFont(None, 75)

# 植物类
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_shot_time = pygame.time.get_ticks()
        self.health = 100  # 植物的生命值
    
    def update(self):
        # 每秒发射一颗子弹
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 1000:
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            bullets.add(bullet)
            self.last_shot_time = current_time
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        self.rect.x += 5
        if self.rect.left > 800:
            self.kill()

# 僵尸类
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
        self.health = 100  # 僵尸的生命值
        self.attacking = False
        self.last_attack_time = pygame.time.get_ticks()
    
    def update(self):
        if not self.attacking:
            self.rect.x -= self.speed
        if self.rect.right < 0:
            global running
            running = False
        if self.rect.right < 0:
            self.kill()
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
    
    def attack(self, plant):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > 500:  # 每秒攻击2次
            plant.take_damage(20)
            self.last_attack_time = current_time

# 创建植物实例
plant = Plant(100, 300)
plants = pygame.sprite.Group(plant)

# 创建僵尸组
zombies = pygame.sprite.Group()
for i in range(15):
    zombie = Zombie(random.randint(800, 1600), 300)
    zombies.add(zombie)

# 创建子弹组
bullets = pygame.sprite.Group()

# 主循环
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新
    plants.update()
    bullets.update()
    zombies.update()

    # 检查子弹与僵尸的碰撞
    collisions = pygame.sprite.groupcollide(bullets, zombies, True, False)
    for bullet, hit_zombies in collisions.items():
        for zombie in hit_zombies:
            zombie.take_damage(20)

    # 检查僵尸与植物的碰撞
    for zombie in zombies:
        if pygame.sprite.spritecollideany(zombie, plants):
            zombie.attacking = True
            zombie.attack(plant)
        else:
            zombie.attacking = False

    # 绘制
    screen.fill(BLACK)
    plants.draw(screen)
    bullets.draw(screen)
    zombies.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# 显示失败信息
screen.fill(BLACK)
text = font.render("Failed", True, WHITE)
screen.blit(text, (300, 250))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
