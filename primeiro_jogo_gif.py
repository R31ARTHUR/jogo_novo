import pygame
import sys
import imageio

# Função para carregar um GIF animado como uma lista de frames
def load_gif(gif_path):
    gif = imageio.mimread(gif_path)
    frames = [pygame.image.frombuffer(frame, gif[0].shape[1::-1], 'RGB') for frame in gif]
    return frames

# Inicialização do Pygame
pygame.init()

# Definição das constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meu Jogo com Fundo Animado e Movimento de Jogador")

# Carregar GIF animado
gif_path = 'pt.gif'  # Coloque o caminho correto do seu GIF aqui
background_frames = load_gif(gif_path)

# Carregar imagem do jogador
player_image = pygame.image.load('player.png').convert_alpha()
player_rect = player_image.get_rect()
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Inicializar variáveis de controle
frame_index = 0
clock = pygame.time.Clock()

# Velocidade de movimento do jogador
player_speed = 5

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verificar as teclas pressionadas para mover o jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # Desenhar o frame atual do GIF na tela
    screen.blit(background_frames[frame_index], (0, 0))

    # Desenhar o jogador na tela
    screen.blit(player_image, player_rect)

    # Avançar para o próximo frame do GIF
    frame_index = (frame_index + 1) % len(background_frames)

    pygame.display.flip()
    clock.tick(30)  # Ajustar para taxa de atualização desejada

pygame.quit()
sys.exit()
