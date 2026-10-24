class Settings:
    """Uma classe para armazenar todas as configurações do Alien Invasion."""

    def __init__(self):
        """Inicializa as configurações estáticas do jogo."""
        # Configurações da tela
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (15, 15, 30)

        # Configurações da nave (Aumentado para a nave ficar bem ágil e rápida)
        self.ship_speed = 4.5
        self.ship_limit = 3

        # Configurações dos projéteis do jogador (Cor branca pura e velocidade ajustada)
        self.bullet_speed = 3.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)  # Branco puro para destacar no fundo escuro
        self.bullets_allowed = 6             # Permitir mais tiros simultâneos para maior dinamismo

        # Configurações dos alienígenas e da frota
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_rows = 6
        self.fleet_columns = 13
        
        # Configuração dos projéteis dos alienígenas (bolas vermelhas)
        self.alien_bullet_speed = 3.0

        # fleet_direction de 1 representa a direita; -1 representa a esquerda.
        self.fleet_direction = 1

        # Taxa com que a velocidade do jogo aumenta
        self.speedup_scale = 1.1
        # Taxa com que os pontos dos alienígenas aumentam
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa as configurações que mudam ao longo do jogo."""
        self.ship_speed = 3.5
        self.bullet_speed = 3.5
        self.alien_speed = 1.0

        # Pontuação para cada alienígena
        self.alien_points = 50

    def increase_speed(self):
        """Aumenta as configurações de velocidade e os pontos dos alienígenas."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)