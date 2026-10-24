import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """Uma classe para relatar informações de pontuação."""

    def __init__(self, ai_game):
        """Inicializa os atributos de pontuação."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Cor do texto em branco puro
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepara as imagens iniciais
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_shield()
        self.prep_ships()

    def prep_score(self):
        """Transforma a pontuação em uma imagem renderizada com fundo transparente."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Transforma a pontuação máxima em uma imagem renderizada."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Verifica se há uma nova pontuação máxima."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Transforma o nível em uma imagem renderizada com fundo transparente."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Mostra quantas vidas restam."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            scale_factor = 30 / ship.image.get_width()
            new_width = 30
            new_height = int(ship.image.get_height() * scale_factor)
            ship.image = pygame.transform.scale(ship.image, (new_width, new_height))
            
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)
            
    def prep_shield(self):
        """Prepara a imagem do escudo com tamanho proporcional e alinhada verticalmente com as vidas."""
        try:
            original_shield = pygame.image.load('images/shield.bmp')
        except Exception as e:
            print(f"Erro ao carregar shield.bmp: {e}")
            original_shield = pygame.Surface((30, 30))
            
        # Tamanho ideal de 30 pixels para equiparar com as vidas
        target_size = 30
        self.shield_image = pygame.transform.scale(original_shield, (target_size, target_size))
        
        # Cria a versão cinza utilizando a função nativa do Pygame
        try:
            self.shield_image_gray = pygame.transform.grayscale(self.shield_image)
        except Exception:
            self.shield_image_gray = self.shield_image.copy()

        # Define se exibe colorido (disponível) ou cinza (usado/indisponível)
        if self.stats.shield_available:
            self.active_shield_image = self.shield_image
        else:
            self.active_shield_image = self.shield_image_gray
            
        # Descobre a altura da nave de vida para centralizar o escudo perfeitamente na vertical
        temp_ship = Ship(self.ai_game)
        scale_factor = 30 / temp_ship.image.get_width()
        life_height = int(temp_ship.image.get_height() * scale_factor)
        
        # Posição X logo após o grupo de vidas
        shield_layout_x = 10 + (self.settings.ship_limit * (30 + 10)) + 10
        
        # Posição Y ajustada para subir o escudo e centralizá-lo em relação à altura das vidas
        shield_layout_y = 10 + (life_height - target_size) // 2
        
        self.active_shield_image_rect = self.active_shield_image.get_rect()
        self.active_shield_image_rect.x = shield_layout_x
        self.active_shield_image_rect.y = shield_layout_y

    def show_score(self):
        """Desenha as pontuações, o nível, o escudo e as naves na tela."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.active_shield_image, self.active_shield_image_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Verifica se há uma nova pontuação máxima."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.stats.save_high_score()  # Salva permanentemente no arquivo
            self.prep_high_score()