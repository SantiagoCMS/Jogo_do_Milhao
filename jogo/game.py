import pygame
from jogo.menus import MainMenu, OptionsMenu
from jogo.assets import Assets
from jogo.subjects_menu import SubjectsMenu
from jogo.game_screen import GameScreen
from jogo.ranking_screen import RankingScreen

class Game:
    """Controlador principal do jogo (inicializa Pygame, menus e gerencia a troca de telas)."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Tamanho da janela
        self.SCREEN_WIDTH = 1080
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Code Milionário")

        # Carrega imagens, sons, fontes, etc.
        self.assets = Assets()

        # Inicializa todas as telas
        self.main_menu = MainMenu(self.screen, self.assets)
        self.options_menu = OptionsMenu(self.screen, self.assets)
        self.subjects_menu = SubjectsMenu(self.screen, self.assets)
        self.game_screen = GameScreen(self.screen, self.assets)
        self.ranking_screen = RankingScreen(self.screen, self.assets)

        self.running = True  # Loop principal

    def run(self):
        """Executa o loop principal do jogo."""
        while self.running:
            # Fundo e logo
            self.screen.blit(self.assets.background, (0, 0))
            logo_x = (self.SCREEN_WIDTH - self.assets.logo_img.get_width()) // 2
            self.screen.blit(self.assets.logo_img, (logo_x, 30))

            # Menu principal: se "Jogar" for clicado
            if self.main_menu.update():
                self.assets.click_sound.play()
                self.subjects_menu.show()

                # Se o botão "Iniciar" foi clicado após escolher a matéria
                if self.subjects_menu.start_clicked:
                    self.game_screen.show()

            # Menu de opções
            if self.main_menu.options_clicked:
                self.assets.click_sound.play()
                tela_foi_alterada = self.options_menu.show()
                self.main_menu.options_clicked = False

                if tela_foi_alterada:
                    # Altera entre modo janela e tela cheia
                    if self.options_menu.is_fullscreen:
                        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

                    # Atualiza a referência da tela nas outras telas
                    self.main_menu.screen = self.screen
                    self.options_menu.screen = self.screen
                    self.subjects_menu.screen = self.screen
                    self.game_screen.screen = self.screen

            # Se "Sair" for clicado
            if self.main_menu.exit_clicked:
                self.assets.click_sound.play()
                self.running = False

            # Fecha o jogo se clicar no "X"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()

        pygame.quit()