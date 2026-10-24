import sys
import pygame
import random

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from alien_bullet import AlienBullet


class AlienInvasion:
    """Classe geral para gerenciar os ativos e o comportamento do jogo."""

    def __init__(self):
        """Inicializa o jogo e cria os recursos do jogo."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Configura o jogo em TELA CHEIA e atualiza as dimensões reais da tela
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Instancia as estatísticas do jogo e o painel de pontuação
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        
        # Grupo para armazenar os projéteis dos alienígenas
        self.alien_bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Inicia o Alien Invasion em estado inativo
        self.game_active = False

        # Cria o botão Play
        self.play_button = Button(self, "Play")

        # Carrega e inicia a MÚSICA DE FUNDO em loop infinito
        try:
            pygame.mixer.music.load('sounds/background_music.wav')
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except Exception:
            try:
                pygame.mixer.music.load('sounds/background_music.mp3')
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
            except Exception:
                pass

        # Carrega os efeitos sonoros com tratamento de exceção
        try:
            self.bullet_sound = pygame.mixer.Sound('sounds/bullet.wav')
        except Exception as e:
            print(f"Erro ao carregar som do tiro (bullet.wav): {e}")
            self.bullet_sound = None

        try:
            self.alien_die_sound = pygame.mixer.Sound('sounds/alien_die.wav')
        except Exception as e:
            print(f"Erro ao carregar som de morte do alien (alien_die.wav): {e}")
            self.alien_die_sound = None

        try:
            self.shield_activate_sound = pygame.mixer.Sound('sounds/shield_activate.wav')
        except Exception:
            self.shield_activate_sound = None

        try:
            self.shield_break_sound = pygame.mixer.Sound('sounds/shield_break.wav')
        except Exception:
            self.shield_break_sound = None

        try:
            self.alien_shoot_sound = pygame.mixer.Sound('sounds/alien_shoot.wav')
        except Exception:
            self.alien_shoot_sound = None

        try:
            self.ship_hit_sound = pygame.mixer.Sound('sounds/ship_hit.wav')  # Ou explosion.wav, conforme o nome do teu arquivo
        except Exception as e:
            print(f"Erro ao carregar som de impacto da nave: {e}")
            self.ship_hit_sound = None

    
        # Carrega a IMAGEM DE FUNDO (se existir na pasta images)
        try:
            self.bg_image = pygame.image.load('images/space_bg.bmp')
            self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
        except Exception:
            try:
                self.bg_image = pygame.image.load('images/background.bmp')
                self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))
            except Exception:
                self.bg_image = None

    def run_game(self):
        """Inicia o loop principal do jogo."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._fire_alien_bullet()
                self._update_alien_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Responde a eventos de pressionamento de teclas e mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Inicia um novo jogo quando o jogador clica em Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reseta as configurações dinâmicas do jogo
            self.settings.initialize_dynamic_settings()
            
            # Reseta as estatísticas do jogo
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_shield()

            # Limpa aliens e projéteis antigos
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # Cria uma nova frota e centraliza a nave
            self._create_fleet()
            self.ship.center_ship()

            # Oculta o cursor do mouse
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Responde a pressionamentos de tecla."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_w:
            # Ativa o escudo se ele estiver disponível na fase atual
            if self.stats.game_active and self.stats.shield_available and not self.stats.shield_active:
                self.stats.shield_active = True
                self.stats.shield_available = False
                self.sb.prep_shield()  # Atualiza para cor cinza (usado)
                if self.shield_activate_sound:
                    self.shield_activate_sound.play()

    def _check_keyup_events(self, event):
        """Responde a solturas de tecla."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Cria um novo projétil e o adiciona ao grupo de projéteis."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            if self.bullet_sound:
                self.bullet_sound.play()

    def _update_bullets(self):
        """Atualiza a posição dos projéteis e se livra dos projéteis antigos."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Responde a colisões entre projéteis e alienígenas."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            
            # Toca o som de destruição do alienígena
            if self.alien_die_sound:
                self.alien_die_sound.play()

        if not self.aliens:
            self.bullets.empty()
            self.alien_bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.stats.shield_available = True
            self.stats.shield_active = False
            self.sb.prep_level()
            self.sb.prep_shield()

    def _fire_alien_bullet(self):
        """Faz um dos 12 aliens atiradores vivos disparar um projétil."""
        active_shooters = [alien for alien in self.aliens.sprites() if getattr(alien, 'is_shooter', False)]
        
        if active_shooters:
            if random.random() < 0.015:  
                shooter = random.choice(active_shooters)
                new_bullet = AlienBullet(self, shooter)
                self.alien_bullets.add(new_bullet)
                if self.alien_shoot_sound:
                    self.alien_shoot_sound.play()

    def _update_alien_bullets(self):
        """Atualiza a posição dos projéteis alienígenas e gerencia colisões com a nave."""
        self.alien_bullets.update()

        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._handle_ship_hit_by_bullet()

    def _handle_ship_hit_by_bullet(self):
        """Trata o impacto de um projétil alienígena na nave."""
        if self.stats.shield_active:
            self.stats.shield_active = False
            self.alien_bullets.empty()
            if hasattr(self, 'sb'):
                self.sb.prep_shield()
            if self.shield_break_sound:
                self.shield_break_sound.play()
        else:
            self._ship_hit()

    def _create_fleet(self):
        """Cria a frota de alienígenas com 6 linhas e 13 colunas."""
        for row_number in range(self.settings.fleet_rows):
            for alien_number in range(self.settings.fleet_columns):
                self._create_alien(alien_number, row_number)
                
        self._assign_shooters()

    def _create_alien(self, alien_number, row_number):
        """Cria um alienígena e o posiciona na linha correspondente."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        alien.row_number = row_number
        alien.is_shooter = False

        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        
        self.aliens.add(alien)

    def _assign_shooters(self):
        """Seleciona aleatoriamente 12 aliens exclusivamente das 3 fileiras do topo (linhas 0, 1 e 2)."""
        top_row_aliens = [alien for alien in self.aliens.sprites() if alien.row_number < 3]
        num_shooters = min(16, len(top_row_aliens))
        
        if top_row_aliens:
            chosen_shooters = random.sample(top_row_aliens, num_shooters)
            for alien in chosen_shooters:
                alien.is_shooter = True

    def _check_fleet_edges(self):
        """Responde se algum alienígena atingiu as bordas."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Faz toda a frota descer e mudar a sua direção."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
     """Responde ao fato de a nave ter sido atingida por um alien."""
     if self.stats.ships_left > 0:
         self.stats.ships_left -= 1
         self.sb.prep_ships()

         # Toca o som de impacto/destruição da nave
         if self.ship_hit_sound:
             self.ship_hit_sound.play()

         self.stats.shield_active = False
         self.sb.prep_shield()

         self.aliens.empty()
         self.bullets.empty()
         self.alien_bullets.empty()

         self._create_fleet()
         self.ship.center_ship()

         pygame.time.wait(500)
     else:
         self.stats.game_active = False
         pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Verifica se algum alienígena chegou à parte inferior da tela."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_aliens(self):
        """Verifica se a frota está nas bordas, então atualiza as posições."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._handle_ship_hit_by_alien()

        self._check_aliens_bottom()

    def _handle_ship_hit_by_alien(self):
        """Trata o impacto direto da nave contra um alienígena."""
        if self.stats.shield_active:
            self.stats.shield_active = False
            if hasattr(self, 'sb'):
                self.sb.prep_shield()
            if self.shield_break_sound:
                self.shield_break_sound.play()
        else:
            self._ship_hit()

    def _update_screen(self):
        """Atualiza as imagens na tela e alterna para a nova tela."""
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(self.settings.bg_color)
        
        # Desenha os projéteis dos alienígenas
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Desenha a informação de pontuação
        self.sb.show_score()

        # Desenha o botão Play se o jogo estiver inativo
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()