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

# 定义网格大小
GRID_SIZE = 50
GRID_WIDTH = 800 // GRID_SIZE
GRID_HEIGHT = 600 // GRID_SIZE

# 植物类
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE - 4, GRID_SIZE - 4))  # 减小植物大小以增加间距
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x + 2, y + 2)  # 调整位置以保持居中
        self.last_shot_time = pygame.time.get_ticks()
        self.health = 100  # 植物的生命值
    
    def update(self):
        # 每秒发射一颗子弹
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 1000:
            bullet = Bullet(self.rect.right, self.rect.centery)
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
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
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

# 创建植物组
plants = pygame.sprite.Group()

# 创建僵尸组
zombies = pygame.sprite.Group()
for i in range(5):
    zombie = Zombie(random.randint(800, 1600), random.choice([i * GRID_SIZE for i in range(GRID_HEIGHT)]))
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 获取鼠标点击位置
            mouse_x, mouse_y = event.pos
            # 计算点击的网格坐标
            grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
            grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
            # 检查该位置是否已有植物
            if not any(plant.rect.collidepoint(grid_x + 2, grid_y + 2) for plant in plants):
                plant = Plant(grid_x, grid_y)
                plants.add(plant)

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
            zombie.attack(pygame.sprite.spritecollideany(zombie, plants))
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
