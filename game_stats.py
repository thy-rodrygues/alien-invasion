import os

class GameStats:
    """Armazena estatísticas para o Alien Invasion."""

    def __init__(self, ai_game):
        """Inicializa as estatísticas."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Inicia o jogo em um estado inativo
        self.game_active = False

        # Carrega o high score salvo de um arquivo (se existir)
        self.high_score = self.load_high_score()

    def reset_stats(self):
        """Inicializa estatísticas que podem mudar durante o jogo."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        
        # Variáveis do Escudo
        self.shield_available = True
        self.shield_active = False

    def load_high_score(self):
        """Lê o high score de um arquivo de texto, se existir."""
        try:
            if os.path.exists('high_score.txt'):
                with open('high_score.txt', 'r') as f:
                    return int(f.read().strip())
        except Exception:
            pass
        return 0

    def save_high_score(self):
        """Salva o high score atual em um arquivo de texto."""
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(int(self.high_score)))
        except Exception:
            pass