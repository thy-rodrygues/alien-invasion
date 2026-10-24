import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Um classe que representa um único alienígena da frota."""

    def __init__(self, ai_game):
        """Inicializa o alienígena e define sua posição inicial."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carrega a imagem do alienígena e redimensiona para largura de 50 pixels
        original_image = pygame.image.load('images/alien.bmp')
        aspect_ratio = original_image.get_height() / original_image.get_width()
        new_width = 50
        new_height = int(new_width * aspect_ratio)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        
        self.rect = self.image.get_rect()

        # Inicia cada novo alienígena perto do canto superior esquerdo da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Armazena a posição exata do alienígena
        self.x = float(self.rect.x)

    def check_edges(self):
        """Retorna True se o alienígena estiver na borda da tela"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move o alienígena para a direita ou para a esquerda"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x