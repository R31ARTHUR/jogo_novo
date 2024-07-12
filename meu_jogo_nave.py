import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definição das constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meu Jogo de Nave")

# Carregar imagens
background = pygame.image.load('imagens/fundo.png').convert()
player_image = pygame.image.load('imagens/player.png').convert_alpha()
enemy_image = pygame.image.load('imagens/inimigo.png').convert_alpha()
powerup_image = pygame.image.load('imagens/powerup.png').convert_alpha()

# Carregar sons
collision_sound = pygame.mixer.Sound('som_colisao.wav')
powerup_sound = pygame.mixer.Sound('som_powerup.wav')

# Carregar música de fundo
pygame.mixer.music.load('musica_fundo.wav')
pygame.mixer.music.set_volume(0.5)  # Ajustar volume da música
pygame.mixer.music.play(-1)  # Reproduzir música em loop

# Definição de variáveis do jogo
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 5
player_health = 3
score = 0

enemies = []
powerups = []

enemy_speed = 3
powerup_speed = 4

# Função para criar novos inimigos
def create_enemy():
    enemy_x = random.randint(50, SCREEN_WIDTH - 50)
    enemy_y = random.randint(-200, -50)
    enemies.append([enemy_x, enemy_y])

# Função para criar novos power-ups
def create_powerup():
    powerup_x = random.randint(50, SCREEN_WIDTH - 50)
    powerup_y = random.randint(-200, -50)
    powerups.append([powerup_x, powerup_y])

# Função para detectar colisões
def check_collision(x1, y1, x2, y2):
    distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    if distance < 50:  # Ajuste conforme o tamanho dos objetos
        return True
    return False

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    # Criar novos inimigos e power-ups aleatoriamente
    if random.random() < 0.01:
        create_enemy()
    if random.random() < 0.005:
        create_powerup()

    # Movimento dos inimigos
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > SCREEN_HEIGHT:
            enemies.remove(enemy)
            score -= 10  # Penalidade por deixar inimigo escapar

        # Verificar colisão do jogador com inimigos
        if check_collision(player_x, player_y, enemy[0], enemy[1]):
            collision_sound.play()
            enemies.remove(enemy)
            player_health -= 1
            score -= 50  # Penalidade por colidir com inimigo

    # Movimento dos power-ups
    for powerup in powerups:
        powerup[1] += powerup_speed
        if powerup[1] > SCREEN_HEIGHT:
            powerups.remove(powerup)

        # Verificar colisão do jogador com power-ups
        if check_collision(player_x, player_y, powerup[0], powerup[1]):
            powerup_sound.play()
            powerups.remove(powerup)
            score += 100  # Pontuação por coletar power-up

    # Desenhar na tela
    screen.blit(background, (0, 0))  # Desenha o fundo
    screen.blit(player_image, (player_x, player_y))  # Desenha o jogador

    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))  # Desenha os inimigos

    for powerup in powerups:
        screen.blit(powerup_image, (powerup[0], powerup[1]))  # Desenha os power-ups

    # Desenhar texto na tela (pontuação e vida do jogador)
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Pontuação: {score}', True, WHITE)
    health_text = font.render(f'Vidas: {player_health}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))

    # Verificar se o jogador perdeu todas as vidas
    if player_health <= 0:
        game_over_text = font.render('GAME OVER', True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Delay antes de fechar o jogo
        pygame.quit()
        sys.exit()

    pygame.display.flip()

    # Ajustar velocidade de atualização da tela
    pygame.time.Clock().tick(60)
