import pygame
import sys
import random
import imageio

# Função para carregar um GIF animado como uma lista de frames
def load_gif(gif_path):
    gif = imageio.mimread(gif_path)
    frames = [pygame.image.frombuffer(frame, gif[0].shape[1::-1], 'RGB') for frame in gif]
    return frames

# Inicialização do Pygame
pygame.init()

# Definição das constantes
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meu Jogo de Nave")

# Carregar GIF animado
gif_path = 'pt.gif'  # Coloque o caminho correto do seu GIF aqui
background_frames = load_gif(gif_path)

# Carregar imagens
player_image = pygame.image.load('player.png').convert_alpha()
enemy_image = pygame.image.load('inimigo.png').convert_alpha()
enemy2_image = pygame.image.load('inimigo2.png').convert_alpha()  # Adicione os outros inimigos aqui
boss_image = pygame.image.load('boss.png').convert_alpha()  # Adicione a imagem do chefe aqui
powerup_image = pygame.image.load('powerup.png').convert_alpha()
bullet_image = pygame.image.load('bala.png').convert_alpha()

# Carregar sons
collision_sound = pygame.mixer.Sound('som_colisao.mp3')
powerup_sound = pygame.mixer.Sound('som_powerup.mp3')
shoot_sound = pygame.mixer.Sound('som_tiro.wav')
pygame.mixer.music.load('pou.mp3')
pygame.mixer.music.play(-1)  # Toca a música continuamente

# Inicializar variáveis de controle
frame_index = 0
clock = pygame.time.Clock()

# Definição de variáveis do jogo
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 5
player_health = 3
score = 0
current_level = 1
enemies = []
powerups = []
bullets = []

enemy_speed = 3
powerup_speed = 4
bullet_speed = 7
fire_rate = 500  # Milissegundos entre disparos do jogador
last_shot_time = 0
multi_shot = 1  # Número de tiros disparados de uma vez

# Configurações do chefe
boss_health = 0
boss_active = False
boss_x = SCREEN_WIDTH // 2 - 50
boss_y = -100
boss_speed = 2

# Configurações de fases
levels = {
    1: {'enemy_speed': 3, 'enemy_spawn_rate': 0.01, 'powerup_spawn_rate': 0.005, 'boss_health': 20},
    2: {'enemy_speed': 5, 'enemy_spawn_rate': 0.02, 'powerup_spawn_rate': 0.007, 'boss_health': 40},
    3: {'enemy_speed': 7, 'enemy_spawn_rate': 0.03, 'powerup_spawn_rate': 0.01, 'boss_health': 60},
}

# Função para criar novos inimigos
def create_enemy():
    enemy_x = random.randint(50, SCREEN_WIDTH - 50)
    enemy_y = random.randint(-200, -50)
    enemy_type = random.choice([enemy_image, enemy2_image])  # Escolhe aleatoriamente entre os tipos de inimigos
    enemies.append([enemy_x, enemy_y, enemy_type])

# Função para criar novos power-ups
def create_powerup():
    powerup_x = random.randint(50, SCREEN_WIDTH - 50)
    powerup_y = random.randint(-200, -50)
    powerup_type = random.choice(['health', 'rate', 'multi'])  # Adiciona tipo 'multi' para múltiplos disparos
    powerups.append({'x': powerup_x, 'y': powerup_y, 'image': powerup_image, 'type': powerup_type})

# Função para atirar balas
def shoot_bullet(x, y):
    if multi_shot == 1:
        bullets.append([x, y])
    elif multi_shot == 2:
        bullets.append([x - 10, y])
        bullets.append([x + 10, y])
    elif multi_shot == 3:
        bullets.append([x, y])
        bullets.append([x - 10, y])
        bullets.append([x + 10, y])

# Função para detectar colisões
def check_collision(x1, y1, x2, y2, width, height):
    if x1 < x2 + width and x1 + player_image.get_width() > x2 and y1 < y2 + height and y1 + player_image.get_height() > y2:
        return True
    return False

