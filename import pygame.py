import pygame
import random
import time

def initialize_game():
    global cards, selected_cards, start_time, cards_data, game_over
    cards = []
    selected_cards = []
    game_over = False
    start_time = time.time()
    random.shuffle(cards_data)
    for i, card_data in enumerate(cards_data):
        x = (i % cards_per_row) * (card_width + card_gap) + (screen_width - (cards_per_row * (card_width + card_gap))) / 2
        y = (i // cards_per_row) * (card_height + card_gap) + card_gap + 60
        card = card_data.copy()
        card['rect'] = pygame.Rect(x, y, card_width, card_height)
        card['revealed'] = False
        cards.append(card)

def draw_button(text, button_rect, text_color, button_color):
    pygame.draw.rect(screen, button_color, button_rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors and font
white = (255, 255, 255)
grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Game variables
num_pairs = 8
cards_per_row = 4
card_width = 120
card_height = 120
card_gap = 20
game_over = False
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 165, 0), (128, 0, 128)]
cards_data = [{'color': colors[i // 2], 'id': i // 2} for i in range(num_pairs * 2)]

# Sound (assuming 'pairSound.wav' exists)
match_sound = pygame.mixer.Sound("pairSound.wav")

font = pygame.font.Font(None, 36)
reset_button = pygame.Rect(650, 10, 140, 40)
play_again_button = pygame.Rect(screen_width // 2 - 70, screen_height // 2 + 20, 140, 40)

# Initialize game state
initialize_game()

clock = pygame.time.Clock()
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if play_again_button.collidepoint(event.pos):
                    initialize_game()
            else:
                if reset_button.collidepoint(event.pos):
                    initialize_game()
                elif len(selected_cards) < 2:
                    for card in cards:
                        if card['rect'].collidepoint(event.pos) and not card['revealed']:
                            card['revealed'] = True
                            selected_cards.append(card)
                            if len(selected_cards) == 2:
                                screen.fill(white)
                                for card in cards:
                                    pygame.draw.rect(screen, card['color'] if card['revealed'] else grey, card['rect'])
                                pygame.display.flip()
                                pygame.time.wait(500)
                                if selected_cards[0]['id'] == selected_cards[1]['id']:
                                    match_sound.play()
                                    cards = [card for card in cards if card not in selected_cards]
                                else:
                                    for selected_card in selected_cards:
                                        selected_card['revealed'] = False
                                selected_cards = []

    screen.fill(white)

    for card in cards:
        pygame.draw.rect(screen, card['color'] if card['revealed'] else grey, card['rect'])

    if len(cards) == 0:
        game_over = True
        message = font.render("Well done!", True, green)
        screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2 - 20))
        draw_button("Play again", play_again_button, white, red)
    else:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, black)
        screen.blit(timer_text, (screen_width // 2 - 50, 20))
        draw_button("Reset", reset_button, white, red)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
