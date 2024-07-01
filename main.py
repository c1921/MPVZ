import pygame
import sys
import time

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width = 400
screen_height = 250
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# 设置网格大小
cols = 10
rows = 6
cell_width = screen_width // cols
cell_height = (screen_height - 50) // rows  # 减去顶部植物栏的高度

# 植物类
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((cell_width, cell_height))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.last_shot = time.time()
    
    def update(self):
        # 每秒发射一个子弹
        if time.time() - self.last_shot >= 1:
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_shot = time.time()

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(white)
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
        for zombie in hit_zombies:
            zombie.take_damage(self.damage)
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
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
    
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
        self.image.blit(self.peashooter_icon, (10, 10))

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

def main():
    clock = pygame.time.Clock()
    running = True
    plant_selected = False
    zombie_spawn_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < 50:  # 点击植物栏
                    plant_selected = True
                elif plant_selected:
                    col = x // cell_width
                    row = (y - 50) // cell_height
                    plant = Plant(col * cell_width, 50 + row * cell_height)
                    all_sprites.add(plant)
                    plants.add(plant)
                    plant_selected = False

        # 生成僵尸
        if time.time() - zombie_spawn_time >= 3:
            zombie = Zombie(screen_width, 50 + (cell_height * (rows - 1)))
            all_sprites.add(zombie)
            zombies.add(zombie)
            zombie_spawn_time = time.time()

        screen.fill(black)
        draw_grid()
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
