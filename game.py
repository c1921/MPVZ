import pygame
import time
import random
from plants import Peashooter, WallNut, CherryBomb, IceShooter
from zombies import RegularZombie, ConeheadZombie, BucketheadZombie
from utils import draw_grid

# 初始化精灵组
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
plants = pygame.sprite.Group()
zombies = pygame.sprite.Group()

# 设置屏幕大小
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
brown = (139, 69, 19)
red = (255, 0, 0)
blue = (0, 0, 255)

# 设置网格大小
cols = 10
rows = 6
cell_width = screen_width // cols
cell_height = (screen_height - 50) // rows  # 减去顶部植物栏的高度

class PlantBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((screen_width, 50))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.peashooter_icon = pygame.Surface((cell_width, cell_height))
        self.peashooter_icon.fill(green)
        self.wallnut_icon = pygame.Surface((cell_width, cell_height))
        self.wallnut_icon.fill(brown)
        self.cherrybomb_icon = pygame.Surface((cell_width, cell_height))
        self.cherrybomb_icon.fill(red)
        self.iceshooter_icon = pygame.Surface((cell_width, cell_height))
        self.iceshooter_icon.fill(blue)
        self.image.blit(self.peashooter_icon, (10, 10))
        self.image.blit(self.wallnut_icon, (cell_width + 20, 10))
        self.image.blit(self.cherrybomb_icon, (2 * cell_width + 30, 10))
        self.image.blit(self.iceshooter_icon, (3 * cell_width + 40, 10))

# 创建植物栏
plant_bar = PlantBar()
all_sprites.add(plant_bar)

# 计数器，用于跟踪spawn_zombies的调用次数
zombie_spawn_count = 0

def spawn_zombies(amount):
    global zombie_spawn_count
    if zombie_spawn_count >= 100:
        return
    for _ in range(amount):
        row = random.randint(0, rows - 1)
        zombie_type = random.choice([RegularZombie, ConeheadZombie, BucketheadZombie])
        zombie = zombie_type(screen_width, 50 + row * cell_height, plants)
        all_sprites.add(zombie)
        zombies.add(zombie)
    zombie_spawn_count += 1

def game_loop():
    global zombie_spawn_count
    # 重置计数器和精灵组
    zombie_spawn_count = 0
    all_sprites.empty()
    bullets.empty()
    plants.empty()
    zombies.empty()
    all_sprites.add(plant_bar)

    clock = pygame.time.Clock()
    running = True
    plant_selected = None
    start_time = time.time()
    zombie_spawn_interval = 3  # 初始僵尸生成间隔（秒）
    last_zombie_spawn_time = time.time()
    last_horde_spawn_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < 50:  # 点击植物栏
                    if x < cell_width + 10:
                        plant_selected = Peashooter
                    elif x < 2 * cell_width + 20:
                        plant_selected = WallNut
                    elif x < 3 * cell_width + 30:
                        plant_selected = CherryBomb
                    elif x < 4 * cell_width + 40:
                        plant_selected = IceShooter
                elif plant_selected:
                    col = x // cell_width
                    row = (y - 50) // cell_height
                    if plant_selected == Peashooter:
                        plant = plant_selected(col * cell_width, 50 + row * cell_height, all_sprites, bullets, zombies)
                    elif plant_selected == CherryBomb:
                        plant = plant_selected(col * cell_width, 50 + row * cell_height, all_sprites, zombies, cell_width, cell_height)
                    elif plant_selected == IceShooter:
                        plant = plant_selected(col * cell_width, 50 + row * cell_height, all_sprites, bullets, zombies)
                    else:
                        plant = plant_selected(col * cell_width, 50 + row * cell_height)
                    all_sprites.add(plant)
                    plants.add(plant)
                    plant_selected = None

        # 动态调整僵尸生成频率
        elapsed_time = time.time() - start_time
        if elapsed_time > 30:  # 每经过30秒，增加僵尸生成频率
            zombie_spawn_interval = max(0.5, 3 - (elapsed_time // 30) * 0.5)  # 最低间隔为0.5秒

        # 生成普通僵尸
        if time.time() - last_zombie_spawn_time >= zombie_spawn_interval:
            spawn_zombies(1)
            last_zombie_spawn_time = time.time()

        # 每隔1分钟生成大量僵尸
        if time.time() - last_horde_spawn_time >= 60:
            spawn_zombies(10)  # 生成10个僵尸
            last_horde_spawn_time = time.time()

        screen.fill(black)
        draw_grid(screen, cols, rows, cell_width, cell_height)
        all_sprites.update()
        all_sprites.draw(screen)

        # 检查是否有僵尸移动到最左边
        for zombie in zombies:
            if zombie.rect.right <= 0:
                return "Game Over"

        # 检查胜利条件
        if zombie_spawn_count >= 100 and len(zombies) == 0:
            return "You Win!"

        pygame.display.flip()
        clock.tick(60)
