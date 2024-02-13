from pygame.locals import *
import pygame, sys, math
import random
import time
import json
import datetime

# Constants needed for the game to run 
WIDTH, HEIGHT = 800, 800
FPS = 60
NEON_PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, NEON_PURPLE, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = radius

    def update(self):
        pass

class FittsLawExperiment:
    def __init__(self):
        self.data = {'fittslaw': []}
        self.succ_score = 0
        self.unsucc_score = 0
        self.targets = pygame.sprite.Group()
        self.current_target = None
        self.is_running = False
        self.next_target()
        self.show_welcome_screen()

    def show_welcome_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font = pygame.font.Font(None, 36)
        text = font.render("Welcome to the Fitts' Law Experiment", True, NEON_PURPLE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        button = pygame.Rect(WIDTH/2 - 50, HEIGHT/2 + 50, 300, 50)
        button_text = font.render("Let's Begin the fun game", True, GOLD)
        button_text_rect = button_text.get_rect(center=button.center)

        clock = pygame.time.Clock()
        while True:
            screen.fill(BLACK)
            screen.blit(text, text_rect)
            pygame.draw.rect(screen, NEON_PURPLE, button)
            screen.blit(button_text, button_text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button.collidepoint(event.pos):
                        self.is_running = True
                        return

            clock.tick(FPS)

    def show_image_screen(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        image = pygame.image.load("informedConsent.png") 
        image_rect = image.get_rect(center=(WIDTH/2, HEIGHT/2))
        button = pygame.Rect(WIDTH/2 - 50, HEIGHT - 100, 400, 50)
        font = pygame.font.Font(None, 36)
        button_text = font.render("i agree to sell you my data", True, BLACK)
        button_text_rect = button_text.get_rect(center=button.center)

        clock = pygame.time.Clock()
        while True:
            screen.fill(BLACK)
            screen.blit(image, image_rect)
            pygame.draw.rect(screen, NEON_PURPLE, button)
            screen.blit(button_text, button_text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button.collidepoint(event.pos):
                        return

            clock.tick(FPS)

    def next_target(self):
        if self.current_target:
            self.current_target.kill()

        radius = random.choice([10, 20, 40, 60])
        x, y = random.choice([(0, HEIGHT/2), (100, HEIGHT/2), (200, HEIGHT/2), (300, HEIGHT/2), (500, HEIGHT/2), (600, HEIGHT/2), (700, HEIGHT/2), (800, HEIGHT/2)])
        self.current_target = Target(x, y, radius)
        self.targets.add(self.current_target)

    def run_experiment(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fitts' Law Experiment")
        clock = pygame.time.Clock()

        self.show_welcome_screen()

        if self.is_running:
            self.show_image_screen()

        start_time = None
        while self.is_running:
            screen.fill(BLACK)
            self.targets.update()
            self.targets.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open('data.json', 'a') as outfile:  # Open in append mode ('a') instead of write mode ('w')
                        json.dump(self.data, outfile)
                        outfile.write('\n')  # Add a newline character to separate each appended entry
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_target.rect.collidepoint(event.pos):
                        if not start_time:
                            start_time = datetime.datetime.now()

                        difftime = datetime.datetime.now() - start_time
                        self.succ_score += 1

                        dist = math.hypot(event.pos[0] - WIDTH/2, event.pos[1] - HEIGHT/2)
                        self.data['fittslaw'].append({
                            'time': difftime.microseconds,
                            'distance': dist,
                            'width': self.current_target.radius * 2
                        })

                        self.next_target()
                        print('Successful clicks:', self.succ_score, 'vs Unsuccessful clicks:', self.unsucc_score)

                elif event.type == pygame.MOUSEBUTTONUP:
                    start_time = None

            clock.tick(FPS)

if __name__ == '__main__':
    experiment = FittsLawExperiment()
    experiment.run_experiment()
