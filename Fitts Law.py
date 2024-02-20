import csv
from pygame.locals import *
import pygame, sys, math
import random

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

    def terminate_game(self):
        with open('data.csv', 'a', newline='') as csvfile:
            fieldnames = ['time_difference', 'distance', 'width']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            # Write data to CSV file
            for entry in self.data['fittslaw']:
                writer.writerow({
                'time_difference': entry.get('time_difference', 0),
                'distance': entry.get('distance', 0),
                'width': entry.get('width', 0)
            })

        pygame.quit()
        sys.exit()

    def run_experiment(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fitts' Law Experiment")
        clock = pygame.time.Clock()

        self.show_welcome_screen()

        if self.is_running:
            self.show_image_screen()
            
        start_time = 0
        while self.is_running:
            screen.fill(BLACK)
            self.targets.update()
            self.targets.draw(screen)
            pygame.display.flip()

            if self.succ_score >= 5:
                self.terminate_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate_game()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_target.rect.collidepoint(event.pos):
                        if start_time == 0:
                            start_time = pygame.time.get_ticks()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if start_time != 0:
                        end_time = pygame.time.get_ticks()
                        difftime = (end_time - start_time) / 1000
                        start_time = 0

                        self.succ_score += 1
                        dist = math.hypot(event.pos[0] - WIDTH/2, event.pos[1] - HEIGHT/2)

                        self.data['fittslaw'].append({
                            'start_time': round(start_time, 2),
                            'end_time': round(end_time, 2),
                            'time_difference': round(difftime, 2),
                            'distance': round(dist, 2),
                            'width': self.current_target.radius * 2
                        })

                        self.next_target()
                        print('Successful clicks:', self.succ_score, 'vs Unsuccessful clicks:', self.unsucc_score)

            clock.tick(FPS)

if __name__ == '__main__':
    experiment = FittsLawExperiment()
    experiment.run_experiment()
