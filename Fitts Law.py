import pygame
import sys
import random
import time
import openpyxl
#Open AI API Key: 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
# Pygame initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800  # Adjusted window size
FPS = 60

# Colors
BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (20, 57, 255)
NEON_PURPLE = (128, 0, 128)

# Task parameters
sizes = [10, 20, 40, 60]
distances = [100, 200, 300, 400]
positions = ['left', 'right']

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fitts' Law Game")
clock = pygame.time.Clock()

# Fonts
consent_font = pygame.font.Font(None, 36)
countdown_font = pygame.font.Font(None, 48)
progress_font = pygame.font.Font(None, 24)

# Sounds
hit_sound = pygame.mixer.Sound("hit_sound.mp3")
miss_sound = pygame.mixer.Sound("miss_sound.mp3")
game_complete_sound = pygame.mixer.Sound("game_complete_sound.mp3")

# Informed Consent Form
consent_text = "I agree to participate in the Fitts' Law game. Press Space to continue."
consent_rendered = consent_font.render(consent_text, True, NEON_GREEN)

# Countdown
countdown = 3

# Game state
consent_given = False
game_active = False
pause = False

# Progress bar
progress = 0
progress_increment = 8  # 32 tasks / 4 tasks per increment

# Data collection
data = []

# Main game loop
running = True
while running:
    task_completed = False  # Variable to track if the current task is completed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not consent_given and event.key == pygame.K_SPACE:
                consent_given = True
                game_active = True
            elif game_active and event.key == pygame.K_p:
                pause = not pause
                pygame.time.delay(500)  # Avoids multiple key presses during a single key press
        elif game_active and event.type == pygame.MOUSEBUTTONUP:
            # Check if the click is inside the circle
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 0 <= progress < 32 and not task_completed:  # Ensure progress is within valid range and task is not already completed
                circle_x = WIDTH // 2 + (distances[progress % 4] if positions[(progress // 8) % 2] == 'right' else -distances[progress % 4])
                circle_y = HEIGHT // 2
                size = sizes[progress // 8]

                distance_to_center = ((mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2) ** 0.5

                if distance_to_center <= size / 2:
                    hit_sound.play()
                    data.append([progress % progress_increment, size, distances[progress % 4], positions[(progress // 8) % 2], False, 0])
                    task_completed = True  # Set the flag to indicate task completion
                else:
                    miss_sound.play()
                    data.append([progress % progress_increment, size, distances[progress % 4], positions[(progress // 8) % 2], True, distance_to_center])

                    # Skip the next task in case of a miss
                    progress += 1

                # Check if all tasks are completed
                if progress == 32:
                    game_complete_sound.play()
                    game_active = False

    screen.fill(BLACK)

    if not consent_given:
        # Display Informed Consent Form
        screen.blit(consent_rendered, (50, HEIGHT // 2 - 50))
    else:
        if game_active:
            if not pause:
                if countdown > 0:
                    # Display countdown
                    countdown_rendered = countdown_font.render(str(countdown), True, NEON_BLUE)
                    screen.blit(countdown_rendered, (WIDTH // 2 - 20, HEIGHT // 2 - 20))
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    countdown -= 1
                else:
                    # Display task
                    if task_completed:  # Only proceed to the next task if the current task is completed
                        progress += 1
                        task_completed = False  # Reset the task completion flag

                    if progress % progress_increment == 0:
                        size = random.choice(sizes)
                        distance = random.choice(distances)
                        position = random.choice(positions)

                        circle_x = WIDTH // 2 + (distance if position == 'right' else -distance)
                        circle_y = HEIGHT // 2

                        pygame.draw.circle(screen, NEON_PURPLE, (circle_x, circle_y), size)

                        # Display progress bar
                        pygame.draw.rect(screen, NEON_GREEN, (0, 0, WIDTH * progress / 32, 10))

                        tasks_completed = progress % progress_increment

                        # Update progress text
                        progress_text = f"Task {tasks_completed}/4"
                        progress_rendered = progress_font.render(progress_text, True, NEON_GREEN)
                        screen.blit(progress_rendered, (WIDTH // 2 - 40, 10))

                        pygame.display.flip()

                        # Wait for a short time before clearing the screen
                        pygame.time.delay(500)

                # Clear the screen
                screen.fill(BLACK)

            else:
                # Display pause message
                pause_text = "Paused. Press 'P' to resume."
                pause_rendered = consent_font.render(pause_text, True, NEON_BLUE)
                screen.blit(pause_rendered, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

        else:
            # Display completion message
            completion_text = "Thank you for completing the Fitts' Law game!"
            completion_rendered = consent_font.render(completion_text, True, NEON_GREEN)
            screen.blit(completion_rendered, (50, HEIGHT // 2 - 50))

    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()

# Save data to Excel file
if data:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Task', 'Size', 'Distance', 'Position', 'Missed', 'Missed Distance'])

    for task_data in data:
        ws.append(task_data)

    wb.save('fitts_law_results.xlsx')