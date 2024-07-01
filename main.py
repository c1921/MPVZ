import pygame
import sys
import time
import random

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width = 400
screen_height = 250
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)
green = (0, 255, 0)
brown = (139, 69, 19)
red = (255, 0, 0)

# 设置网格大小
cols = 10
rows = 6
cell_width = screen_width // cols
cell_height = (screen_height - 50) // rows  # 减去顶部植物栏的高度

# 定义植物类
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y, health, color):
        super().__init__()
        self.image = pygame.Surface((cell_width, cell_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = health

    def update(self):
        if self.health <= 0:
            self.kill()

class Peashooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, 100, green)
        self.last_shot = time.time()
    
    def update(self):
        super().update()
        if time.time() - self.last_shot >= 1:
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_shot = time.time()

class WallNut(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, 10000, brown)

class CherryBomb(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, 10000, red)
        self.plant_time = time.time()
    
    def update(self):
        super().update()
        if time.time() - self.plant_time >= 0.5:
            self.explode()
    
    def explode(self):
        # 计算3x3范围
        for zombie in zombies:
            if abs(zombie.rect.centerx - self.rect.centerx) <= 1.5 * cell_width and abs(zombie.rect.centery - self.rect.centery) <= 1.5 * cell_height:
                zombie.take_damage(10000)
        self.kill()

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(grey)  # 设置子弹颜色为灰色
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.damage = 20
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.left > screen_width:
            self.kill()
        # 检查与僵尸的碰撞
        hit_zombies = pygame.sprite.spritecollide(self, zombies, False)
        if hit_zombies:
            # 找到最左边的僵尸
            leftmost_zombie = min(hit_zombies, key=lambda z: z.rect.x)
            leftmost_zombie.take_damage(self.damage)
            self.kill()

# 僵尸类
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((cell_width, cell_height))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100
        self.speed = 1
        self.frame_count = 0  # 添加一个帧计数器
        self.last_attack_time = time.time()
    
    def update(self):
        self.frame_count += 1
        if self.frame_count % 3 == 0:  # 每3帧移动1像素
            if not pygame.sprite.spritecollideany(self, plants):
                self.rect.x -= self.speed
        # 检查与植物的碰撞
        hit_plants = pygame.sprite.spritecollide(self, plants, False)
        if hit_plants:
            # 每秒攻击6次
            if time.time() - self.last_attack_time >= 1/6:
                for plant in hit_plants:
                    plant.health -= 20
                self.last_attack_time = time.time()
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

# 植物栏类
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
        self.image.blit(self.peashooter_icon, (10, 10))
        self.image.blit(self.wallnut_icon, (cell_width + 20, 10))
        self.image.blit(self.cherrybomb_icon, (2 * cell_width + 30, 10))

def draw_grid():
    for col in range(cols):
        for row in range(rows):
            rect = pygame.Rect(col * cell_width, 50 + row * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, white, rect, 1)

# 初始化精灵组
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
plants = pygame.sprite.Group()
zombies = pygame.sprite.Group()

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
        zombie = Zombie(screen_width, 50 + row * cell_height)
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
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < 50:  # 点击植物栏
                    if x < cell_width + 10:
                        plant_selected = Peashooter
                    elif x < 2 * cell_width + 20:
                        plant_selected = WallNut
                    elif x < 3 * cell_width + 30:
                        plant_selected = CherryBomb
                elif plant_selected:
                    col = x // cell_width
                    row = (y - 50) // cell_height
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
        draw_grid()
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

def main_menu():
    font = pygame.font.Font(None, 36)
    while True:
        screen.fill(black)
        text = font.render("Press SPACE to Start", True, white)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def main():
    while True:
        main_menu()
        result = game_loop()
        font = pygame.font.Font(None, 36)
        while True:
            screen.fill(black)
            text = font.render(result, True, white)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
            text = font.render("Press SPACE to Return to Main Menu", True, white)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2 + 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        break
            else:
                continue
            break

if __name__ == "__main__":
    main()
