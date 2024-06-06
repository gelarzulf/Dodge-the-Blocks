import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Warna
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Pengaturan Player
player_size = 50
player_color = blue
player_pos = [screen_width // 2, screen_height - 2 * player_size]

# Pengaturan NPC
npc_size = 50
npc_color = red
npc_list = []

# Kecepatan
speed = 10
clock = pygame.time.Clock()
game_over = False
score = 0
high_score = 0  # Tambahkan variabel untuk high score

# Font
font = pygame.font.SysFont("monospace", 35)
small_font = pygame.font.SysFont("monospace", 20)

def set_level(score, speed):
    if score < 20:
        speed = 5
    elif score < 40:
        speed = 7
    elif score < 60:
        speed = 10
    else:
        speed = 15
    return speed

def drop_npcs(npc_list):
    delay = random.random()
    if len(npc_list) < 10 and delay < 0.1:
        while True:
            x_pos = random.randint(0, screen_width - npc_size)
            y_pos = 0
            new_npc = [x_pos, y_pos]
            if not any(detect_collision(new_npc, npc) for npc in npc_list):
                npc_list.append(new_npc)
                break

def draw_npcs(npc_list):
    for npc_pos in npc_list:
        pygame.draw.rect(screen, npc_color, (npc_pos[0], npc_pos[1], npc_size, npc_size))

def update_npc_positions(npc_list, score):
    for idx, npc_pos in enumerate(npc_list):
        if npc_pos[1] >= 0 and npc_pos[1] < screen_height:
            npc_pos[1] += speed
        else:
            npc_list.pop(idx)
            score += 1
    return score

def collision_check(npc_list, player_pos):
    for npc_pos in npc_list:
        if detect_collision(npc_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, npc_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = npc_pos[0]
    e_y = npc_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + npc_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + npc_size)):
            return True
    return False

def game_over_screen():
    global high_score, score
    if score > high_score:
        high_score = score

    screen.fill(black)
    game_over_text = "Game Over!"
    restart_text = "Play Again  Quit"
    high_score_text = f"High Score: {high_score}"

    game_over_label = font.render(game_over_text, 1, white)
    restart_label = font.render(restart_text, 1, white)
    high_score_label = font.render(high_score_text, 1, white)

    screen.blit(game_over_label, (screen_width // 2 - game_over_label.get_width() // 2, screen_height // 2 - 100))
    screen.blit(high_score_label, (screen_width // 2 - high_score_label.get_width() // 2, screen_height // 2 - 50))
    screen.blit(restart_label, (screen_width // 2 - restart_label.get_width() // 2, screen_height // 2 + 50))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
    return False

def game_loop():
    global game_over, score, speed, player_pos, npc_list, high_score
    player_pos = [screen_width // 2, screen_height - 2 * player_size]
    npc_list = []
    speed = 10
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                x = player_pos[0]
                y = player_pos[1]
                if event.key == pygame.K_LEFT:
                    x -= player_size
                elif event.key == pygame.K_RIGHT:
                    x += player_size

                # Pastikan player tidak menembus tembok kiri atau kanan
                if x < 0:
                    x = 0
                elif x > screen_width - player_size:
                    x = screen_width - player_size

                player_pos = [x, y]

        screen.fill(black)

        drop_npcs(npc_list)
        score = update_npc_positions(npc_list, score)
        speed = set_level(score, speed)

        text = "Score: " + str(score)
        high_score_text = "High Score: " + str(high_score)
        label = small_font.render(text, 1, white)
        high_score_label = small_font.render(high_score_text, 1, white)

        screen.blit(label, (screen_width - label.get_width() - 10, screen_height - label.get_height() - 10))
        screen.blit(high_score_label, (10, screen_height - high_score_label.get_height() - 10))

        if collision_check(npc_list, player_pos):
            game_over = True

        draw_npcs(npc_list)

        pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))

        clock.tick(30)

        pygame.display.update()

while True:
    game_loop()
    if not game_over_screen():
        break

pygame.quit()
