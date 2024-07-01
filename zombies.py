import pygame
import time

# 设置颜色
red = (255, 0, 0)
grey = (128, 128, 128)
dark_grey = (64, 64, 64)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, health, color, plants):
        super().__init__()
        self.image = pygame.Surface((40, 40))  # 设置大小为40x40
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = health
        self.speed = 1
        self.frame_count = 0  # 添加一个帧计数器
        self.last_attack_time = time.time()
        self.plants = plants
        self.ice_effect_start_time = None
        self.original_frame_interval = 3  # 原始的移动帧数间隔
        self.current_frame_interval = self.original_frame_interval

    def update(self):
        self.frame_count += 1
        if self.frame_count % self.current_frame_interval == 0:  # 使用当前帧数间隔
            if not pygame.sprite.spritecollideany(self, self.plants):
                self.rect.x -= self.speed
        # 检查与植物的碰撞
        hit_plants = pygame.sprite.spritecollide(self, self.plants, False)
        if hit_plants:
            if time.time() - self.last_attack_time >= 1/6:
                for plant in hit_plants:
                    plant.health -= 20
                self.last_attack_time = time.time()

        # 检查寒冰效果
        if self.ice_effect_start_time and time.time() - self.ice_effect_start_time > 3:
            self.current_frame_interval = self.original_frame_interval
            self.ice_effect_start_time = None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def apply_ice_effect(self, duration):
        self.current_frame_interval = self.original_frame_interval * 2  # 将移动帧数间隔加倍
        self.ice_effect_start_time = time.time()  # 重置寒冰效果开始时间

class RegularZombie(Zombie):
    def __init__(self, x, y, plants):
        super().__init__(x, y, 100, red, plants)

class ConeheadZombie(Zombie):
    def __init__(self, x, y, plants):
        super().__init__(x, y, 250, grey, plants)

class BucketheadZombie(Zombie):
    def __init__(self, x, y, plants):
        super().__init__(x, y, 500, dark_grey, plants)
