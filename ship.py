import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Classe para gerenciar a espaçonave"""

    def __init__(self, ai_game):
        """Inicializa a espaçonave e define sua posição inicial"""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.screen_rect = ai_game.screen.get_rect()

        # Carrega a imagem normal da espaçonave (largura de 50 pixels)
        original_image = pygame.image.load('images/ship.bmp')
        aspect_ratio = original_image.get_height() / original_image.get_width()
        new_width = 50
        new_height = int(new_width * aspect_ratio)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        
        # Carrega a imagem da nave com escudo
        try:
            original_shield_ship = pygame.image.load('images/ship_with_shield.bmp')
            shield_aspect = original_shield_ship.get_height() / original_shield_ship.get_width()
            shield_width = 70  # Um pouco maior para acomodar a bolha do escudo
            shield_height = int(shield_width * shield_aspect)
            self.image_with_shield = pygame.transform.scale(original_shield_ship, (shield_width, shield_height))
        except Exception as e:
            print(f"Aviso - 'images/ship_with_shield.bmp' não encontrada: {e}")
            self.image_with_shield = self.image

        self.rect = self.image.get_rect()

        # Inicia cada nova espaçonave na parte inferior central da tela
        self.rect.midbottom = self.screen_rect.midbottom

        # Armazena um valor flutuante para a posição horizontal da espaçonave
        self.x = float(self.rect.x)

        # Flag de movimento
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Atualiza a posição da espaçonave com base nas flags de movimento"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """Desenha a espaçonave ou a nave com escudo em sua posição atual"""
        if self.stats.shield_active:
            # Desenha a nave com escudo centralizada no rect principal
            shield_rect = self.image_with_shield.get_rect()
            shield_rect.center = self.rect.center
            self.screen.blit(self.image_with_shield, shield_rect)
        else:
            self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centraliza a espaçonave na tela"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
    def activate_shield(self):
        """Ativa o escudo se disponível e consome-o para esta fase."""
        if self.stats.shield_available and not self.stats.shield_active:
            self.stats.shield_active = True
            self.stats.shield_available = False  # Torna indisponível pelo resto da fase
            
            # Atualiza o scoreboard imediatamente para o ícone ficar cinza
            if hasattr(self.ai_game, 'sb'):
                self.ai_game.sb.prep_shield()
                
            if hasattr(self.ai_game, 'shield_activate_sound'):
                self.ai_game.shield_activate_sound.play()