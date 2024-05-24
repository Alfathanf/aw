#==========================================================IMOORT LIBRARY==============================================================
import pygame
from pygame.locals import *
from random import randint

pygame.init()
pygame.display.set_caption('Dennis vs Bang Jarwo')
pygame.mixer.init()

#=========================================================LAGU======================================================================

pygame.mixer.music.load("aset/sound/BGM.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1, 0.0)

#==========================================================GAME==============================================================
class Game:
    def __init__(self):
        self.width = 1500
        self.height = 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.jarwo_timer = 100
        self.jarwo = []
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.keys = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False
        }
        
        self.player = Player(100, 375)
        self.load_assets()

    def load_assets(self):
        self.gambarplayer = pygame.image.load("aset/gambar/Dennis.png")
        self.background = pygame.image.load("aset/gambar/bg.jpeg")
        self.gambarjarwo = pygame.image.load("aset/gambar/jarwo.png")
        self.tombolreplay = pygame.image.load("aset/gambar/replay.png")
        self.hitsound = pygame.mixer.Sound("aset/sound/tolongin.mp3")
        self.hitsound.set_volume(0.5)

    def reset_game(self):
        self.player.reset_position(100, 375)
        self.jarwo = []
        self.score = 0
        self.jarwo_timer = 100
        self.game_over = False

    def draw_background(self):
        for x in range(int(self.width / self.background.get_width() + 1)):
            for y in range(int(self.height / self.background.get_height() + 1)):
                self.screen.blit(self.background, (x * 200, y * 200))

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (100, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_replay_button(self):
        replay_button_rect = self.tombolreplay.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(self.tombolreplay, replay_button_rect)
        return replay_button_rect

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.replay_button_rect.collidepoint(mouse_pos):
                        self.reset_game()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_w:
                        self.keys["top"] = True
                    elif event.key == K_a:
                        self.keys["left"] = True
                    elif event.key == K_s:
                        self.keys["bottom"] = True
                    elif event.key == K_d:
                        self.keys["right"] = True
                if event.type == pygame.KEYUP:
                    if event.key == K_w:
                        self.keys["top"] = False
                    elif event.key == K_a:
                        self.keys["left"] = False
                    elif event.key == K_s:
                        self.keys["bottom"] = False
                    elif event.key == K_d:
                        self.keys["right"] = False

    def update_enemies(self):
        self.jarwo_timer -= 1
        if self.jarwo_timer == 0:
            self.jarwo.append(Musuh(self.width, randint(50, self.height - 32)))
            self.jarwo_timer = randint(1, 25)

        for enemy in self.jarwo:
            enemy.move()
            if enemy.is_off_screen():
                self.jarwo.remove(enemy)

    def check_collisions(self):
        player_rect = self.player.get_rect(self.gambarplayer)
        for enemy in self.jarwo:
            enemy_rect = enemy.get_rect(self.gambarjarwo)
            if player_rect.colliderect(enemy_rect):
                self.hitsound.play() 
                self.game_over = True

    def run(self):
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update_enemies()
                self.player.move(self.keys, self.width, self.height, self.gambarplayer.get_height(), self.gambarplayer.get_width())
                self.check_collisions()
                self.score += 1

            self.screen.fill(0)
            self.draw_background()
            self.screen.blit(self.gambarplayer, self.player.position)
            for enemy in self.jarwo:
                self.screen.blit(self.gambarjarwo, enemy.position)
            self.draw_score()
            if self.game_over:
                self.replay_button_rect = self.draw_replay_button()
            pygame.display.flip()
            self.clock.tick(60)


        pygame.quit()

#==========================================================PLAYER==============================================================
class Player:
    def __init__(self, x, y):
        self.position = [x, y]

    def reset_position(self, x, y):
        self.position = [x, y]

    def move(self, keys, screen_width, screen_height, player_height, player_width):
        if keys["top"] and self.position[1] > 50:
            self.position[1] -= 5
        if keys["bottom"] and self.position[1] < screen_height - player_height:
            self.position[1] += 5
        if keys["left"] and self.position[0] > 0:
            self.position[0] -= 5
        if keys["right"] and self.position[0] < screen_width - player_width:
            self.position[0] += 5

    def get_rect(self, image):
        rect = pygame.Rect(image.get_rect())
        rect.topleft = self.position
        return rect

#==========================================================MUSUH==============================================================
class Musuh:
    def __init__(self, x, y):
        self.position = [x, y]

    def move(self):
        self.position[0] -= 13

    def is_off_screen(self):
        return self.position[0] < 0

    def get_rect(self, image):
        rect = pygame.Rect(image.get_rect())
        rect.topleft = self.position
        return rect


if __name__ == "__main__":
    game = Game()
    game.run()