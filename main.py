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
DARK_GRAY = (50, 50, 50)
HIGHLIGHT = (100, 100, 100)

# 定义字体
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 75)

# 定义网格大小
GRID_SIZE = 50
GRID_WIDTH = 12  # 网格列数
GRID_HEIGHT = 6  # 网格行数
PLANT_BAR_HEIGHT = 50  # 植物栏高度

# 初始费用
cost = 500
last_cost_update = pygame.time.get_ticks()

# 僵尸生成逻辑
zombie_death_count = 0
last_zombie_spawn_time = pygame.time.get_ticks()
phase = 1
zombie_spawn_interval_phase1 = 10000  # 一阶段：每10秒生成一个僵尸
zombie_spawn_interval_phase2 = 5000   # 二阶段：每5秒生成一个僵尸

# 当前选择的植物
selected_plant = None

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
    def __init__(self, x, y, speed=1):  # 增加一个speed参数，默认值为1
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed  # 设置僵尸的速度
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
            global zombie_death_count
            zombie_death_count += 1
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
            if mouse_y < PLANT_BAR_HEIGHT:
                # 点击植物栏
                if selected_plant == 'Peashooter':
                    selected_plant = None
                else:
                    selected_plant = 'Peashooter'
            elif event.button == 3:  # 右键单击
                selected_plant = None
            else:
                # 计算点击的网格坐标
                grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
                grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
                # 检查该位置是否已有植物并且是否选择了植物
                if selected_plant and cost >= 100 and not any(plant.rect.collidepoint(grid_x + 2, grid_y + 2) for plant in plants):
                    plant = Plant(grid_x, grid_y)
                    plants.add(plant)
                    cost -= 100  # 减少费用

    # 更新费用
    current_time = pygame.time.get_ticks()
    if current_time - last_cost_update > 10000:  # 每10秒增加25费用
        cost += 25
        last_cost_update = current_time

    # 更新僵尸生成逻辑
    if phase == 1 and zombie_death_count > 10:
        phase = 2

    if phase == 1:
        spawn_interval = zombie_spawn_interval_phase1
    else:
        spawn_interval = zombie_spawn_interval_phase2

    if current_time - last_zombie_spawn_time > spawn_interval:
        zombie = Zombie(800, random.choice([i * GRID_SIZE + PLANT_BAR_HEIGHT for i in range(GRID_HEIGHT)]), speed=1)
        zombies.add(zombie)
        last_zombie_spawn_time = current_time

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
    
    # 绘制植物栏
    for i in range(5):
        rect = pygame.Rect(i * GRID_SIZE, 0, GRID_SIZE, PLANT_BAR_HEIGHT)
        color = HIGHLIGHT if selected_plant == 'Peashooter' and i == 0 else DARK_GRAY
        pygame.draw.rect(screen, color, rect)
        if i == 0:
            plant_text = font.render("Peashooter", True, WHITE)
            screen.blit(plant_text, (i * GRID_SIZE + 5, 10))
    
    # 绘制网格
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE + PLANT_BAR_HEIGHT, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, DARK_GRAY, rect, 1)
    
    plants.draw(screen)
    bullets.draw(screen)
    zombies.draw(screen)

    # 绘制费用
    cost_text = font.render(f"Cost: {cost}", True, WHITE)
    screen.blit(cost_text, (10, PLANT_BAR_HEIGHT + 10))

    pygame.display.flip()
    clock.tick(60)

# 显示失败信息
screen.fill(BLACK)
text = large_font.render("Failed", True, WHITE)
screen.blit(text, (300, 250))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
