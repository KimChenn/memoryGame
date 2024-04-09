import pygame
import random
import time

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()
stage_index = 0
def initialize_game():
    global cards, selected_cards, start_time, cards_data, game_over, current_turn, player_scores, time_limit, time_attack_mode, stage_duration, stage_index
    cards = []
    selected_cards = []
    game_over = False
    current_turn = 1
    player_scores = [0, 0]
    start_time = time.time()
    time_limit = stage_duration[stage_index]
    random.shuffle(cards_data)
    for i, card_data in enumerate(cards_data):
        x = (i % cards_per_row) * (card_width + card_gap) + (screen_width - (cards_per_row * (card_width + card_gap) - card_gap)) / 2
        y = (i // cards_per_row) * (card_height + card_gap) + card_gap + 50
        card = card_data.copy()
        card['rect'] = pygame.Rect(x, y, card_width, card_height)
        card['revealed'] = False
        cards.append(card)
    if time_attack_mode:
        start_time = time.time()

def flip_card_animation(card, revealing):
    original_rect = card['rect'].copy()
    for width in list(range(card_width, 0, -10)) + list(range(0, card_width + 1, 10)):
        card['rect'].width = width
        if width > 0:
            card['rect'].centerx = original_rect.centerx
        screen.fill(white)
        
        for other_card in cards:
            if other_card == card and width <= 0 and revealing:
                pygame.draw.rect(screen, card['color'], other_card['rect'])
            else:
                if other_card['revealed'] or other_card == card:
                    pygame.draw.rect(screen, other_card['color'], other_card['rect'])
                else:
                    pygame.draw.rect(screen, grey, other_card['rect'])
        pygame.display.flip()
        pygame.time.wait(16)
    
    card['rect'] = original_rect

def draw_button(text, button_rect, text_color, button_color):
    pygame.draw.rect(screen, button_color, button_rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

def player_mode_buttons():
    draw_button("1 Player", one_player_button, black, green)
    draw_button("2 Players", two_player_button, black, red)
    draw_button("Time Attack", time_attack_button, black, blue)

def switch_turn():
    global current_turn
    current_turn = 2 if current_turn == 1 else 1

def announce_winner():
    winner = "1" if player_scores[0] > player_scores[1] else "2"
    winner_text = "It's a tie!" if player_scores[0] == player_scores[1] else f"Player {winner} wins!"
    winner_message = font.render(winner_text, True, black)
    screen.blit(winner_message, (screen_width // 2 - winner_message.get_width() // 2, screen_height // 2 + 100))

screen_width = 800
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
font = pygame.font.Font(None, 36)
match_sound = pygame.mixer.Sound("pairSound.wav")

num_pairs = 8
cards_per_row = 4
card_width = 120
card_height = 120
card_gap = 20
player_mode = 0
time_attack_mode = False
stage_duration = [60, 50, 40, 30, 20, 10]  # Duration for each stage in seconds
cards_data = [{'color': [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 165, 0), (128, 0, 128)][i // 2], 'id': i // 2} for i in range(num_pairs * 2)]

reset_button = pygame.Rect(650, 10, 140, 40)
play_again_button = pygame.Rect(screen_width // 2 - 70, screen_height - 100, 140, 40)
one_player_button = pygame.Rect(screen_width // 4 - 75, screen_height // 2 - 60, 150, 50)
two_player_button = pygame.Rect(screen_width * 3 // 4 - 75, screen_height // 2 - 60, 150, 50)
time_attack_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 60, 150, 50)

initialize_game()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if play_again_button.collidepoint(event.pos):
                    # This resets the game for any mode when "Play Again" is clicked.
                    initialize_game()
                    if time_attack_mode:
                        if 1 < remaining_time:
                            stage_index += 1
                            time_limit = stage_duration[stage_index]  # Ensure time attack mode starts with the default time limit
                        else:
                            stage_index = 0
                            time_limit = stage_duration[stage_index]
            elif player_mode == 0:
                if one_player_button.collidepoint(event.pos):
                    player_mode = 1
                    time_attack_mode = False  # Reset time attack mode off for one player
                    initialize_game()
                elif two_player_button.collidepoint(event.pos):
                    player_mode = 2
                    time_attack_mode = False  # Ensure time attack mode is off for two players
                    initialize_game()
                elif time_attack_button.collidepoint(event.pos):
                    player_mode = 1
                    time_attack_mode = True
                    initialize_game()
            elif reset_button.collidepoint(event.pos):
                initialize_game()
                if time_attack_mode:
                    time_limit = stage_duration[0]  # Reset to the current stage duration for Time Attack mode
            elif len(selected_cards) < 2 and not game_over:
                for card in cards:
                    if card['rect'].collidepoint(event.pos) and not card['revealed']:
                        flip_card_animation(card, revealing=True)  # Add flip animation here
                        card['revealed'] = True
                        selected_cards.append(card)
                        if len(selected_cards) == 2:
                            screen.fill(white)
                            for card in cards:
                                if card['revealed']:
                                    pygame.draw.rect(screen, card['color'], card['rect'])
                                else:
                                    pygame.draw.rect(screen, grey, card['rect'])
                            pygame.display.flip()
                            pygame.time.wait(400)
                            if selected_cards[0]['id'] == selected_cards[1]['id']:
                                match_sound.play()
                                player_scores[current_turn - 1] += 1  # Increment score
                                cards = [card for card in cards if card not in selected_cards]
                            else:
                                for selected_card in selected_cards:
                                    flip_card_animation(selected_card, revealing=False)  # Add flip animation here
                                    selected_card['revealed'] = False
                                if player_mode == 2:
                                    switch_turn()  # Switch turn only if there is no match
                            selected_cards = []

    screen.fill(white)

    if player_mode == 0:
        player_mode_buttons()
    else:
        for card in cards:
            if card['revealed']:
                pygame.draw.rect(screen, card['color'], card['rect'])
            else:
                pygame.draw.rect(screen, grey, card['rect'])
        if len(cards) == 0:
            game_over = True
            if time_attack_mode:
                if stage_index == len(stage_duration) - 1:
                    # Last stage completed
                    game_over_message = "Congratulations! You have completed all stages successfully!"
                elif stage_index < len(stage_duration) - 1:
                    # Move to next stage
                    game_over_message = f"Well done! Move to the next stage, succeed in {stage_duration[stage_index + 1]} seconds"
                else:
                    game_over_message = "Error: Unknown stage index"
                
                message = font.render(game_over_message, True, green)
                screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2 - 40))
                draw_button("Next Stage", play_again_button, white, green)
        elif game_over and time_attack_mode:
            game_over_message = f"Time's up! You did not succeed. Try again for {stage_duration[0]} seconds."
            message = font.render(game_over_message, True, red)
            screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2 - 40))
            draw_button("Try Again", play_again_button, white, red)
        else:
            elapsed_time = time.time() - start_time
            if time_attack_mode and elapsed_time > time_limit:
                game_over = True
                message = font.render(f"Time's Up! Try again for {stage_duration[stage_index]} seconds.", True, red)
                screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2 - 40))
                draw_button("Try Again", play_again_button, white, red)
            else:
                remaining_time = max(0, time_limit - elapsed_time)
                minutes, seconds = divmod(int(remaining_time), 60)
                timer_text = font.render(f"Time Left: {minutes:02d}:{seconds:02d}", True, black)
                screen.blit(timer_text, (10, 10))
            draw_button("Reset", reset_button, white, red)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()