# Loop principal do jogo
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and pygame.time.get_ticks() - last_shot_time > fire_rate:
                shoot_bullet(player_x + player_image.get_width() // 2, player_y)
                shoot_sound.play()
                last_shot_time = pygame.time.get_ticks()

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Limitar movimento do jogador dentro da tela
    if player_x < 0:
        player_x = 0
    elif player_x > SCREEN_WIDTH - player_image.get_width():
        player_x = SCREEN_WIDTH - player_image.get_width()
    if player_y < 0:
        player_y = 0
    elif player_y > SCREEN_HEIGHT - player_image.get_height():
        player_y = SCREEN_HEIGHT - player_image.get_height()

    # Configurações da fase atual
    if current_level in levels:
        enemy_speed = levels[current_level]['enemy_speed']
        enemy_spawn_rate = levels[current_level]['enemy_spawn_rate']
        powerup_spawn_rate = levels[current_level]['powerup_spawn_rate']
        boss_health = levels[current_level]['boss_health']
    else:
        # Fim do jogo, todas as fases completadas
        game_won_text = pygame.font.SysFont(None, 48).render('Você venceu!', True, WHITE)
        screen.blit(game_won_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    # Criar novos inimigos e power-ups aleatoriamente se o chefe não estiver ativo
    if not boss_active:
        if random.random() < enemy_spawn_rate:
            create_enemy()
        if random.random() < powerup_spawn_rate:
            create_powerup()
    else:
        # Movimento do chefe
        boss_y += boss_speed
        if boss_y > SCREEN_HEIGHT - boss_image.get_height():
            boss_speed = -boss_speed
        elif boss_y < 0:
            boss_speed = -boss_speed

        # Verificar colisão do jogador com o chefe
        if check_collision(player_x, player_y, boss_x, boss_y, boss_image.get_width(), boss_image.get_height()):
            collision_sound.play()
            player_health -= 1

    # Movimento dos inimigos
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > SCREEN_HEIGHT:
            enemies.remove(enemy)
            score -= 10  # Penalidade por deixar inimigo escapar
        # Verificar colisão do jogador com inimigos
        if check_collision(player_x, player_y, enemy[0], enemy[1], enemy[2].get_width(), enemy[2].get_height()):
            collision_sound.play()
            enemies.remove(enemy)
            player_health -= 1
            score -= 50  # Penalidade por colidir com inimigo

    # Movimento dos power-ups
    for powerup in powerups[:]:
        powerup['y'] += powerup_speed
        if powerup['y'] > SCREEN_HEIGHT:
            powerups.remove(powerup)
        # Verificar colisão do jogador com power-ups
        if check_collision(player_x, player_y, powerup['x'], powerup['y'], powerup['image'].get_width(), powerup['image'].get_height()):
            powerup_sound.play()
            if powerup['type'] == 'health':
                player_health += 1  # Aumenta a vida do jogador
            elif powerup['type'] == 'rate':
                fire_rate = max(100, fire_rate - 100)  # Aumenta a taxa de disparo
            elif powerup['type'] == 'multi':
                multi_shot = min(3, multi_shot + 1)  # Aumenta o número de disparos
            powerups.remove(powerup)
            score += 100  # Pontuação por coletar power-up

    # Movimento das balas
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        # Verificar colisão das balas com inimigos
        for enemy in enemies[:]:
            if check_collision(bullet[0], bullet[1], enemy[0], enemy[1], enemy[2].get_width(), enemy[2].get_height()):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 50  # Pontuação por destruir inimigo
                break
        # Verificar colisão das balas com o chefe
        if boss_active and check_collision(bullet[0], bullet[1], boss_x, boss_y, boss_image.get_width(), boss_image.get_height()):
            boss_health -= 1
            bullets.remove(bullet)
            if boss_health <= 0:
                score += 500  # Pontuação por derrotar o chefe
                boss_active = False
                current_level += 1
                boss_y = -100
                break

    # Ativar chefe quando a pontuação atingir o limiar
    if score >= current_level * 1000 and not boss_active:
        boss_active = True

    # Desenhar na tela
    screen.blit(background_frames[frame_index], (0, 0))  # Desenha o frame atual do GIF na tela
    screen.blit(player_image, (player_x, player_y))  # Desenha o jogador

    if boss_active:
        screen.blit(boss_image, (boss_x, boss_y))  # Desenha o chefe

    for enemy in enemies:
        screen.blit(enemy[2], (enemy[0], enemy[1]))  # Desenha os inimigos

    for powerup in powerups:
        screen.blit(powerup['image'], (powerup['x'], powerup['y']))  # Desenha os power-ups

    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))  # Desenha as balas

    frame_index = (frame_index + 1) % len(background_frames)  # Avança para o próximo frame do GIF

    # Desenhar texto na tela (pontuação e vida do jogador)
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Pontuação: {score}', True, WHITE)
    health_text = font.render(f'Vidas: {player_health}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))

    pygame.display.flip()
    clock.tick(30)  # Ajusta para taxa de atualização desejada

    # Verificar se o jogador perdeu todas as vidas
    if player_health <= 0:
        game_over_text = pygame.font.SysFont(None, 48).render('GAME OVER', True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Delay antes de fechar o jogo
        pygame.quit()
        sys.exit()

pygame.quit()
sys.exit()
