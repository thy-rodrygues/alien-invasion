import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Uma classe que gerencia os projéteis disparados pela nave."""

    def __init__(self, ai_game):
        """Cria um objeto para o projétil na posição atual da nave."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Garante que lê a cor definida no settings.py
        self.color = (255, 255, 255)

        # Cria um rect para o projétil em (0, 0) e define a posição correta.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Armazena a posição do projétil como um valor em ponto flutuante.
        self.y = float(self.rect.y)

    def update(self):
        """Move o projétil para cima na tela."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Desenha o projétil na tela."""
        pygame.draw.rect(self.screen, self.color, self.rect)