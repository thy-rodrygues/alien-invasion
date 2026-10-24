import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """Uma classe para gerenciar projéteis (bolas) disparados pelos alienígenas."""

    def __init__(self, ai_game, alien):
        """Cria um projétil circular na posição atual do alienígena."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Define o raio e a cor da bola (vermelha brilhante)
        self.radius = 6
        self.color = (255, 50, 50)

        # Cria a superfície do projétil com suporte a transparência
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        
        self.rect = self.image.get_rect()
        self.rect.midtop = alien.rect.midbottom

        # Armazena a posição vertical como float para movimento suave
        self.y = float(self.rect.y)

    def update(self):
        """Move o projétil para baixo na tela."""
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Desenha o projétil na tela."""
        self.screen.blit(self.image, self.rect)